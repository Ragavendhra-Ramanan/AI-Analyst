from .base_tool import rag_query_tool


def differentiation_tool(query: str) -> str:
    """Extract competitive differentiation and unique advantages"""
    enhanced_query = f"""
        EXTRACT DIFFERENTIATION FACTORS:
        Find information about: unique selling points, intellectual property, competitive edge,
        barriers to entry, moats, what makes this solution different.
        
        Query: {query}
        
        Focus on: competitive advantages, IP/patents, unique technology, market positioning,
        defensibility, barriers to competition.
        
        Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
