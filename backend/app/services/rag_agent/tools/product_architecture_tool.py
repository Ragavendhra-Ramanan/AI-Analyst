from .base_tool import rag_query_tool


def product_architecture_tool(query: str) -> str:
    """Extract technical and operational architecture"""
    enhanced_query = f"""
        EXTRACT PRODUCT ARCHITECTURE:
        Find information about: technology stack, operational infrastructure, system architecture,
        integrations, technical capabilities, platform details.
        
        Query: {query}
        
        Focus on: technical stack, infrastructure, system design, integrations, scalability,
        technical specifications, operational setup.
        
        Dont infer any information.

        """
    return rag_query_tool(enhanced_query)
