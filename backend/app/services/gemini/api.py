import time
from typing import Any, Dict

from langchain.output_parsers import PydanticOutputParser
from vertexai.preview.generative_models import GenerativeModel

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


# -----------------------
# Gemini call with fully dynamic parser
# -----------------------
def call_gemini_api(
    model_name: str,
    content: list,
    dynamic_parser: PydanticOutputParser,
    max_retries: int = MAX_RETRIES,
    retry_delay: int = RETRY_DELAY,
) -> Dict[str, Any]:
    """
    Calls the Gemini model with a prompt and text input.
    Parses JSON output dynamically without pre-defined keys.

    Args:
        model_name (str): Gemini model name (e.g., "gemini-2.5-flash-lite")
        prompt (str): Prompt template to guide extraction
        dynamic_parser (PydanticOutputParser): Parser for dynamic JSON
        max_retries (int): Number of retry attempts
        retry_delay (int): Delay between retries (seconds)

    Returns:
        Dict[str, Any]: Parsed JSON output from Gemini, or empty dict on failure
    """
    model = GenerativeModel(model_name)

    for attempt in range(1, max_retries + 1):
        try:
            # Combine prompt and text input
            response = model.generate_content(content)
            raw_output = response.text.strip()
            # Parse dynamically using Pydantic RootModel
            try:
                parsed_output = dynamic_parser.parse(raw_output)
                return parsed_output.model_dump()
            except Exception as parse_err:
                print(f"[Attempt {attempt}] Failed to parse JSON: {parse_err}")
                return {}

        except Exception as call_err:
            print(f"[Attempt {attempt}] Gemini call failed: {call_err}")
            time.sleep(retry_delay)

    # Return empty dict after all retries fail
    return {}
