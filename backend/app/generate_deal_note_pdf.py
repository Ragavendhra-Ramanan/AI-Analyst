import asyncio
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


def _parse_formatting(text):
    """
    Parse markdown-style formatting and convert to ReportLab HTML tags

    Args:
        text (str): Text to format

    Returns:
        str: Text with ReportLab HTML formatting
    """
    # Convert bold: **text** or __text__ to <b>text</b>
    text = re.sub(
        r"\*\*(.*?)\*\*|__(.*?)__", lambda m: f"<b>{m.group(1) or m.group(2)}</b>", text
    )

    # Convert italic: *text* or _text_ to <i>text</i>
    text = re.sub(
        r"\*(.*?)\*|_(.*?)_(?![_\*])",
        lambda m: f"<i>{m.group(1) or m.group(2)}</i>",
        text,
    )

    # Convert links: [text](url) to <a href="url">text</a>
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)

    return text


async def create_investment_memo_pdf(
    markdown_content: str, company_name: str
) -> BytesIO:
    """
    Convert Markdown content to a professionally styled investment memo PDF with company name featured on the first page.

    Args:
        markdown_content (str): The markdown content to convert
        company_name (str): Company name to display on the first page

    Returns:
        BytesIO: A buffer containing the PDF data
    """
    buffer = BytesIO()

    def build_pdf():
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        # Define styles
        styles = getSampleStyleSheet()

        # Custom styles for professional investment memo
        title_style = ParagraphStyle(
            "Title",
            parent=styles["Title"],
            fontSize=28,  # Larger font for impact
            alignment=1,  # Center alignment
            spaceAfter=20,
            textColor=colors.HexColor("#003366"),  # Deep blue for professional look
            fontName="Helvetica-Bold",
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=16,
            alignment=1,  # Center alignment
            spaceAfter=40,  # More space after subtitle
            textColor=colors.HexColor("#666666"),
            fontStyle="italic",
            fontName="Helvetica",
        )

        section_header = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading1"],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,  # Add space before each section
            textColor=colors.HexColor("#003366"),
            borderWidth=0,
            borderRadius=0,
            borderPadding=0,
            borderColor=colors.HexColor("#CCCCCC"),
            borderBottomWidth=1,
            borderBottomPadding=6,
            fontName="Helvetica-Bold",
            leading=18,  # Increased line height for headers
        )

        subsection_header = ParagraphStyle(
            "SubSectionHeader",
            parent=styles["Heading2"],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor("#004477"),
            fontName="Helvetica-Bold",
            leading=16,
        )

        normal_style = ParagraphStyle(
            "NormalText",
            parent=styles["Normal"],
            fontSize=11,  # Professional font size
            spaceAfter=8,
            leading=16,  # Better line height
            fontName="Helvetica",
            textColor=colors.HexColor("#333333"),  # Slightly softer than black
        )

        bullet_style = ParagraphStyle(
            "BulletPoint",
            parent=styles["Normal"],
            fontSize=11,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4,
            leading=16,
            fontName="Helvetica",
            textColor=colors.HexColor("#333333"),
        )

        # Style for key metrics and numbers
        metric_style = ParagraphStyle(
            "MetricText",
            parent=styles["Normal"],
            fontSize=11,
            spaceAfter=6,
            leading=16,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#003366"),  # Highlight important numbers
        )

        # Start with content for the first page
        story = []

        # Create a professional cover page with vertical centering
        story.append(Spacer(1, 180))  # Push content down for centering

        # Add company name as title
        story.append(Paragraph(f"{company_name}", title_style))
        story.append(Spacer(1, 15))

        # Add "Investment Memo" subtitle
        story.append(Paragraph("Investment Memo", subtitle_style))
        story.append(Spacer(1, 30))

        # Add date
        current_date = datetime.now().strftime("%B %d, %Y")
        date_style = ParagraphStyle(
            "DateStyle",
            parent=styles["Normal"],
            fontSize=12,
            alignment=1,
            textColor=colors.HexColor("#666666"),
        )
        story.append(Paragraph(f"Generated on {current_date}", date_style))

        # Add confidentiality notice at bottom of first page
        story.append(Spacer(1, 120))
        confidential_style = ParagraphStyle(
            "Confidential",
            parent=styles["Normal"],
            fontSize=9,
            alignment=1,
            textColor=colors.HexColor("#999999"),
            fontStyle="italic",
        )
        story.append(Paragraph("CONFIDENTIAL", confidential_style))
        story.append(
            Paragraph(
                "For internal investment review purposes only", confidential_style
            )
        )

        # Add page break after cover page
        story.append(PageBreak())

        # Process markdown content
        # Split into sections based on headers
        sections = re.split(r"(?m)^##\s+(.*?)$", markdown_content)

        # First part is content before any sections
        intro = sections.pop(0).strip()
        if intro:
            for line in intro.split("\n"):
                if line.startswith("# "):
                    # Skip the title as we've already included it
                    continue
                story.append(Paragraph(line, normal_style))
                story.append(Spacer(1, 6))

        # Process each section
        for i in range(0, len(sections), 2):
            if i + 1 < len(sections):
                section_title = sections[i].strip()
                section_content = sections[i + 1].strip()

                # Add section title
                story.append(Paragraph(section_title, section_header))
                story.append(Spacer(1, 10))

                # Process subsections
                subsections = re.split(r"(?m)^###\s+(.*?)$", section_content)
                main_content = subsections.pop(0).strip()

                # Process main content of the section line by line
                for line in main_content.split("\n"):
                    if line.strip():
                        # Convert bullets
                        if line.strip().startswith("- ") or line.strip().startswith(
                            "* "
                        ):
                            bullet_text = line.strip()[2:]
                            # Handle bold and italic in bullet points
                            bullet_text = _parse_formatting(bullet_text)
                            story.append(Paragraph(f"• {bullet_text}", bullet_style))
                        else:
                            # Handle bold, italic, and other formatting
                            formatted_line = _parse_formatting(line)
                            story.append(Paragraph(formatted_line, normal_style))

                # Process subsections
                for j in range(0, len(subsections), 2):
                    if j + 1 < len(subsections):
                        subsection_title = subsections[j].strip()
                        subsection_content = subsections[j + 1].strip()

                        story.append(Spacer(1, 10))
                        story.append(Paragraph(subsection_title, subsection_header))
                        story.append(Spacer(1, 6))

                        for line in subsection_content.split("\n"):
                            if line.strip():
                                # Convert bullets
                                if line.strip().startswith(
                                    "- "
                                ) or line.strip().startswith("* "):
                                    bullet_text = line.strip()[2:]
                                    # Handle bold and italic in bullet points
                                    bullet_text = _parse_formatting(bullet_text)
                                    story.append(
                                        Paragraph(f"• {bullet_text}", bullet_style)
                                    )
                                else:
                                    # Handle bold, italic, and other formatting
                                    formatted_line = _parse_formatting(line)
                                    story.append(
                                        Paragraph(formatted_line, normal_style)
                                    )

                # Add space after section
                story.append(Spacer(1, 20))

        # Build the PDF
        doc.build(story)
        buffer.seek(0)

    # Run PDF building in a separate thread
    await asyncio.to_thread(build_pdf)
    return buffer
