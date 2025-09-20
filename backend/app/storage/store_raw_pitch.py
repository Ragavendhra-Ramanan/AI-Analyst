import os

from fastapi import UploadFile

BASE_UPLOAD_DIR = "uploads"
SUBDIRS = ["pdf", "video", "audio", "json"]


async def save_file(file: UploadFile, file_type: str, app_name: str) -> str:
    if file_type not in SUBDIRS:
        raise ValueError("Invalid file type for storage.")
    # Ensure directories exist
    for subdir in SUBDIRS:
        os.makedirs(
            os.path.join(f"{BASE_UPLOAD_DIR}/{app_name}", subdir), exist_ok=True
        )

    file_path = os.path.join(f"{BASE_UPLOAD_DIR}/{app_name}", file_type, file.filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path
