from .base_tool import rag_query_tool


def traction_tool(query: str) -> str:
    """Extract traction and growth metrics"""
    enhanced_query = f"""
    EXTRACT TRACTION AND GROWTH DATA:
    Find information about: user adoption, growth metrics (ARR, MRR, DAU, MAU),
    month-over-month/year-over-year growth, churn rates, key milestones.
    
    Query: {query}
    
    Focus on: specific growth numbers, user metrics, revenue growth, customer acquisition,
    retention rates, key achievements, milestones reached.
    
    Dont infer any information.

    """
    return rag_query_tool(enhanced_query)
