"""Data processing functions for metrics extraction and comparison."""

import pandas as pd
import sys
sys.path.append('/Users/pragathi.vetrivelmurugan/AI-Analyst/backend/app')
from utils.helpers import safe_extract_amount, calculate_ltv_cac_ratio, calculate_revenue_multiple


class MetricsProcessor:
    """Processor for extracting and standardizing company metrics."""
    
    def __init__(self):
        pass
    
    def extract_metrics_for_comparison(self, companies_data):
        """Extract standardized metrics from companies data for comparison."""
        if not companies_data:
            print("No companies data provided for metrics extraction")
            return pd.DataFrame()
        
        metrics_list = []
        
        for company in companies_data:
            try:
                company_data = company['data']
                company_name = company_data.get('company_overview', {}).get('name', company['id'])
                
                # Extract all relevant metrics
                metrics = {
                    'company_name': company_name,
                    'sector': ' > '.join(company_data.get('company_overview', {}).get('sector_hierarchy', ['Unknown'])),
                    'stage': company_data.get('company_overview', {}).get('stage', 'Unknown'),
                    'founding_year': company_data.get('company_overview', {}).get('founding_year'),
                    
                    # Financial metrics
                    'revenue': safe_extract_amount(company_data.get('financials', {}).get('revenue')),
                    'gmv': safe_extract_amount(company_data.get('financials', {}).get('gmv')),
                    'cac': safe_extract_amount(company_data.get('financials', {}).get('cac')),
                    'aov': safe_extract_amount(company_data.get('financials', {}).get('aov')),
                    'gross_margin_pct': company_data.get('financials', {}).get('gross_margin_pct'),
                    
                    # Market metrics
                    'tam': safe_extract_amount(company_data.get('market', {}).get('tam')),
                    'sam': safe_extract_amount(company_data.get('market', {}).get('sam')),
                    
                    # Traction metrics
                    'orders_fulfilled_total': company_data.get('traction', {}).get('orders_fulfilled_total'),
                    'repeat_rate_pct': company_data.get('traction', {}).get('repeat_rate_pct'),
                    
                    # Fundraise metrics
                    'valuation': self._extract_valuation(company_data.get('fundraise', {})),
                    'round': company_data.get('fundraise', {}).get('round'),
                    
                    # Calculated metrics
                    'ltv_cac_ratio': calculate_ltv_cac_ratio(company_data.get('financials', {})),
                    'revenue_multiple': calculate_revenue_multiple(
                        company_data.get('financials', {}),
                        company_data.get('fundraise', {})
                    )
                }
                
                metrics_list.append(metrics)
                
            except Exception as e:
                print(f"Error extracting metrics for company {company.get('id', 'Unknown')}: {e}")
                continue
        
        df = pd.DataFrame(metrics_list)
        print(f"Extracted metrics for {len(df)} companies")
        return df
    
    def _extract_valuation(self, fundraise_data):
        """Extract valuation from fundraise data."""
        if not fundraise_data:
            return None
        
        # Try post-money first, then pre-money
        post_money = fundraise_data.get('post_money_valuation')
        if post_money and isinstance(post_money, dict):
            valuation = safe_extract_amount(post_money)
            if valuation:
                # Convert USD to INR if needed (approximate rate)
                if post_money.get('currency') == 'USD':
                    valuation = valuation * 83  # Approximate USD to INR
                return valuation
        
        pre_money = fundraise_data.get('pre_money_valuation')
        if pre_money and isinstance(pre_money, dict):
            valuation = safe_extract_amount(pre_money)
            if valuation:
                # Convert USD to INR if needed (approximate rate)
                if pre_money.get('currency') == 'USD':
                    valuation = valuation * 83  # Approximate USD to INR
                return valuation
        
        return None
    
    def prepare_comparison_data(self, target_company_data, competitor_companies):
        """Prepare data for comparison analysis."""
        # Combine target company with competitors
        all_companies = competitor_companies.copy()
        
        # Add target company if not already in the list
        target_name = target_company_data.get('company_overview', {}).get('name')
        if target_name and not any(comp['data'].get('company_overview', {}).get('name') == target_name for comp in all_companies):
            all_companies.append({
                'id': 'target_company',
                'data': target_company_data
            })
        
        # Extract metrics for all companies
        df = self.extract_metrics_for_comparison(all_companies)
        
        if df.empty:
            print("No data available for comparison")
            return df
        
        # Mark the target company
        if target_name:
            df.loc[df['company_name'] == target_name, 'is_target'] = True
            df['is_target'] = df['is_target'].fillna(False).infer_objects(copy=False)
        
        return df


# Global instance
metrics_processor = MetricsProcessor()
