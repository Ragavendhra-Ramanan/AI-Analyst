from vertexai.preview import rag


async def upload_to_rag_corpus(display_name, file_name):
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-005"
        )
    )

    rag_corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    app_name = file_name.split(".")[0]
    await rag.import_files_async(
        corpus_name=rag_corpus.name,
        paths=[f"gs://pitch_info_bucket/{app_name}/{file_name}"],
    )
    print(f"Uploaded to gs://pitch_info_bucket/{app_name}/{file_name} rag corpus")
    return rag_corpus.name
