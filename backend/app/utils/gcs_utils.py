import asyncio
import json
import os
from ..constants import GCS_BUCKET
from google.cloud import storage


client = storage.Client()
bucket = client.bucket(GCS_BUCKET)


async def upload_raw_pitch_async(deck_name: str, data: dict):
    blob = bucket.blob(f"{deck_name}/raw_{deck_name}.json")
    await asyncio.to_thread(
        blob.upload_from_string,
        json.dumps(data, indent=2),
        content_type="application/json",
    )
    print(f"Uploaded JSON to gs://{GCS_BUCKET}/{deck_name}/raw_{deck_name}.json")
    return f"gs://{GCS_BUCKET}/{deck_name}/raw_{deck_name}.json"


# Upload local images asynchronously
async def upload_images_to_gcs(deck_name: str):
    """
    Upload all PNG images from local_dir to GCS under folder deck_name.
    Returns a dict: {page_number: gcs_link}
    """
    gcs_links = {}

    for filename in os.listdir(f"uploads/{deck_name}/images"):
        if filename.endswith(".png"):
            local_path = os.path.join(f"uploads/{deck_name}/images", filename)
            blob_path = f"{deck_name}/images/{filename}"
            blob = bucket.blob(blob_path)
            # Upload in separate thread
            await asyncio.to_thread(blob.upload_from_filename, local_path)

            # Public link (or signed URL if needed)
            gcs_link = f"https://storage.googleapis.com/{GCS_BUCKET}/{blob_path}"
            # Extract page number from filename
            page_number = int(filename.split("_page_")[1].split(".png")[0])
            gcs_links[page_number] = gcs_link

    print(f"Uploaded {len(gcs_links)} images to GCS for deck {deck_name}")
    return gcs_links
