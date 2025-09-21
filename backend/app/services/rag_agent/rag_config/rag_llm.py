from langchain_google_vertexai import VertexAI
from .rag_models_config import rag_model_config
from ....constants import PROJECT_ID


llm = VertexAI(
    model_name=rag_model_config.model_name,
    project=PROJECT_ID,
    temperature=rag_model_config.temperature,
)
