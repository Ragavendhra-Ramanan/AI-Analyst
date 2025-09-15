from abc import ABC, abstractmethod
from typing import Optional

from fastapi import BackgroundTasks, UploadFile


class FileProcessor(ABC):
    @abstractmethod
    async def process(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks,
        file_name: Optional[str] = None,
    ):
        pass
