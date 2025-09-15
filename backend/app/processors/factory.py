from fastapi import HTTPException, UploadFile

from .base import FileProcessor
from .pdf_processor import PDFProcessor


class ProcessorFactory:
    @staticmethod
    def get_processor(file: UploadFile) -> FileProcessor:
        filename = file.filename.lower()
        content_type = file.content_type.lower()
        process_type = None

        if filename.endswith((".pdf")):
            process_type = "pdf"
        elif content_type.startswith("video/"):
            process_type = "video"
        elif content_type.startswith("audio/"):
            process_type = "audio"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if process_type == "pdf":
            return PDFProcessor()
        else:
            raise HTTPException(status_code=400, detail="Invalid process_type")
