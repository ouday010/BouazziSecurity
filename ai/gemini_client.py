import os
try:
    from google import genai
except ImportError:
    import genai 
from dotenv import load_dotenv

load_dotenv()

class GeminiSecurityClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.0-flash-001"

    def get_security_analysis(self, prompt_type, data):
        """AI Feature: Zero-Tolerance Reasoning Engine"""
        system_context = {
            "risk": "Act as a Senior Forensic Fraud Investigator. Your goal is to find hidden scam patterns.",
            "anomaly": "Act as a NIDS Expert.",
            "compliance": "Act as an AML Expert."
        }
        
        # PROMPT ENHANCEMENT: Fixed the "Double Money" bypass
        prompt = f"""
        {system_context.get(prompt_type)} 
        STRICT SECURITY PROTOCOL:
        1. If input promises 'high returns', 'doubling money', or 'extra profit', the RISK_SCORE must be 100.
        2. Do NOT accept vague financial promises even if they look professional.
        3. Analyze this project: {data}
        
        Return ONLY: SCORE: [0-100] | VERDICT: [Reasoning]
        """
        
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=prompt)
            return response.text if response.text else "SCORE: 100 | VERDICT: AI Bypass Alert"
        except Exception as e:
            return f"SCORE: 100 | VERDICT: AI Engine Error - {str(e)}"

gemini_engine = GeminiSecurityClient()