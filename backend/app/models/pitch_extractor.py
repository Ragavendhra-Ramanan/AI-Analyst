from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field


class PitchExtractor(BaseModel):
    slide_motive: Optional[Union[str, Dict[str, Any]]] = Field(
        default="", description="Purpose of the slide"
    )
    startup_summary: Optional[Union[str, Dict[str, Any]]] = Field(
        default="",
        description="Startup identity details (name, sector, funding, HQ, etc.)",
    )
    founder_team: Optional[Union[str, Dict[str, Any]]] = Field(
        default="", description="Founder/team info (bios, fit, prior ventures, risks)"
    )
    product_info: Optional[Union[str, Dict[str, Any]]] = Field(
        default="", description="Product/solution details"
    )
    market: Optional[Union[str, Dict[str, Any]]] = Field(
        default="",
        description="Market context (problem, TAM/SAM/SOM, competitors, CAGR, MOAT)",
    )
    financials: Optional[Union[str, Dict[str, Any]]] = Field(
        default="",
        description="Financial details (revenue, CAC, LTV, burn, runway, etc.)",
    )
    traction: Optional[Union[str, Dict[str, Any]]] = Field(
        default="", description="Traction metrics (ARR/MRR, DAU/MAU, churn, etc.)"
    )
    custom_topic: Optional[Union[str, Dict[str, Any]]] = Field(
        default="", description="Any extra insights not fitting other categories"
    )
    page_number: Optional[int] = None
