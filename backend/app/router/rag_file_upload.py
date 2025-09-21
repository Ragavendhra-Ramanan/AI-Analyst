import os

from fastapi import APIRouter, BackgroundTasks, UploadFile
from ..processors.factory import ProcessorFactory
from ..services.vector_indexing.chunking import chunk_markdown_slides
from ..services.vector_indexing.create_corpus import upload_to_rag_corpus
from ..services.vector_indexing.upload_to_gcs import upload_file_to_gcs
from ..services.rag_agent.rag_config.rag_registry import rag_registry
from ..constants import GCS_BUCKET

router = APIRouter()


@router.post("/upload/")
async def upload_rag_data(file: UploadFile, background_tasks: BackgroundTasks):
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
    rag_registry.set("company_name", filename)
    rag_corpus_name = await upload_to_rag_corpus(
        display_name=filename, file_name=f"{filename}.jsonl"
    )
    rag_registry.set("corpus_name", rag_corpus_name)

    return {
        "message": "File uploaded and processing completed",
        "file": file.filename,
    }
