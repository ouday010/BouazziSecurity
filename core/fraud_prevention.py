import hashlib

class FraudPreventionSystem:
    def __init__(self):
        # Simulated database of "Linguistic Fingerprints" from known fraud projects
        # In a real system, these are NLP-generated vectors
        self.known_fraud_fingerprints = [
            "high_urgency_crypto_pattern",
            "guaranteed_return_forex_pattern"
        ]
        self.active_connections = {} # Graph simulation: IP -> Project Titles

    def generate_linguistic_fingerprint(self, title, description):
        """
        AI Feature: NLP Linguistic Fingerprinting
        Creates a unique hash of the linguistic style to detect Fraud Rings.
        """
        # We take the style/tone patterns (simplified for demo)
        style_markers = f"{title[:3]}_{len(description)}_{description.count('!')}"
        return hashlib.md5(style_markers.encode()).hexdigest()

    def detect_fraud_ring(self, user_ip, title, description):
        """
        AI Feature: Graph Analysis (Network Attack Detection)
        Checks if the current project is linked to others via style or IP.
        """
        fingerprint = self.generate_linguistic_fingerprint(title, description)
        
        # 1. Check for Style Similarity (NLP Graph)
        if fingerprint in self.known_fraud_fingerprints:
            return False, "CRITICAL: NLP Fingerprint matches a known Fraud Ring pattern."

        # 2. Check for IP Overlap (Graph Analysis)
        if user_ip in self.active_connections:
            if len(self.active_connections[user_ip]) >= 2:
                return False, "SUSPICIOUS: Multiple campaigns from the same IP (Potential Sybil Attack)."
            self.active_connections[user_ip].append(title)
        else:
            self.active_connections[user_ip] = [title]

        # 3. Cross-Linguistic Pattern Matching
        # (Simulating finding hidden connections between different users)
        if "risk-free" in description.lower() and "guaranteed" in description.lower():
            return False, "AI BLOCK: Semantic signature linked to 'High-Yield Fraud' clusters."

        return True, "SAFE: No hidden connections or fraud ring patterns detected."

# Global instance for the orchestrator
fps_engine = FraudPreventionSystem()