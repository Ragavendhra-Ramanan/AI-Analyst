from .base_tool import rag_query_tool


def team_overview_tool(query: str) -> str:
    """Extract team and leadership information"""
    enhanced_query = f"""
    EXTRACT TEAM OVERVIEW INFORMATION:
    Find details about: founders, co-founders, team members, leadership bios, roles, skills, education, 
    work experience, team composition, advisory board, key personnel.
    
    Query: {query}
    
    Focus on: names, positions, backgrounds, education credentials, previous company experience,
    years of experience, team size, organizational structure.
    
    """
    return rag_query_tool(enhanced_query)
