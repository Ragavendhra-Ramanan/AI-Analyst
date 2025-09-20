from .base_tool import rag_query_tool


def problem_statement_tool(query: str) -> str:
    """Extract problem statement and market pain points"""
    enhanced_query = f"""
        EXTRACT PROBLEM STATEMENT:
        Find information about: the specific problem being addressed, market pain points,
        customer challenges, unmet needs, current solutions' limitations.
        
        Query: {query}
        
        Focus on: problem definition, market gaps, customer frustrations, existing solution 
        inadequacies, pain point quantification.

        Dont infer any information.
        """
    return rag_query_tool(enhanced_query)
