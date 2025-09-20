from prompts.comprehensive_deal_note_prompt import COMPREHENSIVE_DEAL_NOTE_PROMPT
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from .rag_config.rag_models_config import rag_model_config
from .tools.team_overview_tool import team_overview_tool
from .tools.problem_statement_tool import problem_statement_tool
from .tools.problem_solution_tool import solution_tool
from .tools.business_model_tool import business_model_tool
from .tools.differentiation_tool import differentiation_tool
from .tools.market_opportunity_tool import market_opportunity_tool
from .tools.market_strategy_tool import gtm_strategy_tool
from .tools.traction_tool import traction_tool
from .tools.product_architecture_tool import product_architecture_tool
from .tools.risk_mitigation_tool import risks_mitigations_tool
from .tools.exit_potential_tool import exit_potentials_tool
from .tools.funding_details_tool import funding_details_tool
from .rag_config.rag_llm import llm


def create_comprehensive_agent():
    """Create the comprehensive agent with all 12 specialized tools"""

    # Define all 12 specialized tools
    tools = [
        Tool(
            name="Team_Overview",
            func=team_overview_tool,
            description="Extract team and leadership information: founders, team bios, roles, skills, education, experience, team composition, advisory board.",
        ),
        Tool(
            name="Problem_Statement",
            func=problem_statement_tool,
            description="Extract problem statement: specific problems addressed, market pain points, customer challenges, unmet needs.",
        ),
        Tool(
            name="Solution",
            func=solution_tool,
            description="Extract solution information: product features, value proposition, how it addresses problems, capabilities, benefits.",
        ),
        Tool(
            name="Differentiation",
            func=differentiation_tool,
            description="Extract competitive differentiation: unique selling points, IP, competitive edge, barriers to entry, moats.",
        ),
        Tool(
            name="Market_Opportunity",
            func=market_opportunity_tool,
            description="Extract market opportunity: market size (TAM/SAM/SOM), trends, growth rates, target users, competitors.",
        ),
        Tool(
            name="Business_Model",
            func=business_model_tool,
            description="Extract business model: revenue sources, pricing, revenue metrics, unit economics, monetization strategy.",
        ),
        Tool(
            name="Traction",
            func=traction_tool,
            description="Extract traction data: adoption, growth (ARR, MRR, DAU, MAU), MoM/YoY growth, churn, milestones.",
        ),
        Tool(
            name="Product_Architecture",
            func=product_architecture_tool,
            description="Extract technical architecture: tech stack, operational infrastructure, system architecture, integrations.",
        ),
        Tool(
            name="GTM_Strategy",
            func=gtm_strategy_tool,
            description="Extract go-to-market strategy: sales channels, marketing, partnerships, customer acquisition strategy.",
        ),
        Tool(
            name="Funding_Details",
            func=funding_details_tool,
            description="Extract funding information: stage, amount raised, investors, cap table, runway, use of funds.",
        ),
        Tool(
            name="Risks_Mitigations",
            func=risks_mitigations_tool,
            description="Extract risk analysis: identified risks (market, tech, regulatory, execution) and mitigation plans.",
        ),
        Tool(
            name="Exit_Potentials",
            func=exit_potentials_tool,
            description="Extract exit strategy: IPO potential, acquisition opportunities, M&A prospects, exit pathways.",
        ),
    ]

    # Create comprehensive prompt template with fixed ReAct format
    prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
        template=COMPREHENSIVE_DEAL_NOTE_PROMPT,
    )

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        max_iterations=rag_model_config.max_iterations,
        handle_parsing_errors=True,
    )
    return agent_executor
