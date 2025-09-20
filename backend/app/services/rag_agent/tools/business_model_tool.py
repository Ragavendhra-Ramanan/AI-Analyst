from .base_tool import rag_query_tool


def business_model_tool(query: str) -> str:
    """Extract business model and revenue information"""
    enhanced_query = f"""
        EXTRACT BUSINESS MODEL INFORMATION:
        Find details about: revenue sources, pricing strategy, revenue metrics,
        unit economics, monetization strategy, revenue streams.
        
        Query: {query}
        
        Focus on: revenue model, pricing structure, unit economics, customer acquisition cost,
        lifetime value, revenue streams, monetization approach.
    
         Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
