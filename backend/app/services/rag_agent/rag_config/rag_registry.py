from typing import Dict


class RagCorpusRegistry:
    """Registry to manage RAG corpus names per session or file."""

    def __init__(self):
        self._registry: Dict[str, str] = {}

    def set(self, key: str, corpus_name: str):
        self._registry[key] = corpus_name

    def get(self, key: str) -> str:
        if key not in self._registry:
            raise RuntimeError(f"No RAG corpus registered for key: {key}")
        return self._registry[key]


rag_registry = RagCorpusRegistry()
