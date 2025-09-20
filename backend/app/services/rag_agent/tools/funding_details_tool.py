from .base_tool import rag_query_tool


def funding_details_tool(query: str) -> str:
    """Extract funding and financial information"""
    enhanced_query = f"""
        EXTRACT FUNDING DETAILS:
        Find information about: funding stage, amount raised, investors, cap table,
        runway, use of funds, valuation, investment rounds.
        
        Query: {query}
        
        Focus on: specific funding amounts, investor names, valuation figures, funding rounds,
        use of capital, runway duration, equity structure.
        Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
