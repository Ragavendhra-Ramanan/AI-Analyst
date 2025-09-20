from .base_tool import rag_query_tool


def risks_mitigations_tool(query: str) -> str:
    """Extract risk analysis and mitigation strategies"""
    enhanced_query = f"""
        EXTRACT RISKS AND MITIGATIONS:
        Find information about: identified risks (market, technical, regulatory, execution),
        risk mitigation plans, challenges, potential obstacles.
        
        Query: {query}
        
        Focus on: specific risks identified, mitigation strategies, challenge analysis,
        risk management approach, contingency plans.
        Dont infer any information.
        """
    return rag_query_tool(enhanced_query)
