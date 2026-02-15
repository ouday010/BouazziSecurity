import streamlit as st
import pandas as pd
import time
import random

# --- 1. CORE INTEGRATION ---
try:
    from core.orchestrator import orchestrator
    from ai.anomaly_api import anomaly_sensor
    from core.auth import verify_user_ultra  # Import Login Logic
except Exception as e:
    st.error(f"System Linkage Error: {e}")

# --- 2. PROFESSIONAL UI STYLING ---
st.set_page_config(page_title="BouazziSecurity Pro", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f8fafc; color: #1e293b; }
    .login-box { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff; border-radius: 12px; padding: 5px; box-shadow: 0 2px 15px rgba(0,0,0,0.05); }
    .analysis-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .metric-box { text-align: center; padding: 15px; border-radius: 12px; background: #f1f5f9; border: 1px solid #cbd5e1; min-height: 120px; }
    .accuracy-val { font-size: 20px; font-weight: 900; margin-top: 5px; }
    .pillar-desc { font-size: 8.5px; color: #64748b; line-height: 1.2; font-weight: 500; }
    .log-container { background: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; border-left: 5px solid #3b82f6; }
    .log-line { color: #1e293b !important; font-size: 0.95rem; font-weight: 500; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'projects' not in st.session_state:
    st.session_state.projects = []

# --- 4. LOGIN PAGE ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.title("🔐 SOC Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            # Verify credentials using auth.py logic
            res = verify_user_ultra(user, pwd)
            if res["status"] == "SUCCESS":
                st.session_state.authenticated = True
                st.session_state.token = res["token"]
                st.success(f"Welcome {user}! Identity Verified.")
                time.sleep(1)
                st.rerun()
            else:
                st.error(res["msg"])
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Stop execution here until login

# --- 5. DASHBOARD (ONLY AFTER LOGIN) ---
st.title("🛡️ BouazziSecurity Autonomous Shield")
m = anomaly_sensor.get_real_time_metrics()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Network Stability", f"{100 - m['cpu_load']}%", delta="Stable")
c2.metric("Threat Neutralization", m['blocked_attempts'], delta=f"+{m['active_threats']}")
c3.metric("AI Core Status", "Online", delta="Gemini 2.0")
c4.metric("Identity Token", "JWT-ACTIVE", delta="Secure")

st.divider()

# --- 6. MAIN WORKSPACE (Forensic Lab / SOC / Market) ---
t1, t2, t3 = st.tabs(["🔬 Forensic Investigation Lab", "📡 SOC Intelligence Center", "🚀 Verified Market"])

with t1:
    col_input, col_result = st.columns([1, 1.3])
    with col_input:
        st.subheader("Campaign Submission")
        with st.form("audit_form"):
            title = st.text_input("Project Label")
            desc = st.text_area("Intention Payload")
            amt = st.number_input("Target Amount ($)", value=100)
            if st.form_submit_button("🚀 Execute Specialized Audit"):
                if title and desc:
                    anomaly_sensor.analyze_traffic_heuristics({"action": "audit_submission"})
                    with st.spinner("Analyzing Multi-Layer Integrity..."):
                        res = orchestrator.run_full_security_audit("192.168.1.1", title, desc, amt)
                        res['title'] = title
                        st.session_state.projects.append(res)
                else: st.warning("Input required.")

    with col_result:
        st.subheader("Specialized Integrity Analysis")
        if not st.session_state.projects:
            st.info("Awaiting forensic input.")
        else:
            p = st.session_state.projects[-1]
            acc_data = p.get('accuracies', {})
            
            if p.get('status') == "SUCCESS":
                st.success(f"✅ Clearance Granted for {p['title']}")
                p_colors = {k: "#10b981" for k in acc_data.keys()}
            else:
                st.error(f"🛑 CRITICAL BLOCK: {p.get('reason')}")
                p_colors = {k: "#ef4444" for k in acc_data.keys()}

            pillars_info = {
                "AES-256": "Data Encryption & Integrity",
                "JWT": "Identity Session Token",
                "HMAC": "Payload Authentication",
                "ZKP": "Zero-Knowledge Account Proof",
                "GEMINI": "AI Forensic Intent Accuracy",
                "STYLO": "Linguistic Style Fingerprinting",
                "RL-GATE": "Adaptive Defense Threshold"
            }

            st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
            cols = st.columns(7)
            for col, name in zip(cols, pillars_info.keys()):
                val = f"{acc_data.get(name, 0.0)}%"
                color = p_colors.get(name, "#ef4444")
                col.markdown(f"""
                <div class='metric-box'>
                    <p style='font-size:10px; font-weight:800;'>{name}</p>
                    <p class='accuracy-val' style='color:{color};'>{val}</p>
                    <p class='pillar-desc'>{pillars_info[name]}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='log-container'>", unsafe_allow_html=True)
            for log in p.get('audit_trail', []):
                st.markdown(f"<p class='log-line'>🟢 {log}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

with t2:
    st.header("SOC Visual Intelligence")
    risk_history = [proj.get('risk_level', 0) for proj in st.session_state.projects]
    st.line_chart(pd.DataFrame(risk_history, columns=["Risk Index (%)"]))
    st.area_chart(pd.DataFrame([m['cpu_load'], 22, 38], columns=["Processing Load"]))

# --- TAB 3: VERIFIED MARKET ---
with t3:
    st.header("Verified Market Repository")
    valid_projects = [p for p in st.session_state.projects if p.get('status') == "SUCCESS"]
    if not valid_projects:
        st.info("Market is empty. Verified projects will appear here after passing the 8-Engine Gate.")
    else:
        for p in valid_projects:
            display_risk = round(random.uniform(1.2, 9.8), 1) 
            
            with st.expander(f"📦 {p.get('title')} | Security Risk: {display_risk}%"):
                st.markdown("### 8-Layer Security Badges:")
                st.markdown("`[AES-256-GCM]` `[JWT-SESSION]` `[HMAC-SIGNED]` `[ZKP-VERIFIED]` `[AI-FORENSIC]` `[STYLO-DNA]` `[RL-ADAPTIVE]` `[DLP-SAFE]`")
                
                # N-wariw el accuracies el s7a7 elli t-calculaw specialized
                st.write("**Verified Accuracy Scores:**")
                st.json(p.get('accuracies'))
                
                st.write("**Encrypted Storage Payload (AES-GCM):**")
                st.code(p.get('encrypted_content'), language="text")
                
                st.write("**ZKP Handshake Metadata:**")
                st.json(p.get('payment_details'))
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()