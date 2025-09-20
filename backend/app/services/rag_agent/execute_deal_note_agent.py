from typing import Any, Dict
from .deal_note_agent_analyser import analyze_comprehensive


async def generate_full_investment_report(
    company_name: str = "Target Company",
) -> Dict[str, Any]:
    """Generate complete investment report covering all 12 sections"""

    comprehensive_query = f"""
        Generate a complete investment analysis report for {company_name} covering all 12 critical areas:
        
        1. Team Overview - Leadership team, founders, co-founders, experience, skills
        2. Problem Statement - Market problems being addressed
        3. Solution - Product/service solution and value proposition  
        4. Differentiation - Competitive advantages and unique factors
        5. Market Opportunity - Market size, growth, and opportunity
        6. Business Model - Revenue streams and monetization
        7. Traction - Growth metrics, adoption, milestones
        8. Product Architecture - Technology and infrastructure
        9. Go-to-Market Strategy - Sales and marketing approach
        10. Funding Details - Investment rounds and financial status
        11. Risks & Mitigations - Risk analysis and mitigation plans
        12. Exit Potentials - Exit opportunities and strategic options
        
        Provide comprehensive analysis with specific details, metrics, and insights for each section.
        """
    return await analyze_comprehensive(comprehensive_query)
