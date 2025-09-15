import os

from fastapi import APIRouter, BackgroundTasks, UploadFile
from fastapi.responses import StreamingResponse
from processors.factory import ProcessorFactory
from refiners.pitch_common_refiner import refine_pitch_content
from generate_deal_note import create_deal_note_async

router = APIRouter()


@router.post("/upload/")
async def generate_deal_note(file: UploadFile, background_tasks: BackgroundTasks):
    processor = ProcessorFactory.get_processor(file)
    filename = os.path.splitext(file.filename)[0]
    raw_pitch_contents = await processor.process(
        file=file, background_tasks=background_tasks, file_name=filename
    )
    refined_pitch_content = await refine_pitch_content(raw_pitch_contents)
    pdf_buffer = await create_deal_note_async(refined_pitch_content)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={filename}_deal_note.pdf"},
    )
