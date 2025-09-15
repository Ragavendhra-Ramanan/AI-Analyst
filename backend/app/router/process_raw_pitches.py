import os

from fastapi import APIRouter, BackgroundTasks, UploadFile
from fastapi.responses import JSONResponse
from processors.factory import ProcessorFactory

router = APIRouter()


@router.post("/upload/")
async def generate_deal_note(file: UploadFile, background_tasks: BackgroundTasks):
    processor = ProcessorFactory.get_processor(file)
    filename = os.path.splitext(file.filename)[0]  # remove extension
    result = await processor.process(
        file=file, background_tasks=background_tasks, file_name=filename
    )

    return JSONResponse(content=result)
