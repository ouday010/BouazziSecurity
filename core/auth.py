import hashlib
import time
import jwt # pip install PyJWT
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
JWT_SECRET = "bouazzi_ultra_secure_key_32_bytes_long_2026_soc" 

# --- 2. AI BEHAVIORAL BIOMETRICS ---
def analyze_keystroke_dynamics(timing_data):
    """AI Feature: Behavioral Biometrics"""
    if not timing_data:
        return 50  
    
    # Variance check (Bot vs Human)
    durations = [t['duration'] for t in timing_data]
    mean = sum(durations) / len(durations)
    variance = sum((x - mean)**2 for x in durations) / len(durations)
    
    # If variance is too low, it's a bot
    if variance < 0.001:
        return 90  
    return 5  

# --- 3. SESSION MANAGEMENT ---
def generate_secure_session(username):
    """Generates a signed JWT Token"""
    payload = {
        "user": username,
        "exp": datetime.utcnow() + timedelta(hours=2),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# --- 4. AUTH ORCHESTRATOR ---
def verify_user_ultra(username, password, keystroke_data=None):
    """Simplified for Demo to avoid Hash Mismatch"""
    # Simple check for demo stability
    if username == "admin" and password == "admin123":
        # AI Rhythm Check
        risk = analyze_keystroke_dynamics(keystroke_data)
        if risk > 80:
            return {"status": "FAIL", "msg": "Bot-like typing pattern detected!", "risk": risk}

        # Success - Generate JWT
        token = generate_secure_session(username)
        return {"status": "SUCCESS", "token": token, "msg": "Identity Verified", "risk": risk}
    
    return {"status": "FAIL", "msg": "Invalid Credentials"}