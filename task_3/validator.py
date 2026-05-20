import re

def is_valid_select(sql_query):
    """Rule-based security check to block DML (Modifications)."""
    cleaned = sql_query.strip().upper()
    
    if not cleaned.startswith("SELECT") and not cleaned.startswith("WITH"):
        return False, "Query must start with SELECT or WITH."
        
    blocked_keywords = [r'\bDELETE\b', r'\bDROP\b', r'\bUPDATE\b', r'\bINSERT\b', r'\bALTER\b', r'\bTRUNCATE\b']
    
    for pattern in blocked_keywords:
        if re.search(pattern, cleaned):
            return False, f"Dangerous keyword detected: {pattern}"
            
    return True, "Valid"