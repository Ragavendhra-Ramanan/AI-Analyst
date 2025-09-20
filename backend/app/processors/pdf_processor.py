import asyncio
import io
import os
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

import pymupdf  # PyMuPDF
from fastapi import BackgroundTasks, UploadFile
from PIL import Image
from prompts.multimodal_extraction_prompt import MULTIMODAL_EXTRACTION_PROMPT
from services.gemini_api import call_gemini_api
from storage.store_raw_pitch import save_file
from utils.gcs_utils import upload_images_to_gcs, upload_raw_pitch_async
from vertexai.preview.generative_models import Image as GeminiImage

from .base import FileProcessor

DPI = 200


class PDFProcessor(FileProcessor):
    async def process(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks,
        file_name: Optional[str] = None,
    ):
        pdf_path = await save_file(file, "pdf", file_name)

        # Convert PDF to images concurrently
        pages, page_numbers = await self.pdf_to_images_concurrent(
            pdf_path, file_name, DPI
        )

        # Run Gemini API calls **sequentially** (one by one)
        pdf_data = []
        for img, page_num in zip(pages, page_numbers):
            page_result = await self.extract_data_from_page(
                img, file_name, page_num, pdf_path
            )
            pdf_data.append(page_result)

        # Background uploads
        background_tasks.add_task(upload_raw_pitch_async, file_name, pdf_data)
        background_tasks.add_task(upload_images_to_gcs, file_name)
        return pdf_data

    async def pdf_to_images_concurrent(self, pdf_path, app_name, dpi):
        """Convert PDF pages to images concurrently using threads."""
        doc = pymupdf.open(pdf_path)
        images = []
        page_numbers = []

        def render_page(page_number):
            page = doc[page_number]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Save image
            os.makedirs(f"uploads/{app_name}/images", exist_ok=True)
            img.save(
                os.path.join(
                    f"uploads/{app_name}/images",
                    f"{os.path.basename(pdf_path)}_page_{page_number + 1}.png",
                )
            )
            return img, page_number + 1

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            tasks = [
                loop.run_in_executor(executor, render_page, i) for i in range(len(doc))
            ]
            results = await asyncio.gather(*tasks)

        for img, page_number in results:
            images.append(img)
            page_numbers.append(page_number)

        return images, page_numbers

    async def extract_data_from_page(self, image, app_name, page_number, pdf_path):
        """Call Gemini API for a single page sequentially with delay."""
        print(f"Processing {os.path.basename(pdf_path)} - Page {page_number}...")

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        gemini_img = GeminiImage.from_bytes(buf.getvalue())

        prompt = MULTIMODAL_EXTRACTION_PROMPT.format(app_name=app_name)
        content = [prompt, gemini_img]

        # Call Gemini API in thread to avoid blocking event loop
        parsed_result = await asyncio.to_thread(
            call_gemini_api,
            model_name="gemini-2.5-flash-lite",
            content=content,
        )

        return parsed_result
