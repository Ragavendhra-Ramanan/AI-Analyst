import re
from typing import List, Dict
from datetime import datetime
import asyncio


async def chunk_markdown_slides(
    md_slides: List[str],
    min_chunk_size: int = 150,
    max_chunk_size: int = 400,
    overlap: int = 40,
    doc_id: str = "buffer",
    source_type: str = "markdown",
) -> List[Dict]:
    """
    Process a list of markdown slides, chunk them into ~200-400 word segments,
    and add metadata including slide_number.
    - section_path_full = main heading only
    - tags = subheadings only (no duplicates)
    - id: "chunk-<number>"
    - embedding_model removed
    """
    all_chunks = []
    chunk_counter = 0

    for slide_idx, md_text in enumerate(md_slides, start=1):  # slide_number starts at 1
        sections = await asyncio.to_thread(_split_by_headings, md_text)

        for section in sections:
            if not section["content"].strip():
                continue

            words = section["content"].split()

            # Main title = first element in path
            section_title = section["path"][0] if section["path"] else "Untitled"

            # Tags = remaining subheadings (deduplicated)
            tags = list(dict.fromkeys(section["path"][1:]))

            # 🔹 Merge short sections with previous chunk
            if (
                len(words) < min_chunk_size
                and all_chunks
                and all_chunks[-1]["metadata"]["slide_number"] == slide_idx
            ):
                all_chunks[-1]["text"] += "\n\n" + section["content"].strip()
                all_chunks[-1]["metadata"]["word_count"] += len(words)

                old_tags = set(all_chunks[-1]["metadata"]["tags"])
                all_chunks[-1]["metadata"]["tags"] = list(old_tags.union(tags))
                # id stays same for previous chunk
                continue

            # 🔹 Split long sections into multiple overlapping chunks
            if len(words) > max_chunk_size:
                sub_chunks = await asyncio.to_thread(
                    _split_text, words, max_chunk_size, overlap
                )
                for j, sub in enumerate(sub_chunks):
                    text = " ".join(sub)
                    all_chunks.append(
                        {
                            "text": text,
                            "id": f"chunk_{chunk_counter}",
                            "metadata": {
                                "doc_id": doc_id,
                                "source_type": source_type,
                                "chunk_index": chunk_counter,
                                "word_count": len(sub),
                                "section_path_full": section_title,  # only main heading
                                "tags": tags,  # only subheadings
                                "timestamp": datetime.utcnow().isoformat() + "Z",
                                "slide_number": slide_idx,
                            },
                        }
                    )
                    chunk_counter += 1
            else:
                all_chunks.append(
                    {
                        "id": f"chunk_{chunk_counter}",
                        "text": section["content"].strip(),
                        "metadata": {
                            "doc_id": doc_id,
                            "source_type": source_type,
                            "chunk_index": chunk_counter,
                            "word_count": len(words),
                            "section_path_full": section_title,
                            "tags": tags,
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "slide_number": slide_idx,
                        },
                    }
                )
                chunk_counter += 1
    print(len(all_chunks), "total chunks")
    return all_chunks


def _split_by_headings(text: str) -> List[Dict]:
    """Parse markdown into sections based on headings (#, ##, ###)."""
    pattern = re.compile(r"^(#{1,3})\s+(.*)", re.MULTILINE)
    matches = list(pattern.finditer(text))

    sections = []
    current_path = []

    for i, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()

        # Update path by heading level
        current_path = current_path[: level - 1] + [heading]

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        sections.append({"path": current_path.copy(), "content": content})

    return sections


def _split_text(words: List[str], max_words: int, overlap: int) -> List[List[str]]:
    """Split text into overlapping word chunks."""
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(words[start:end])
        if end == len(words):
            break
        start = end - overlap
    return chunks
