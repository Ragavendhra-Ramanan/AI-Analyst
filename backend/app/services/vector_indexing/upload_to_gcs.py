import json
import os
from google.cloud import storage
import asyncio
from storage.store_raw_pitch import BASE_UPLOAD_DIR


def write_chunks_to_jsonl(chunks, filename: str):
    """
    Writes list of chunks to a JSONL file. Each line is a JSON object.
    """
    app_name = filename.split(".")[0]
    file_path = os.path.join(f"{BASE_UPLOAD_DIR}/{app_name}", "json", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            # JSON object you want in each line
            obj = {
                "content": chunk["text"],
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print("local file write successfull")
    return file_path


async def upload_file_to_gcs(
    chunks, bucket_name: str, local_file_path: str, destination_blob_name: str
):
    """
    Upload the local jsonl file to GCS.
    """
    # If using service account JSON, ensure env var is set:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/key.json"
    local_full_file_path = await asyncio.to_thread(
        write_chunks_to_jsonl, chunks, local_file_path
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_full_file_path)
    print(
        f"Uploaded {local_full_file_path} to gs://{bucket_name}/{destination_blob_name}"
    )
