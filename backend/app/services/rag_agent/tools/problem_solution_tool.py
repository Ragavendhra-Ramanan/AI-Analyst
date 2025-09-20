from .base_tool import rag_query_tool


def solution_tool(query: str) -> str:
    """Extract solution and product information"""
    enhanced_query = f"""
        EXTRACT SOLUTION INFORMATION:
        Find details about: the startup's solution, product features, value proposition,
        how it addresses the problem, product capabilities, user benefits.
        
        Query: {query}
        
        Focus on: product description, key features, value proposition, solution benefits,
        how it solves the problem, product functionality.
        
        Dont infer any information.
        """
    return rag_query_tool(enhanced_query)
