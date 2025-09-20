from .base_tool import rag_query_tool


def exit_potentials_tool(query: str) -> str:
    """Extract exit strategy and opportunities"""
    enhanced_query = f"""
        EXTRACT EXIT POTENTIALS:
        Find information about: IPO potential, acquisition opportunities, M&A prospects,
        exit pathways, strategic buyers, exit timeline.
        
        Query: {query}
        
        Focus on: exit strategy, potential acquirers, IPO readiness, exit valuation,
        strategic options, investor exit opportunities.
        """
    return rag_query_tool(enhanced_query)
