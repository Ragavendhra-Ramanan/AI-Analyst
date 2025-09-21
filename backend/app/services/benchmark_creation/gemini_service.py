"""Gemini AI service for structured data extraction."""

import json
import google.generativeai as genai
from config.gemini_config import gemini_config
from config.settings import load_extraction_prompt


class GeminiService:
    """Gemini AI service for structured data extraction."""
    
    def __init__(self):
        self.configured = False
        self.model = None
        self.prompt_template = None
        # Try to initialize automatically
        self.initialize()
    
    def initialize(self):
        """Initialize the Gemini service."""
        if gemini_config.configure():
            self.configured = True
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.prompt_template = load_extraction_prompt()
                return True
            except Exception as e:
                print(f"Error initializing Gemini model: {e}")
                return False
        return False
    
    def extract_structured_data(self, extracted_text, filename):
        """Extract structured data from text using Gemini."""
        if not self.configured:
            print("Gemini not configured, skipping structured extraction")
            return None
        
        if not self.model or not self.prompt_template:
            if not self.initialize():
                return None
        
        try:
            # Format the prompt with the extracted text
            prompt = self.prompt_template.format(extracted_text=extracted_text)
            
            print("Sending text to Gemini for structured extraction...")
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Clean up the response text
                response_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                # Parse JSON
                structured_data = json.loads(response_text)
                
                # Add metadata
                structured_data['metadata'] = {
                    'source_document_title': filename,
                    'extraction_date': json.loads(json.dumps(structured_data.get('metadata', {}))).get('extraction_date', '2025-09-20'),
                    'raw_text_snippet': extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                }
                
                print("Successfully extracted structured data")
                return structured_data
            else:
                print("No response from Gemini")
                return None
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Gemini response: {e}")
            print(f"Raw response: {response.text if response else 'No response'}")
            return None
        except Exception as e:
            print(f"Error during Gemini extraction: {e}")
            return None
    
    def generate_competitive_summary(self, target_data, competitor_data, insights, benchmarks):
        """Generate AI-powered competitive analysis summary."""
        if not self.configured or not self.model:
            print("Gemini not configured, skipping competitive summary")
            return None
        
        try:
            # Create a comprehensive prompt for competitive analysis
            summary_prompt = self._create_competitive_summary_prompt(target_data, competitor_data, insights, benchmarks)
            
            # Generate summary using Gemini
            response = self.model.generate_content(summary_prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating competitive summary: {e}")
            return None
    
    def _create_competitive_summary_prompt(self, target_data, competitor_data, insights, benchmarks):
        """Create a detailed prompt for competitive analysis."""
        company_name = target_data.get('company_overview', {}).get('name', 'Target Company')
        sector = ' > '.join(target_data.get('company_overview', {}).get('sector_hierarchy', ['Unknown Sector']))
        
        # Extract key metrics
        financials = target_data.get('financials', {})
        revenue = financials.get('revenue', {}).get('amount') if financials.get('revenue') else None
        cac = financials.get('cac', {}).get('amount') if financials.get('cac') else None
        gross_margin = financials.get('gross_margin_pct')
        
        fundraise = target_data.get('fundraise', {})
        valuation = fundraise.get('post_money_valuation', {}).get('amount') if fundraise.get('post_money_valuation') else None
        
        traction = target_data.get('traction', {})
        orders = traction.get('orders_fulfilled_total')
        repeat_rate = traction.get('repeat_rate_pct')
        
        # Create competitor summary
        competitor_count = len(competitor_data)
        competitor_names = [comp.get('data', {}).get('company_overview', {}).get('name', 'Unknown') 
                          for comp in competitor_data[:3] if comp.get('data')]
        
        prompt = f"""
You are an expert investment analyst. Analyze the competitive position of {company_name} against its peers in the {sector} sector.

TARGET COMPANY: {company_name}
SECTOR: {sector}
COMPETITORS ANALYZED: {competitor_count} companies including {', '.join(competitor_names[:3])}

COMPANY METRICS:
- Revenue: {f"Rs{revenue/1e7:.1f}Cr" if revenue else "Not available"}
- Customer Acquisition Cost: {f"Rs{cac:,.0f}" if cac else "Not available"}
- Gross Margin: {f"{gross_margin}%" if gross_margin else "Not available"}
- Valuation: {f"Rs{valuation/1e7:.1f}Cr" if valuation else "Not available"}
- Orders Fulfilled: {f"{orders:,}" if orders else "Not available"}
- Customer Repeat Rate: {f"{repeat_rate}%" if repeat_rate else "Not available"}

COMPETITIVE INSIGHTS:
{chr(10).join(f"• {insight}" for insight in insights.get('insights', []))}

ANALYST RECOMMENDATIONS:
{chr(10).join(f"• {rec}" for rec in insights.get('recommendations', []))}

OVERALL COMPETITIVE POSITION: {insights.get('competitive_position', 'Not assessed')}

Please provide a comprehensive analysis in the following format:

## COMPETITIVE ADVANTAGES
List 3-5 specific areas where {company_name} outperforms its competitors. Include quantitative comparisons where possible.

## COMPETITIVE DISADVANTAGES  
List 3-5 specific areas where {company_name} underperforms compared to peers. Include quantitative gaps where possible.

## STRATEGIC RECOMMENDATIONS
Provide 3-4 actionable strategic recommendations to improve competitive position, focusing on the most critical gaps identified.

## INVESTMENT PERSPECTIVE
Provide a brief assessment of {company_name}'s investment attractiveness relative to sector peers, considering growth potential, execution risks, and market position.

Keep the analysis data-driven, specific, and actionable. Use bullet points for clarity.
"""
        return prompt
    
    def is_available(self):
        """Check if Gemini service is available."""
        return self.configured and self.model is not None


# Global instance
gemini_service = GeminiService()
