import os

from fastapi import APIRouter, BackgroundTasks, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from processors.factory import ProcessorFactory
from refiners.pitch_common_refiner import refine_pitch_content
from generate_deal_note import create_deal_note_async
from dotenv import load_dotenv
from services.vector_indexing.chunking import chunk_markdown_slides
from services.vector_indexing.create_corpus import upload_to_rag_corpus
from services.vector_indexing.upload_to_gcs import upload_file_to_gcs
from services.rag_agent.rag_config import rag_registry

router = APIRouter()

load_dotenv()  # load variables from .env file

GCS_BUCKET = os.getenv("GCS_BUCKET")


@router.post("/upload/")
async def generate_deal_note(file: UploadFile, background_tasks: BackgroundTasks):
    processor = ProcessorFactory.get_processor(file)
    filename = os.path.splitext(file.filename)[0]
    raw_pitch_contents = await processor.process(
        file=file, background_tasks=background_tasks, file_name=filename
    )
    chunks = await chunk_markdown_slides(md_slides=raw_pitch_contents, doc_id=filename)
    await upload_file_to_gcs(
        chunks,
        GCS_BUCKET,
        f"{filename}.jsonl",
        f"{filename}/{filename}.jsonl",
    )
    rag_corpus_name = await upload_to_rag_corpus(
        display_name=filename, file_name=f"{filename}.jsonl"
    )
    rag_registry.set("corpus_name", rag_corpus_name)

    return JSONResponse(content=raw_pitch_contents)
