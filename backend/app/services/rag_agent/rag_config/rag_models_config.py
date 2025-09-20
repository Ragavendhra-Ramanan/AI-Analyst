from dataclasses import dataclass


@dataclass
class InvestmentAnalysisConfig:
    """Configuration for investment analysis"""

    model_name: str = "gemini-2.5-flash"
    temperature: float = 1
    top_k: int = 8
    hybrid_alpha = 1
    similarity_threshold: float = 0.6
    max_iterations: int = 50


rag_model_config = InvestmentAnalysisConfig()
