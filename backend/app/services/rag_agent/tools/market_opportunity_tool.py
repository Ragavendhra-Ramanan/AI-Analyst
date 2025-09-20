from .base_tool import rag_query_tool


def market_opportunity_tool(query: str) -> str:
    """Extract market size and opportunity data"""
    enhanced_query = f"""
        EXTRACT MARKET OPPORTUNITY DATA:
        Find information about: market size (TAM/SAM/SOM), market trends, growth rates,
        target users, market segments, addressable market, competitors.
        
        Query: {query}
        
        Focus on: specific market size numbers, growth percentages, target market definition,
        competitive landscape, market trends.
        
        Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
