"""Helper utility functions."""


def format_currency(amount):
    """Format currency amount in a readable format."""
    if not amount:
        return "N/A"
    
    try:
        amount = float(amount)
        
        if amount >= 1_000_000_000:  # Billions
            return f"₹{amount / 1_000_000_000:.2f}B"
        elif amount >= 1_000_000:  # Millions
            return f"₹{amount / 1_000_000:.2f}M"
        elif amount >= 1_000:  # Thousands
            return f"₹{amount / 1_000:.2f}K"
        else:
            return f"₹{amount:.2f}"
    except (ValueError, TypeError):
        return "N/A"


def safe_extract_amount(amount_dict):
    """Safely extract amount from amount dictionary."""
    if not amount_dict or not isinstance(amount_dict, dict):
        return None
    
    amount = amount_dict.get('amount')
    if amount is None:
        return None
    
    try:
        return float(amount)
    except (ValueError, TypeError):
        return None


def calculate_ltv_cac_ratio(financials):
    """Calculate LTV/CAC ratio from financials data."""
    if not financials:
        return None
    
    ltv = safe_extract_amount(financials.get('ltv'))
    cac = safe_extract_amount(financials.get('cac'))
    
    if ltv and cac and cac > 0:
        return ltv / cac
    
    return None


def calculate_revenue_multiple(financials, fundraise):
    """Calculate revenue multiple from financials and fundraise data."""
    if not financials or not fundraise:
        return None
    
    revenue = safe_extract_amount(financials.get('revenue'))
    
    # Try post-money valuation first, then pre-money
    valuation = None
    post_money = fundraise.get('post_money_valuation')
    if post_money:
        valuation = safe_extract_amount(post_money)
    
    if not valuation:
        pre_money = fundraise.get('pre_money_valuation')
        if pre_money:
            valuation = safe_extract_amount(pre_money)
    
    if revenue and valuation and revenue > 0:
        return valuation / revenue
    
    return None
