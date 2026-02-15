from ai.gemini_client import gemini_engine

def analyze_project_risk(title, description):
    """
    Advanced Forensic Analysis: Checks for scam semantics and AI risk.
    """
    text = (title + " " + description).lower()
    
    # --- NEW: HARD-CODED SCAM DETECTION ---
    # Hedhom keywords dima m-liyin b-el fraud
    scam_triggers = [
        "double money", "extra money", "get rich", "multiplier", 
        "investment return", "earn fast", "no risk", "guaranteed"
    ]
    for trigger in scam_triggers:
        if trigger in text:
            return "SCORE: 100 | VERDICT: CRITICAL BLOCK - Financial Fraud Pattern Detected."

    # Context analysis for very short text
    if len(description.split()) < 4:
        return "SCORE: 15 | VERDICT: Initial risk low, but metadata requires manual review."

    # Gemini Analysis
    data_payload = f"Project: {title} | Description: {description}"
    analysis = gemini_engine.get_security_analysis("risk", data_payload)
    return analysis

def ai_data_leak_prevention(text):
    """DLP Engine"""
    sensitive_patterns = ["password", "secret_key", "0000"]
    for pattern in sensitive_patterns:
        if pattern in text.lower():
            return True, f"DLP ALERT: Sensitive pattern '{pattern}' detected."
    return False, ""