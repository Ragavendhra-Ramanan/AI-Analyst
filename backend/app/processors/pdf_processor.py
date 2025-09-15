import asyncio
import io
import os
from typing import Optional

import pymupdf  # PyMuPDF
from fastapi import BackgroundTasks, UploadFile
from langchain.output_parsers import PydanticOutputParser
from models.pitch_extractor import PitchExtractor
from PIL import Image
from prompts.multimodal_extraction_prompt import MULTIMODAL_EXTRACTION_PROMPT
from services.gemini.api import call_gemini_api
from storage.store_raw_pitch import save_file
from utils.gcs_utils import upload_images_to_gcs, upload_raw_pitch_async
from vertexai.preview.generative_models import Image as GeminiImage

from .base import FileProcessor

DPI = 200
TEXT_THRESHOLD = 100


class PDFProcessor(FileProcessor):
    async def process(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks,
        file_name: Optional[str] = None,
    ):
        pdf_path = await save_file(file, "pdf", file_name)
        pdf_data_with_application = {}
        pages, page_numbers = await asyncio.to_thread(
            self.pdf_to_images_filtered, pdf_path, file_name, DPI
        )
        pdf_data = []

        for img, num in zip(pages, page_numbers):
            print(f"Processing {os.path.basename(pdf_path)} - Page {num}...")
            page_json = await self.extract_data_from_page(img, num, file_name)
            pdf_data.append(page_json)

        pdf_data_with_application[os.path.basename(pdf_path)] = pdf_data
        background_tasks.add_task(upload_raw_pitch_async, file_name, pdf_data)
        background_tasks.add_task(upload_images_to_gcs, file_name)
        return pdf_data_with_application

    def pdf_to_images_filtered(self, pdf_path, app_name, dpi):
        doc = pymupdf.open(pdf_path)
        images, page_numbers = [], []

        for page_number in range(len(doc)):
            page = doc[page_number]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            os.makedirs(f"uploads/{app_name}/images", exist_ok=True)
            img.save(
                os.path.join(
                    f"uploads/{app_name}/images",
                    f"{os.path.basename(pdf_path)}_page_{page_number + 1}.png",
                )
            )
            images.append(img)
            page_numbers.append(page_number + 1)

        return images, page_numbers

    async def extract_data_from_page(self, image, page_number, app_name):
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        gemini_img = GeminiImage.from_bytes(buf.getvalue())
        parser = PydanticOutputParser(pydantic_object=PitchExtractor)
        prompt = MULTIMODAL_EXTRACTION_PROMPT.format(app_name=app_name)
        content = [prompt, gemini_img]
        parsed_result = await asyncio.to_thread(
            call_gemini_api,
            model_name="gemini-2.5-flash-lite",
            content=content,
            dynamic_parser=parser,  # Use a dynamic parser for flexible JSON
        )
        parsed_result["page_number"] = page_number
        return parsed_result
