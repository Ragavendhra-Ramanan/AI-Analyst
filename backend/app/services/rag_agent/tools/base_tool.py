from vertexai.preview import rag
from ..rag_config.rag_registry import rag_registry


def rag_query_tool(self, query: str) -> str:
    """Enhanced RAG query tool"""
    try:
        print(f"Querying RAG corpus: {query[:100]}...")
        corpus_name = rag_registry.get("corpus_name")
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
            text=query,
            rag_retrieval_config=rag.RagRetrievalConfig(
                top_k=self.config.top_k,
                filter=rag.Filter(
                    vector_similarity_threshold=self.config.similarity_threshold
                ),
                hybrid_search=rag.HybridSearch(alpha=0.9),
            ),
        )

        texts = []
        if hasattr(response, "contexts") and response.contexts:
            contexts = (
                response.contexts.contexts
                if hasattr(response.contexts, "contexts")
                else response.contexts
            )
            for i, ctx in enumerate(contexts, 1):
                text_content = ""
                if hasattr(ctx, "chunk") and ctx.chunk and hasattr(ctx.chunk, "text"):
                    text_content = ctx.chunk.text
                elif hasattr(ctx, "text"):
                    text_content = ctx.text
                if text_content:
                    texts.append(f"[Source {i}]: {text_content}")

        return "\n\n".join(texts) if texts else ""

    except Exception as e:
        print(f"RAG query error: {str(e)}")
        return ""
