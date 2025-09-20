from .base_tool import rag_query_tool


def gtm_strategy_tool(query: str) -> str:
    """Extract go-to-market and distribution strategy"""
    enhanced_query = f"""
        EXTRACT GO-TO-MARKET STRATEGY:
        Find information about: sales channels, marketing strategy, partnerships,
        customer acquisition strategy, distribution channels, market entry approach.
        
        Query: {query}
        
        Focus on: sales approach, marketing channels, partnership strategy, customer acquisition,
        distribution methods, market entry plan.
        Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
