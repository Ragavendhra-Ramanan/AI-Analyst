from collections import defaultdict
from services.gemini_api import call_gemini_api
from prompts.deal_note_prompt import DEAL_NOTE_PROMPT
from models.pitch_refiner import PitchRefiner
from langchain.output_parsers import PydanticOutputParser
import asyncio


def merge_custom_topic(existing, new):
    """
    Merge two custom_topic dictionaries.
    If sub-keys overlap, concatenate values with ' | '.
    """
    for k, v in new.items():
        if v:
            if k in existing:
                existing[k] = f"{existing[k]} | {v}"
            else:
                existing[k] = v
    return existing


async def merge_similar_keys(pdf_data: dict):
    merged_data = {}

    for file_name, pages in pdf_data.items():
        grouped = defaultdict(list)
        custom_topic_merged = {}

        for page in pages:
            for key, value in page.items():
                if key == "page_number":
                    grouped[key].append(value)
                elif key == "custom_topic" and isinstance(value, dict):
                    custom_topic_merged = await asyncio.to_thread(
                        merge_custom_topic, custom_topic_merged, value
                    )
                elif value:  # Only include non-empty values
                    grouped[key].append(value)

        # Flatten string lists
        for k, v in grouped.items():
            if k != "page_number" and all(isinstance(i, str) for i in v):
                grouped[k] = " | ".join(v)

        grouped["custom_topic"] = custom_topic_merged
        merged_data[file_name] = dict(grouped)

    return merged_data


async def refine_pitch_content(raw_json_content: dict):
    merged_content = await merge_similar_keys(raw_json_content)
    prompt = DEAL_NOTE_PROMPT.format(text_to_analyze=merged_content)
    parser = PydanticOutputParser(pydantic_object=PitchRefiner)
    parsed_output = await asyncio.to_thread(
        call_gemini_api,
        model_name="gemini-2.5-flash-lite",
        content=[prompt],
        dynamic_parser=parser,
    )
    return parsed_output
