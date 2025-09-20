import asyncio
from typing import Any, Dict
import time
from .deal_note_agent import create_comprehensive_agent


async def analyze_comprehensive(query: str) -> Dict[str, Any]:
    """Run comprehensive 12-section investment analysis"""
    try:
        print("Starting comprehensive 12-section analysis...")
        print(f"Query: {query}")
        agent_executor = await asyncio.to_thread(create_comprehensive_agent)
        start_time = time.time()
        result = await agent_executor.acall({"input": query})
        execution_time = time.time() - start_time

        # Format results
        analysis_result = {
            "query": query,
            "comprehensive_analysis": result.get("output", "No analysis generated"),
            "execution_time": round(execution_time, 2),
            "tools_used": len(result.get("intermediate_steps", [])),
            "sections_analyzed": [],
            "tool_breakdown": {},
        }

        # Analyze which tools were used
        if "intermediate_steps" in result:
            tools_used = {}
            for action, observation in result["intermediate_steps"]:
                tool_name = action.tool
                if tool_name not in tools_used:
                    tools_used[tool_name] = 0
                    analysis_result["sections_analyzed"].append(tool_name)
                tools_used[tool_name] += 1

            analysis_result["tool_breakdown"] = tools_used

        return analysis_result

    except Exception as e:
        return {
            "query": query,
            "error": f"Comprehensive analysis failed: {str(e)}",
            "comprehensive_analysis": None,
        }
