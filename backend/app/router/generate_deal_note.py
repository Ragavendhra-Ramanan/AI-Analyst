from fastapi import APIRouter
from services.rag_agent.execute_deal_note_agent import generate_full_investment_report
from services.rag_agent.rag_config.rag_registry import rag_registry
from generate_deal_note_pdf import create_investment_memo_pdf
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/generate_memo/")
async def generate_deal_note():
    company_name = rag_registry.get("company_name")
    response = await generate_full_investment_report(company_name)
    pdf_buffer = await create_investment_memo_pdf(
        markdown_content=response["comprehensive_analysis"],
        company_name=company_name,
    )
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename={company_name}_deal_note.pdf"
        },
    )
