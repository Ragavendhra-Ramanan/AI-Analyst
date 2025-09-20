"""PDF report generation functions."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import sys
sys.path.append('/Users/pragathi.vetrivelmurugan/AI-Analyst/backend/app')
from utils.helpers import format_currency


class PDFReportGenerator:
    """Generator for PDF benchmark reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkred,
            borderWidth=1,
            borderColor=colors.darkred,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyOverview',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=TA_JUSTIFY
        ))
    
    def create_benchmark_report(self, target_data, insights, chart_paths, output_path):
        """Create comprehensive benchmark PDF report."""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            story = []
            
            # Add company overview front page
            self.add_company_overview_to_story(story, target_data)
            
            # Add page break after overview
            story.append(PageBreak())
            
            # Title page
            company_name = target_data.get('company_overview', {}).get('name', 'Target Company')
            story.append(Paragraph(f"{company_name} Benchmark Analysis", self.styles['CustomTitle']))
            story.append(Spacer(1, 0.5*inch))
            
            # Date
            date_str = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(f"Report Generated: {date_str}", self.styles['Normal']))
            story.append(Spacer(1, 0.5*inch))
            
            # Executive summary
            story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
            
            if insights.get('insights'):
                for insight in insights['insights']:
                    story.append(Paragraph(f"• {insight}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Key recommendations
            if insights.get('recommendations'):
                story.append(Paragraph("Key Recommendations", self.styles['SectionHeader']))
                for rec in insights['recommendations']:
                    story.append(Paragraph(f"• {rec}", self.styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
            
            # Competitive position
            if insights.get('competitive_position'):
                story.append(Paragraph("Competitive Position", self.styles['SectionHeader']))
                story.append(Paragraph(insights['competitive_position'], self.styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
            
            # Add charts
            story.append(Paragraph("Performance Analysis", self.styles['SectionHeader']))
            
            for chart_name, chart_path in chart_paths.items():
                if os.path.exists(chart_path):
                    try:
                        # Add chart title
                        chart_title = chart_name.replace('_', ' ').title()
                        story.append(Paragraph(chart_title, self.styles['Heading3']))
                        story.append(Spacer(1, 0.1*inch))
                        
                        # Add chart image
                        img = Image(chart_path, width=6*inch, height=4*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.3*inch))
                    except Exception as e:
                        print(f"Error adding chart {chart_name}: {e}")
                        continue
            
            # Add AI-generated competitive summary
            self.add_ai_competitive_summary_to_story(story, insights)
            
            # Add fundraise analysis
            self.add_fundraise_analysis_to_story(story, target_data)
            
            # Add traction comparison
            self.add_traction_comparison_to_story(story, target_data)
            
            # Build PDF
            doc.build(story)
            print(f"Benchmark report created: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error creating benchmark report: {e}")
            return False
    
    def add_company_overview_to_story(self, story, target_data):
        """Add company overview section to PDF story."""
        try:
            company_overview = target_data.get('company_overview', {})
            
            if not company_overview:
                return
            
            # Company name as title
            company_name = company_overview.get('name', 'Company Name Not Available')
            story.append(Paragraph(company_name, self.styles['CustomTitle']))
            story.append(Spacer(1, 0.3*inch))
            
            # Basic information table
            basic_info = [
                ['Sector', ' > '.join(company_overview.get('sector_hierarchy', ['Not Available']))],
                ['Stage', company_overview.get('stage', 'Not Available')],
                ['Founded', str(company_overview.get('founding_year', 'Not Available'))],
                ['Location', company_overview.get('location', 'Not Available')]
            ]
            
            info_table = Table(basic_info, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Company description
            description = company_overview.get('description', '')
            if description:
                story.append(Paragraph("Company Description", self.styles['SectionHeader']))
                story.append(Paragraph(description, self.styles['CompanyOverview']))
                story.append(Spacer(1, 0.2*inch))
            
            # Business model
            business_model = company_overview.get('business_model', '')
            if business_model:
                story.append(Paragraph("Business Model", self.styles['SectionHeader']))
                story.append(Paragraph(business_model, self.styles['CompanyOverview']))
                story.append(Spacer(1, 0.2*inch))
            
            # Key metrics summary
            financials = target_data.get('financials', {})
            if financials:
                story.append(Paragraph("Key Financial Metrics", self.styles['SectionHeader']))
                
                financial_data = []
                
                # Revenue
                revenue = financials.get('revenue', {})
                if revenue and revenue.get('amount'):
                    financial_data.append(['Revenue', format_currency(revenue.get('amount', 0))])
                
                # CAC
                cac = financials.get('cac', {})
                if cac and cac.get('amount'):
                    financial_data.append(['Customer Acquisition Cost', format_currency(cac.get('amount', 0))])
                
                # AOV
                aov = financials.get('aov', {})
                if aov and aov.get('amount'):
                    financial_data.append(['Average Order Value', format_currency(aov.get('amount', 0))])
                
                # Gross Margin
                gross_margin = financials.get('gross_margin_pct')
                if gross_margin:
                    financial_data.append(['Gross Margin', f"{gross_margin}%"])
                
                if financial_data:
                    financial_table = Table(financial_data, colWidths=[3*inch, 2*inch])
                    financial_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 11),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(financial_table)
                    story.append(Spacer(1, 0.2*inch))
            
        except Exception as e:
            print(f"Error adding company overview: {e}")
    
    def add_fundraise_analysis_to_story(self, story, target_data):
        """Add fundraise analysis section to PDF story."""
        try:
            fundraise_data = target_data.get('fundraise', {})
            
            if not fundraise_data:
                return
            
            story.append(Paragraph("Fundraise Analysis", self.styles['SectionHeader']))
            
            # Current round information
            round_info = fundraise_data.get('round', 'Not specified')
            story.append(Paragraph(f"Current Round: {round_info}", self.styles['Normal']))
            
            # Amount raised
            amount_raised = fundraise_data.get('amount_raised', {})
            if amount_raised and amount_raised.get('amount'):
                amount_text = format_currency(amount_raised.get('amount', 0))
                currency = amount_raised.get('currency', 'INR')
                story.append(Paragraph(f"Amount Raised: {amount_text} {currency}", self.styles['Normal']))
            
            # Valuation
            post_money = fundraise_data.get('post_money_valuation', {})
            if post_money and post_money.get('amount'):
                valuation_text = format_currency(post_money.get('amount', 0))
                currency = post_money.get('currency', 'INR')
                story.append(Paragraph(f"Post-Money Valuation: {valuation_text} {currency}", self.styles['Normal']))
            
            # Lead investors
            lead_investors = fundraise_data.get('lead_investors', [])
            if lead_investors:
                investors_text = ', '.join(lead_investors[:3])  # Show first 3
                if len(lead_investors) > 3:
                    investors_text += f" and {len(lead_investors) - 3} others"
                story.append(Paragraph(f"Lead Investors: {investors_text}", self.styles['Normal']))
            
            story.append(Spacer(1, 0.3*inch))
            
        except Exception as e:
            print(f"Error adding fundraise analysis: {e}")
    
    def add_traction_comparison_to_story(self, story, target_data):
        """Add traction comparison section to PDF story."""
        try:
            traction_data = target_data.get('traction', {})
            
            if not traction_data:
                return
            
            story.append(Paragraph("Traction Metrics", self.styles['SectionHeader']))
            
            traction_table_data = []
            
            # Orders fulfilled
            orders = traction_data.get('orders_fulfilled_total')
            if orders:
                traction_table_data.append(['Total Orders Fulfilled', f"{orders:,}"])
            
            # Repeat rate
            repeat_rate = traction_data.get('repeat_rate_pct')
            if repeat_rate:
                traction_table_data.append(['Customer Repeat Rate', f"{repeat_rate}%"])
            
            # Monthly active users
            mau = traction_data.get('monthly_active_users')
            if mau:
                traction_table_data.append(['Monthly Active Users', f"{mau:,}"])
            
            # App downloads
            downloads = traction_data.get('app_downloads_total')
            if downloads:
                traction_table_data.append(['Total App Downloads', f"{downloads:,}"])
            
            if traction_table_data:
                traction_table = Table(traction_table_data, colWidths=[3*inch, 2*inch])
                traction_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightgreen),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(traction_table)
                story.append(Spacer(1, 0.3*inch))
            
        except Exception as e:
            print(f"Error adding traction comparison: {e}")
    
    def add_ai_competitive_summary_to_story(self, story, insights):
        """Add AI-generated competitive summary section to PDF story."""
        try:
            ai_summary = insights.get('ai_summary')
            
            if not ai_summary:
                return
            
            # Add page break before summary for better formatting
            story.append(PageBreak())
            
            # Add section header
            story.append(Paragraph("AI-Powered Competitive Analysis", self.styles['CustomTitle']))
            story.append(Spacer(1, 0.3*inch))
            
            # Process the AI summary text
            # Split by common section headers and format appropriately
            sections = self._parse_ai_summary(ai_summary)
            
            for section_title, section_content in sections.items():
                if section_content.strip():
                    # Add section header
                    story.append(Paragraph(section_title, self.styles['SectionHeader']))
                    story.append(Spacer(1, 0.1*inch))
                    
                    # Split content into paragraphs and bullet points
                    lines = section_content.strip().split('\n')
                    current_paragraph = []
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                            # Flush current paragraph if any
                            if current_paragraph:
                                story.append(Paragraph(' '.join(current_paragraph), self.styles['Normal']))
                                current_paragraph = []
                            
                            # Add bullet point
                            clean_line = line.lstrip('•-*').strip()
                            story.append(Paragraph(f"• {clean_line}", self.styles['Normal']))
                        else:
                            current_paragraph.append(line)
                    
                    # Flush remaining paragraph
                    if current_paragraph:
                        story.append(Paragraph(' '.join(current_paragraph), self.styles['Normal']))
                    
                    story.append(Spacer(1, 0.2*inch))
            
        except Exception as e:
            print(f"Error adding AI competitive summary: {e}")
    
    def _parse_ai_summary(self, ai_summary):
        """Parse AI summary into sections."""
        sections = {}
        current_section = None
        current_content = []
        
        lines = ai_summary.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check if this is a section header (starts with ## or is in ALL CAPS)
            if (line.startswith('##') or 
                (len(line) > 10 and line.isupper() and 
                 any(keyword in line for keyword in ['ADVANTAGE', 'DISADVANTAGE', 'RECOMMENDATION', 'PERSPECTIVE', 'ANALYSIS']))):
                
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            elif current_section and line:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        # If no sections found, treat entire content as one section
        if not sections and ai_summary.strip():
            sections['Competitive Analysis Summary'] = ai_summary.strip()
        
        return sections


# Global instance
pdf_report_generator = PDFReportGenerator()
