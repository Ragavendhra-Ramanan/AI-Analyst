"""Analysis functions for benchmark comparison and insights."""

from typing import Dict, Any, List, Tuple
import statistics
import sys
sys.path.append('/Users/pragathi.vetrivelmurugan/AI-Analyst/backend/app')
from utils.helpers import format_currency


class CompetitiveAnalyzer:
    """Analyzer for competitive benchmarking and insights."""
    
    def __init__(self):
        pass
    
    def generate_comparison_insights(self, target_data: Dict[str, Any], df) -> Dict[str, Any]:
        """Generate insights by comparing target company with competitors."""
        if df.empty:
            return {"insights": [], "recommendations": []}
        
        insights = []
        recommendations = []
        
        # Get target company metrics
        target_name = target_data.get('company_overview', {}).get('name')
        if not target_name:
            return {"insights": [], "recommendations": []}
        
        target_row = df[df['company_name'] == target_name]
        if target_row.empty:
            return {"insights": [], "recommendations": []}
        
        target_metrics = target_row.iloc[0]
        competitor_data = df[df['company_name'] != target_name]
        
        if competitor_data.empty:
            return {"insights": [], "recommendations": []}
        
        # Revenue comparison
        if target_metrics['revenue'] and not competitor_data['revenue'].isna().all():
            revenue_percentile = self._calculate_percentile(target_metrics['revenue'], competitor_data['revenue'])
            insights.append(f"Revenue performance: {revenue_percentile:.0f}th percentile among peers")
            
            if revenue_percentile < 25:
                recommendations.append("Focus on revenue growth strategies")
            elif revenue_percentile > 75:
                recommendations.append("Strong revenue position - consider scaling strategies")
        
        # CAC comparison
        if target_metrics['cac'] and not competitor_data['cac'].isna().all():
            cac_percentile = 100 - self._calculate_percentile(target_metrics['cac'], competitor_data['cac'])
            insights.append(f"Customer Acquisition Cost: {cac_percentile:.0f}th percentile (lower is better)")
            
            if cac_percentile < 25:
                recommendations.append("High CAC - optimize marketing channels and conversion")
        
        # LTV/CAC ratio comparison
        if target_metrics['ltv_cac_ratio'] and not competitor_data['ltv_cac_ratio'].isna().all():
            ltv_cac_percentile = self._calculate_percentile(target_metrics['ltv_cac_ratio'], competitor_data['ltv_cac_ratio'])
            insights.append(f"LTV/CAC ratio: {ltv_cac_percentile:.0f}th percentile among peers")
            
            if ltv_cac_percentile < 25:
                recommendations.append("Improve customer lifetime value or reduce acquisition costs")
        
        # Gross margin comparison
        if target_metrics['gross_margin_pct'] and not competitor_data['gross_margin_pct'].isna().all():
            margin_percentile = self._calculate_percentile(target_metrics['gross_margin_pct'], competitor_data['gross_margin_pct'])
            insights.append(f"Gross margin: {margin_percentile:.0f}th percentile among peers")
            
            if margin_percentile < 25:
                recommendations.append("Focus on improving unit economics and cost structure")
        
        # Valuation comparison
        if target_metrics['valuation'] and not competitor_data['valuation'].isna().all():
            valuation_percentile = self._calculate_percentile(target_metrics['valuation'], competitor_data['valuation'])
            insights.append(f"Valuation: {valuation_percentile:.0f}th percentile among peers")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "competitive_position": self._assess_competitive_position(target_metrics, competitor_data)
        }
    
    def _calculate_percentile(self, value, series):
        """Calculate percentile of value within series."""
        if value is None:
            return 0
        
        valid_values = series.dropna().tolist()
        if not valid_values:
            return 50  # Default to median if no valid comparisons
        
        valid_values.append(value)
        valid_values.sort()
        
        rank = valid_values.index(value) + 1
        percentile = (rank / len(valid_values)) * 100
        return percentile
    
    def _assess_competitive_position(self, target_metrics, competitor_data) -> str:
        """Assess overall competitive position."""
        key_metrics = ['revenue', 'ltv_cac_ratio', 'gross_margin_pct']
        percentiles = []
        
        for metric in key_metrics:
            if target_metrics[metric] and not competitor_data[metric].isna().all():
                percentile = self._calculate_percentile(target_metrics[metric], competitor_data[metric])
                percentiles.append(percentile)
        
        if not percentiles:
            return "Insufficient data for assessment"
        
        avg_percentile = statistics.mean(percentiles)
        
        if avg_percentile >= 75:
            return "Strong market position"
        elif avg_percentile >= 50:
            return "Competitive market position"
        elif avg_percentile >= 25:
            return "Below average performance"
        else:
            return "Needs significant improvement"
    
    def get_sector_benchmarks(self, df, target_sector: str) -> Dict[str, Any]:
        """Get benchmark statistics for the sector."""
        if df.empty:
            return {}
        
        sector_data = df[df['sector'].str.contains(target_sector.split(' > ')[-1], case=False, na=False)]
        
        if sector_data.empty:
            return {}
        
        benchmarks = {}
        
        # Revenue benchmarks
        revenue_data = sector_data['revenue'].dropna()
        if not revenue_data.empty:
            benchmarks['revenue'] = {
                'median': revenue_data.median(),
                'p25': revenue_data.quantile(0.25),
                'p75': revenue_data.quantile(0.75),
                'formatted_median': format_currency(revenue_data.median())
            }
        
        # CAC benchmarks
        cac_data = sector_data['cac'].dropna()
        if not cac_data.empty:
            benchmarks['cac'] = {
                'median': cac_data.median(),
                'p25': cac_data.quantile(0.25),
                'p75': cac_data.quantile(0.75),
                'formatted_median': format_currency(cac_data.median())
            }
        
        # LTV/CAC ratio benchmarks
        ltv_cac_data = sector_data['ltv_cac_ratio'].dropna()
        if not ltv_cac_data.empty:
            benchmarks['ltv_cac_ratio'] = {
                'median': ltv_cac_data.median(),
                'p25': ltv_cac_data.quantile(0.25),
                'p75': ltv_cac_data.quantile(0.75)
            }
        
        # Gross margin benchmarks
        margin_data = sector_data['gross_margin_pct'].dropna()
        if not margin_data.empty:
            benchmarks['gross_margin_pct'] = {
                'median': margin_data.median(),
                'p25': margin_data.quantile(0.25),
                'p75': margin_data.quantile(0.75)
            }
        
        return benchmarks


# Global instance
competitive_analyzer = CompetitiveAnalyzer()
