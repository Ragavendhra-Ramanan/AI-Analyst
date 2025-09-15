import asyncio
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from typing import Dict, Any


async def create_deal_note_async(data: Dict[str, Any]) -> BytesIO:
    """
    Generate a PDF from structured JSON asynchronously using a thread.
    Returns a BytesIO object containing the PDF.
    """
    buffer = BytesIO()

    def build_pdf():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )
        styles = getSampleStyleSheet()
        story = []

        section_header = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading1"],
            spaceAfter=10,
            textColor=colors.HexColor("#003366"),
        )
        bullet_style = ParagraphStyle(
            "Bullet",
            parent=styles["Normal"],
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4,
        )

        def add_section(title, content):
            story.append(Paragraph(title, section_header))
            story.append(Spacer(1, 6))

            if title == "Financials" and isinstance(content, dict):
                table_data = [[k, str(v)] for k, v in content.items()]
                table = Table(table_data, colWidths=[120, 350])
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 12))
                return

            if title == "Founders" and isinstance(content, dict):
                table_data = [["Name", "Role", "Background"]]
                for member in content.get("Team", []):
                    table_data.append(
                        [
                            member.get("Name", ""),
                            member.get("Role", ""),
                            member.get("Background", ""),
                        ]
                    )
                table = Table(table_data, colWidths=[120, 100, 350])
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 12))
                return

            if isinstance(content, dict):
                for k, v in content.items():
                    if isinstance(v, list):
                        story.append(Paragraph(f"<b>{k}:</b>", styles["Normal"]))
                        for item in v:
                            story.append(Paragraph(f"• {item}", bullet_style))
                    else:
                        story.append(Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]))
                    story.append(Spacer(1, 4))
            elif isinstance(content, list):
                for item in content:
                    story.append(Paragraph(f"• {item}", bullet_style))
            else:
                story.append(Paragraph(str(content), styles["Normal"]))

            story.append(Spacer(1, 12))

        for section, section_data in data.items():
            add_section(section, section_data)

        doc.build(story)
        buffer.seek(0)

    await asyncio.to_thread(build_pdf)
    return buffer
