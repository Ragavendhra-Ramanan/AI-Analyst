"""Configuration settings for the Investor Memo Processing system."""

import os

# GCS Configuration
BUCKET_NAME = 'lvx-investor-memos-bucket-1'

# Firestore Configuration
FIRESTORE_COLLECTION = 'structured_investor_memos'

# File Paths
DEFAULT_PDF_DIR = 'pdfs'
DEFAULT_OUTPUT_DIR = 'extracted_texts'
PROMPT_TEMPLATE_FILE = 'extracted_prompt_template.txt'

# Visualization Settings
VISUALIZATION_DPI = 300
CHART_STYLE = 'whitegrid'

# PDF Report Settings
PDF_PAGE_SIZE = 'A4'
PDF_FONT_SIZE = 12
PDF_MARGIN = 1  # inch

# Environment Variables
GEMINI_API_KEY_ENV = 'GEMINI_API_KEY'

def get_gemini_api_key():
    """Get Gemini API key from environment variable."""
    return os.getenv(GEMINI_API_KEY_ENV)

def load_extraction_prompt():
    """Load the extraction prompt template."""
    try:
        with open(PROMPT_TEMPLATE_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt template file '{PROMPT_TEMPLATE_FILE}' not found")
