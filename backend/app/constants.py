import os

from dotenv import load_dotenv

load_dotenv()  # load variables from .env file

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
GCS_BUCKET = os.getenv("GCS_BUCKET")
