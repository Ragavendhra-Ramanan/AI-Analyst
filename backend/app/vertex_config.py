# config.py
import os

import vertexai
from dotenv import load_dotenv

load_dotenv()  # load variables from .env file

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")


def init_vertex():
    vertexai.init(project=PROJECT_ID, location=REGION)
