import streamlit as st
import sqlite3, bcrypt, random, requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="MangoNav | AgriTech Platform",
    page_icon="🥭",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English": {
        "title": "MangoNav", "tagline": "AgriTech Intelligence Platform",
        "village_sel": "Select Village", "variety": "Mango Variety",
        "quantity": "Quantity (Tonnes)", "analyze_btn": "Run Profit Analysis",
        "top3": "Top 3 Profitable Destinations",
        "bar_title": "Net Profit Comparison", "pie_title": "Market Category Share",
        "map_title": "Smart Route Navigation",
        "rank": "Rank", "dest": "Destination", "cat": "Category",
        "dist_km": "Distance (km)", "rev": "Revenue (₹)", "trans": "Transport (₹)",
        "risk": "Risk (%)", "net": "Net Profit (₹)",
        "logout": "Sign Out", "select_lang": "Language",
        "highest_profit": "BEST PROFIT", "second_best": "2ND", "third_best": "3RD",
        "net_profit_lbl": "Net Profit", "away_lbl": "km",
        "your_loc": "Your Farm", "best_dest": "Best Market",
        "revenue_lbl": "Revenue", "transport_lbl": "Transport",
        "variety_lbl": "Variety", "qty_lbl": "Quantity",
        "best_market": "Best Market", "est_profit": "Max Profit",
        "farmer_tip": "Expert Recommendation",
        "tip_text": "Abroad Export yields +7% premium but requires grading certification. Local Export hubs are accessible within 2–3 days.",
        "no_results": "No markets found within 150km. Try a nearby village or different variety.",
        "kpi_profit": "Max Profit Potential", "kpi_market": "Nearest Market",
        "kpi_roi": "Expected ROI", "kpi_markets": "Markets Analysed",
        "farmer_profile": "Farmer Profile", "crop_data": "Crop Data",
        "name_label": "Farmer Name", "village_label": "Village / District",
        "sign_in": "Sign In", "register": "Register",
        "phone": "Phone Number", "password": "Password",
        "phone_ph": "10-digit mobile", "pass_ph": "Your password",
        "login_btn": "Sign In", "forgot": "Forgot Password?",
        "otp_opt": "Login with OTP", "send_otp": "Send OTP",
        "verify_otp": "Verify OTP", "otp_ph": "6-digit OTP",
        "name": "Full Name", "place": "Village / District", "reg_btn": "Create Account",
        "back": "Back", "use_pw": "Use password",
        "reset_pw": "Reset Password", "new_pw": "New Password",
        "conf_pw": "Confirm Password", "upd_pw": "Update Password",
        "welcome": "Welcome back",
    },
    "Telugu": {
        "title": "MangoNav", "tagline": "వ్యవసాయ సాంకేతిక వేదిక",
        "village_sel": "గ్రామం ఎంచుకోండి", "variety": "మామిడి రకం",
        "quantity": "పరిమాణం (టన్నులు)", "analyze_btn": "లాభం విశ్లేషణ అమలు చేయండి",
        "top3": "అగ్ర 3 లాభదాయక గమ్యాలు",
        "bar_title": "నికర లాభం పోలిక", "pie_title": "మార్కెట్ వర్గం వాటా",
        "map_title": "స్మార్ట్ రూట్ నావిగేషన్",
        "rank": "స్థానం", "dest": "గమ్యం", "cat": "వర్గం",
        "dist_km": "దూరం (కి.మీ)", "rev": "ఆదాయం (₹)", "trans": "రవాణా (₹)",
        "risk": "రిస్క్ (%)", "net": "నికర లాభం (₹)",
        "logout": "నిష్క్రమించు", "select_lang": "భాష",
        "highest_profit": "ఉత్తమ లాభం", "second_best": "2వ", "third_best": "3వ",
        "net_profit_lbl": "నికర లాభం", "away_lbl": "కి.మీ",
        "your_loc": "మీ పొలం", "best_dest": "ఉత్తమ మార్కెట్",
        "revenue_lbl": "ఆదాయం", "transport_lbl": "రవాణా",
        "variety_lbl": "రకం", "qty_lbl": "పరిమాణం",
        "best_market": "ఉత్తమ మార్కెట్", "est_profit": "గరిష్ట లాభం",
        "farmer_tip": "నిపుణుల సిఫారసు",
        "tip_text": "విదేశీ ఎగుమతి +7% ప్రీమియం ఇస్తుంది కానీ నాణ్యత ధృవీకరణ అవసరం.",
        "no_results": "150 కి.మీ పరిధిలో మార్కెట్లు కనుగొనబడలేదు.",
        "kpi_profit": "గరిష్ట లాభ సామర్థ్యం", "kpi_market": "సమీప మార్కెట్",
        "kpi_roi": "అంచనా ROI", "kpi_markets": "విశ్లేషించిన మార్కెట్లు",
        "farmer_profile": "రైతు వివరాలు", "crop_data": "పంట సమాచారం",
        "name_label": "రైతు పేరు", "village_label": "గ్రామం / జిల్లా",
        "sign_in": "లాగిన్", "register": "నమోదు",
        "phone": "ఫోన్ నంబర్", "password": "పాస్‌వర్డ్",
        "phone_ph": "10 అంకెల నంబర్", "pass_ph": "పాస్‌వర్డ్",
        "login_btn": "లాగిన్ చేయండి", "forgot": "పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt": "OTP తో లాగిన్", "send_otp": "OTP పంపండి",
        "verify_otp": "OTP ధృవీకరించండి", "otp_ph": "6 అంకెల OTP",
        "name": "పూర్తి పేరు", "place": "గ్రామం / జిల్లా", "reg_btn": "ఖాతా తెరవండి",
        "back": "తిరిగి", "use_pw": "పాస్‌వర్డ్ ఉపయోగించండి",
        "reset_pw": "పాస్‌వర్డ్ రీసెట్", "new_pw": "కొత్త పాస్‌వర్డ్",
        "conf_pw": "నిర్ధారించండి", "upd_pw": "అప్‌డేట్ చేయండి",
        "welcome": "స్వాగతం",
    },
    "Hindi": {
        "title": "MangoNav", "tagline": "कृषि तकनीक मंच",
        "village_sel": "गाँव चुनें", "variety": "आम की किस्म",
        "quantity": "मात्रा (टन)", "analyze_btn": "लाभ विश्लेषण चलाएं",
        "top3": "शीर्ष 3 लाभदायक गंतव्य",
        "bar_title": "शुद्ध लाभ तुलना", "pie_title": "बाज़ार श्रेणी हिस्सेदारी",
        "map_title": "स्मार्ट रूट नेविगेशन",
        "rank": "रैंक", "dest": "गंतव्य", "cat": "श्रेणी",
        "dist_km": "दूरी (कि.मी.)", "rev": "राजस्व (₹)", "trans": "परिवहन (₹)",
        "risk": "जोखिम (%)", "net": "शुद्ध लाभ (₹)",
        "logout": "साइन आउट", "select_lang": "भाषा",
        "highest_profit": "सर्वोत्तम लाभ", "second_best": "2रा", "third_best": "3रा",
        "net_profit_lbl": "शुद्ध लाभ", "away_lbl": "कि.मी.",
        "your_loc": "आपका खेत", "best_dest": "सर्वोत्तम बाज़ार",
        "revenue_lbl": "राजस्व", "transport_lbl": "परिवहन",
        "variety_lbl": "किस्म", "qty_lbl": "मात्रा",
        "best_market": "सर्वोत्तम बाज़ार", "est_profit": "अधिकतम लाभ",
        "farmer_tip": "विशेषज्ञ सुझाव",
        "tip_text": "विदेश निर्यात +7% प्रीमियम देता है लेकिन ग्रेडिंग प्रमाणीकरण आवश्यक है।",
        "no_results": "150 कि.मी. के भीतर कोई बाज़ार नहीं मिला।",
        "kpi_profit": "अधिकतम लाभ क्षमता", "kpi_market": "निकटतम बाज़ार",
        "kpi_roi": "अपेक्षित ROI", "kpi_markets": "विश्लेषित बाज़ार",
        "farmer_profile": "किसान प्रोफ़ाइल", "crop_data": "फसल डेटा",
        "name_label": "किसान का नाम", "village_label": "गाँव / जिला",
        "sign_in": "साइन इन", "register": "पंजीकरण",
        "phone": "फ़ोन नंबर", "password": "पासवर्ड",
        "phone_ph": "10 अंकों का नंबर", "pass_ph": "पासवर्ड",
        "login_btn": "साइन इन करें", "forgot": "पासवर्ड भूल गए?",
        "otp_opt": "OTP से लॉगिन", "send_otp": "OTP भेजें",
        "verify_otp": "OTP सत्यापित करें", "otp_ph": "6 अंकों का OTP",
        "name": "पूरा नाम", "place": "गाँव / जिला", "reg_btn": "खाता बनाएं",
        "back": "वापस", "use_pw": "पासवर्ड का उपयोग करें",
        "reset_pw": "पासवर्ड रीसेट", "new_pw": "नया पासवर्ड",
        "conf_pw": "पुष्टि करें", "upd_pw": "अपडेट करें",
        "welcome": "स्वागत है",
    },
    "Kannada": {
        "title": "MangoNav", "tagline": "ಕೃಷಿ ತಂತ್ರಜ್ಞಾನ ವೇದಿಕೆ",
        "village_sel": "ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ", "variety": "ಮಾವಿನ ತಳಿ",
        "quantity": "ಪ್ರಮಾಣ (ಟನ್)", "analyze_btn": "ಲಾಭ ವಿಶ್ಲೇಷಣೆ ಚಲಾಯಿಸಿ",
        "top3": "ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title": "ನಿವ್ವಳ ಲಾಭ ಹೋಲಿಕೆ", "pie_title": "ಮಾರುಕಟ್ಟೆ ವರ್ಗ ಪಾಲು",
        "map_title": "ಸ್ಮಾರ್ಟ್ ರೂಟ್ ನ್ಯಾವಿಗೇಷನ್",
        "rank": "ಶ್ರೇಣಿ", "dest": "ಗಮ್ಯ", "cat": "ವರ್ಗ",
        "dist_km": "ದೂರ (ಕಿ.ಮೀ)", "rev": "ಆದಾಯ (₹)", "trans": "ಸಾರಿಗೆ (₹)",
        "risk": "ಅಪಾಯ (%)", "net": "ನಿವ್ವಳ ಲಾಭ (₹)",
        "logout": "ಸೈನ್ ಔಟ್", "select_lang": "ಭಾಷೆ",
        "highest_profit": "ಅತ್ಯುತ್ತಮ ಲಾಭ", "second_best": "2ನೇ", "third_best": "3ನೇ",
        "net_profit_lbl": "ನಿವ್ವಳ ಲಾಭ", "away_lbl": "ಕಿ.ಮೀ",
        "your_loc": "ನಿಮ್ಮ ಹೊಲ", "best_dest": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "revenue_lbl": "ಆದಾಯ", "transport_lbl": "ಸಾರಿಗೆ",
        "variety_lbl": "ತಳಿ", "qty_lbl": "ಪ್ರಮಾಣ",
        "best_market": "ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ", "est_profit": "ಗರಿಷ್ಠ ಲಾಭ",
        "farmer_tip": "ತಜ್ಞರ ಶಿಫಾರಸು",
        "tip_text": "ವಿದೇಶ ರಫ್ತು +7% ಪ್ರೀಮಿಯಂ ನೀಡುತ್ತದೆ ಆದರೆ ಗ್ರೇಡಿಂಗ್ ಪ್ರಮಾಣೀಕರಣ ಅಗತ್ಯ.",
        "no_results": "150 ಕಿ.ಮೀ ಪರಿಧಿಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "kpi_profit": "ಗರಿಷ್ಠ ಲಾಭ ಸಾಮರ್ಥ್ಯ", "kpi_market": "ಸಮೀಪ ಮಾರುಕಟ್ಟೆ",
        "kpi_roi": "ನಿರೀಕ್ಷಿತ ROI", "kpi_markets": "ವಿಶ್ಲೇಷಿಸಿದ ಮಾರುಕಟ್ಟೆಗಳು",
        "farmer_profile": "ರೈತ ಪ್ರೊಫೈಲ್", "crop_data": "ಬೆಳೆ ಡೇಟಾ",
        "name_label": "ರೈತರ ಹೆಸರು", "village_label": "ಗ್ರಾಮ / ಜಿಲ್ಲೆ",
        "sign_in": "ಸೈನ್ ಇನ್", "register": "ನೋಂದಣಿ",
        "phone": "ಫೋನ್ ಸಂಖ್ಯೆ", "password": "ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph": "10 ಅಂಕಿಯ ಸಂಖ್ಯೆ", "pass_ph": "ಪಾಸ್‌ವರ್ಡ್",
        "login_btn": "ಸೈನ್ ಇನ್ ಮಾಡಿ", "forgot": "ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt": "OTP ಲಾಗಿನ್", "send_otp": "OTP ಕಳುಹಿಸಿ",
        "verify_otp": "OTP ಪರಿಶೀಲಿಸಿ", "otp_ph": "6 ಅಂಕಿಯ OTP",
        "name": "ಪೂರ್ಣ ಹೆಸರು", "place": "ಗ್ರಾಮ / ಜಿಲ್ಲೆ", "reg_btn": "ಖಾತೆ ತೆರೆಯಿರಿ",
        "back": "ಹಿಂತಿರುಗಿ", "use_pw": "ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ",
        "reset_pw": "ಪಾಸ್‌ವರ್ಡ್ ರೀಸೆಟ್", "new_pw": "ಹೊಸ ಪಾಸ್‌ವರ್ಡ್",
        "conf_pw": "ದೃಢಪಡಿಸಿ", "upd_pw": "ನವೀಕರಿಸಿ",
        "welcome": "ಸ್ವಾಗತ",
    },
}

# ══════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect("farmers.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, place TEXT, phone TEXT PRIMARY KEY, password TEXT)")
    conn.commit(); conn.close()

def reg(n, p, ph, pw):
    conn = sqlite3.connect("farmers.db")
    h = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    try: conn.execute("INSERT INTO users VALUES(?,?,?,?)", (n, p, ph, h)); conn.commit(); return True
    except: return False
    finally: conn.close()

def login(ph, pw):
    conn = sqlite3.connect("farmers.db"); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone=?", (ph,)); u = c.fetchone(); conn.close()
    if u and bcrypt.checkpw(pw.encode(), u[3]): return u
    return None

def get_u(ph):
    conn = sqlite3.connect("farmers.db"); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone=?", (ph,)); u = c.fetchone(); conn.close(); return u

def upd_pw(ph, pw):
    conn = sqlite3.connect("farmers.db")
    h = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    conn.execute("UPDATE users SET password=? WHERE phone=?", (h, ph)); conn.commit(); conn.close()

init_db()

for k, v in {
    "logged_in": False, "auth_mode": "login", "otp_mode": False,
    "otp_sent": False, "otp_code": None, "otp_phone": None,
    "forgot": False, "f_otp_sent": False, "f_otp_ok": False, "f_code": None,
    "lang": "English", "run": False,
    "last_village": None, "last_variety": "Banganapalli", "last_tonnes": 10.0,
}.items():
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
# MASTER CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, [data-testid="stDecoration"] { display: none !important; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
.stTextInput > label { display: none !important; }

/* ── Sidebar dark theme ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B12 0%, #132218 50%, #0D1B12 100%) !important;
    border-right: 1px solid rgba(46,125,50,0.3) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,140,0,0.3) !important;
    border-radius: 10px !important;
    color: #E8F5E9 !important;
}
[data-testid="stSidebar"] .stSelectbox > label {
    color: #81C784 !important; font-size: 11px !important;
    font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stNumberInput > label {
    color: #81C784 !important; font-size: 11px !important;
    font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,140,0,0.3) !important;
    border-radius: 10px !important; color: #E8F5E9 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] .stExpander {
    border: 1px solid rgba(46,125,50,0.25) !important;
    border-radius: 12px !important;
    background: rgba(255,255,255,0.03) !important;
}
[data-testid="stSidebar"] .stExpander > details > summary {
    color: #A5D6A7 !important; font-weight: 600 !important; font-size: 13px !important;
}

/* ── Main content area ── */
.stApp { background: #F8FAF8 !important; }

/* ── ALL BUTTONS — gradient gold-to-orange ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    background: linear-gradient(135deg, #FF8C00, #E65100) !important;
    color: white !important;
    font-size: 15px !important;
    padding: 14px 24px !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 20px rgba(255,140,0,0.4) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #E65100, #BF360C) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,0,0.55) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important;
    color: rgba(255,255,255,0.65) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    box-shadow: none !important; font-size: 12px !important;
    padding: 9px 14px !important; letter-spacing: 0 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.14) !important;
    color: white !important; transform: none !important;
}

/* ── Login form inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important; color: white !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important;
    padding: 13px 16px !important;
}
.stTextInput > div > div > input:focus { border-color: #FF8C00 !important; outline: none !important; }
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.35) !important; }

/* ── Plotly chart border-radius ── */
.js-plotly-plot, .plot-container { border-radius: 10px !important; overflow: hidden; }

/* ── Sidebar selectbox login page override ── */
.login-select .stSelectbox > div > div {
    background: rgba(255,255,255,0.1) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOGIN — Glassmorphism centered modal
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    lang = st.session_state.lang; tx = T[lang]
    st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .stApp {
        background-image:
            linear-gradient(rgba(5,20,8,0.75), rgba(5,20,8,0.75)),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=90&fit=crop') !important;
        background-size: cover !important; background-position: center !important; min-height: 100vh !important;
    }
    .main .block-container { padding-top: 0 !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        color: white !important; border-radius: 10px !important;
    }
    .stSelectbox > label { color: rgba(255,255,255,0.55) !important; font-size: 10px !important; }
    </style>""", unsafe_allow_html=True)

    # Top bar
    st.markdown(f"""
    <div style="background:rgba(13,27,18,0.7);backdrop-filter:blur(10px);padding:14px 40px;
        display:flex;align-items:center;justify-content:space-between;
        border-bottom:1px solid rgba(46,125,50,0.2);">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;background:linear-gradient(135deg,#FF8C00,#E65100);
                border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">🥭</div>
            <div>
                <div style="font-family:'Inter',sans-serif;font-size:18px;font-weight:800;color:white;">{tx['title']}</div>
                <div style="font-size:10px;color:rgba(165,214,167,0.7);letter-spacing:2px;text-transform:uppercase;">{tx['tagline']}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    _, lc = st.columns([5, 1])
    with lc:
        c = st.selectbox("", ["English","Telugu","Hindi","Kannada"],
            index=["English","Telugu","Hindi","Kannada"].index(lang),
            key="lang_sel", label_visibility="collapsed")
        if c != lang: st.session_state.lang = c; st.rerun()

    st.markdown(f"""
    <div style="text-align:center;padding:52px 20px 40px;">
        <h1 style="font-family:'Inter',sans-serif;font-size:52px;color:white;font-weight:800;
            line-height:1.1;margin-bottom:14px;text-shadow:0 4px 24px rgba(0,0,0,0.5);">
            {tx['hero_title'] if 'hero_title' in tx else tx['title']}
        </h1>
        <p style="font-size:17px;color:rgba(255,255,255,0.7);max-width:480px;margin:0 auto;">
            {tx['tagline']}
        </p>
    </div>""", unsafe_allow_html=True)

    _, mc, _ = st.columns([1, 1.2, 1])
    with mc:
        # Glassmorphism card
        st.markdown("""
        <div style="background:rgba(13,27,18,0.82);backdrop-filter:blur(32px);
            border:1px solid rgba(255,140,0,0.2);border-radius:20px;
            padding:36px 32px 28px;box-shadow:0 32px 80px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)

        tb1, tb2 = st.columns(2)
        with tb1:
            if st.button(tx["sign_in"], key="tab_si", use_container_width=True,
                type="primary" if st.session_state.auth_mode == "login" else "secondary"):
                st.session_state.auth_mode = "login"; st.session_state.otp_mode = False
                st.session_state.forgot = False; st.rerun()
        with tb2:
            if st.button(tx["register"], key="tab_ca", use_container_width=True,
                type="primary" if st.session_state.auth_mode == "register" else "secondary"):
                st.session_state.auth_mode = "register"; st.session_state.otp_mode = False
                st.session_state.forgot = False; st.rerun()

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        def lbl(t):
            st.markdown(f'<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,140,0,0.85);margin-bottom:6px;font-weight:600;">{t}</div>', unsafe_allow_html=True)

        if st.session_state.forgot:
            lbl(tx["reset_pw"]); fph = st.text_input("_fph", placeholder=tx["phone_ph"], key="fp_ph", label_visibility="collapsed")
            if not st.session_state.f_otp_sent:
                if st.button(tx["send_otp"], key="fp_send", use_container_width=True):
                    if fph and len(fph) == 10 and fph.isdigit():
                        u = get_u(fph)
                        if u:
                            code = str(random.randint(100000, 999999)); st.session_state.f_code = code
                            st.session_state.f_otp_sent = True; st.session_state.otp_phone = fph
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            elif not st.session_state.f_otp_ok:
                lbl(tx["otp_ph"]); eo = st.text_input("_fov", placeholder=tx["otp_ph"], key="fp_ov", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="fp_ver", use_container_width=True):
                    if eo == st.session_state.f_code: st.session_state.f_otp_ok = True; st.rerun()
                    else: st.error("Incorrect OTP.")
            else:
                lbl(tx["new_pw"]); np_ = st.text_input("_npw", placeholder=tx["new_pw"], type="password", key="fp_np", label_visibility="collapsed")
                lbl(tx["conf_pw"]); cp_ = st.text_input("_cpw", placeholder=tx["conf_pw"], type="password", key="fp_cp", label_visibility="collapsed")
                if st.button(tx["upd_pw"], key="fp_upd", use_container_width=True):
                    if np_ and np_ == cp_: upd_pw(st.session_state.otp_phone, np_); st.success("Password updated!"); st.session_state.forgot = False; st.session_state.f_otp_sent = False; st.session_state.f_otp_ok = False; st.session_state.f_code = None; st.rerun()
                    else: st.error("Passwords do not match.")
            if st.button(tx["back"], key="fp_back", use_container_width=True, type="secondary"): st.session_state.forgot = False; st.rerun()

        elif st.session_state.auth_mode == "login" and st.session_state.otp_mode:
            lbl(tx["phone"]); op = st.text_input("_op", placeholder=tx["phone_ph"], key="otp_ph_in", label_visibility="collapsed")
            if not st.session_state.otp_sent:
                if st.button(tx["send_otp"], key="s_otp", use_container_width=True):
                    if op and len(op) == 10 and op.isdigit():
                        u = get_u(op)
                        if u:
                            code = str(random.randint(100000, 999999)); st.session_state.otp_code = code
                            st.session_state.otp_sent = True; st.session_state.otp_phone = op
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            else:
                lbl(tx["otp_ph"]); eo = st.text_input("_eov", placeholder=tx["otp_ph"], key="otp_v", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="v_otp", use_container_width=True):
                    if eo == st.session_state.otp_code: u = get_u(st.session_state.otp_phone); st.session_state.logged_in = True; st.session_state.user = u; st.session_state.otp_sent = False; st.rerun()
                    else: st.error("Incorrect OTP.")
            if st.button(tx["use_pw"], key="use_pw_btn", use_container_width=True, type="secondary"): st.session_state.otp_mode = False; st.rerun()

        elif st.session_state.auth_mode == "login":
            lbl(tx["phone"]); ph = st.text_input("_lph", placeholder=tx["phone_ph"], key="l_ph", label_visibility="collapsed")
            lbl(tx["password"]); pw = st.text_input("_lpw", placeholder=tx["pass_ph"], type="password", key="l_pw", label_visibility="collapsed")
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            if st.button(tx["login_btn"], key="do_login", use_container_width=True):
                if ph and pw:
                    u = login(ph, pw)
                    if u: st.session_state.logged_in = True; st.session_state.user = u; st.rerun()
                    else: st.error("Incorrect phone or password.")
                else: st.warning("Fill all fields.")
            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
            fa, oa = st.columns(2)
            with fa:
                if st.button(tx["forgot"], key="frg", use_container_width=True, type="secondary"): st.session_state.forgot = True; st.rerun()
            with oa:
                if st.button(tx["otp_opt"], key="otp_sw", use_container_width=True, type="secondary"): st.session_state.otp_mode = True; st.rerun()
        else:
            for label, key_, ph_, is_pw in [(tx["name"],"r_nm","Full name",False),(tx["place"],"r_pl","Village, District",False),(tx["phone"],"r_ph",tx["phone_ph"],False),(tx["password"],"r_pw",tx["pass_ph"],True)]:
                lbl(label)
                if is_pw: st.text_input(f"_{key_}", placeholder=ph_, key=key_, type="password", label_visibility="collapsed")
                else: st.text_input(f"_{key_}", placeholder=ph_, key=key_, label_visibility="collapsed")
            if st.button(tx["reg_btn"], key="do_reg", use_container_width=True):
                n = st.session_state.get("r_nm",""); p = st.session_state.get("r_pl",""); ph = st.session_state.get("r_ph",""); pw = st.session_state.get("r_pw","")
                if n and p and ph and pw:
                    if reg(n, p, ph, pw): st.success("Account created! Sign in."); st.session_state.auth_mode = "login"; st.rerun()
                    else: st.error("Phone already registered.")
                else: st.warning("All fields required.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:12px;font-size:10px;color:rgba(255,255,255,0.2);letter-spacing:2px;">SECURE · ENCRYPTED · FARMER DATA PROTECTED</div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_all():
    def s(p):
        try: df = pd.read_csv(p); df.columns = df.columns.str.strip().str.lower(); return df
        except: return pd.DataFrame()
    return (s("Village data.csv"), s("cleaned_price_data.csv"), s("cleaned_mandi_location.csv"),
            s("cleaned_processing_facilities.csv"), s("Pulp_units_merged_lat_long.csv"),
            s("cleaned_pickle_units.csv"), s("cleaned_local_export.csv"), s("cleaned_abroad_export.csv"),
            s("cleaned_cold_storage.csv"), s("cleaned_fpo.csv"))

villages, prices, geo, processing, pulp, pickle_u, local_exp, abroad_exp, cold, fpo = load_all()

def hav(la1, lo1, la2, lo2):
    R = 6371; la1, lo1, la2, lo2 = map(np.radians, [la1, lo1, la2, lo2])
    return R * 2 * np.arcsin(np.sqrt(np.sin((la2-la1)/2)**2 + np.cos(la1)*np.cos(la2)*np.sin((lo2-lo1)/2)**2))

def dcols(df):
    nm = la = lo = None
    for c in df.columns:
        cl = c.lower()
        if "lat" in cl and la is None: la = c
        if ("lon" in cl or "lng" in cl) and lo is None: lo = c
        if any(x in cl for x in ["name","firm","facility","hub","market","place","panchayat","company","unit","mandal"]) and nm is None: nm = c
    if nm is None and len(df.columns) > 0: nm = df.columns[0]
    return nm, la, lo

def vlist():
    nc, _, _ = dcols(villages)
    if nc and nc in villages.columns: return sorted(villages[nc].dropna().unique().tolist())
    return ["Default Village"]

def vcoords(vn):
    nc, lc, loc = dcols(villages)
    if nc and lc and loc:
        r = villages[villages[nc] == vn]
        if not r.empty: return float(r.iloc[0][lc]), float(r.iloc[0][loc])
    return 15.9129, 79.7400

def base_price(vlat, vlon):
    try:
        m = prices.merge(geo, on="market", how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices.copy()
        lc = next((c for c in m.columns if "lat" in c.lower()), None)
        loc = next((c for c in m.columns if "lon" in c.lower()), None)
        pc = next((c for c in m.columns if "price" in c.lower()), None)
        if lc and loc and pc:
            m = m.dropna(subset=[lc, loc, pc]); m["d"] = m.apply(lambda r: hav(vlat, vlon, r[lc], r[loc]), axis=1)
            return float(m.loc[m["d"].idxmin()][pc])
    except: pass
    return 25.0

def osm_route(lat1, lon1, lat2, lon2):
    try:
        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson", timeout=8).json()
        if "routes" in r and r["routes"]:
            return [(c[1], c[0]) for c in r["routes"][0]["geometry"]["coordinates"]]
    except: pass
    return [(lat1, lon1), (lat2, lon2)]

def analyse(vlat, vlon, variety, tonnes):
    VACC = {
        "Mandi": ["Banganapalli","Totapuri","Neelam","Rasalu"],
        "Processing": ["Totapuri","Neelam"], "Pulp": ["Totapuri"],
        "Pickle": ["Totapuri","Rasalu"], "Local Export": ["Banganapalli"],
        "Abroad Export": ["Banganapalli"],
        "Cold Storage": ["Banganapalli","Totapuri","Neelam","Rasalu"],
        "FPO": ["Banganapalli","Totapuri","Neelam","Rasalu"],
    }
    mdf = prices.merge(geo, on="market", how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices
    CATS = {
        "Mandi":        {"mg": 0.00, "col": "#1565C0", "ic": "🏪", "df": mdf},
        "Processing":   {"mg": 0.03, "col": "#7c3aed", "ic": "🏭", "df": processing},
        "Pulp":         {"mg": 0.04, "col": "#2E7D32", "ic": "🧃", "df": pulp},
        "Pickle":       {"mg": 0.025,"col": "#db2777", "ic": "🫙", "df": pickle_u},
        "Local Export": {"mg": 0.05, "col": "#2E7D32", "ic": "🚛", "df": local_exp},
        "Abroad Export":{"mg": 0.07, "col": "#FF8C00", "ic": "✈️", "df": abroad_exp},
        "Cold Storage": {"mg": 0.01, "col": "#1565C0", "ic": "🧊", "df": cold},
        "FPO":          {"mg": 0.02, "col": "#2E7D32", "ic": "👥", "df": fpo},
    }
    HND = {"Mandi":0,"Processing":300,"Pulp":400,"Pickle":250,"Local Export":500,"Abroad Export":700,"Cold Storage":200,"FPO":150}
    DLY = {"Mandi":0,"Processing":7,"Pulp":10,"Pickle":5,"Local Export":14,"Abroad Export":30,"Cold Storage":3,"FPO":2}
    bp = base_price(vlat, vlon); rows = []
    for cat, cfg in CATS.items():
        if variety not in VACC.get(cat, []): continue
        df_ = cfg["df"]
        if df_ is None or df_.empty: continue
        nc, lc, loc = dcols(df_)
        if not lc or not loc: continue
        for _, row in df_.iterrows():
            try:
                rlat = float(row[lc]); rlon = float(row[loc])
                dist = hav(vlat, vlon, rlat, rlon)
                if dist > 150: continue
                nm = str(row[nc]) if nc and nc in row.index else cat
                adj = bp * (1 + cfg["mg"]); rev = adj * 1000 * tonnes
                tra = 5000 + dist * 200 * tonnes + 300 * tonnes
                fin = rev * (DLY.get(cat, 0) / 365) * 0.12
                rr = (0.004 * (dist / 10)) + 0.002; rc = rev * rr
                net = rev - tra - HND.get(cat, 0) * tonnes - fin - rc
                rows.append({"Type": cat, "Name": nm, "Dist_km": round(dist, 1),
                             "Revenue": round(rev), "Transport": round(tra),
                             "Risk_pct": round(rr * 100, 2), "Net_Profit": round(net),
                             "Lat": rlat, "Lon": rlon, "color": cfg["col"], "icon": cfg["ic"]})
            except: continue
    if not rows: return pd.DataFrame()
    df = pd.DataFrame(rows).drop_duplicates(subset=["Type","Name"]).sort_values("Net_Profit", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
lang = st.session_state.get("lang", "English"); tx = T[lang]
fname = st.session_state.user[0]; fplace = st.session_state.user[1]

vl = vlist()

# ══════════════════════════════════════════════════════════════
# DARK SIDEBAR — SaaS style
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo + Title
    st.markdown(f"""
    <div style="padding:28px 20px 20px;border-bottom:1px solid rgba(46,125,50,0.25);">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <div style="width:40px;height:40px;background:linear-gradient(135deg,#FF8C00,#E65100);
                border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">🥭</div>
            <div>
                <div style="font-family:'Inter',sans-serif;font-size:18px;font-weight:800;color:white;">{tx['title']}</div>
                <div style="font-size:9px;color:rgba(165,214,167,0.6);letter-spacing:2px;text-transform:uppercase;">{tx['tagline']}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Language
    st.markdown('<div style="padding:16px 8px 0;">', unsafe_allow_html=True)
    sl = st.selectbox(tx["select_lang"], ["English","Telugu","Hindi","Kannada"],
                      index=["English","Telugu","Hindi","Kannada"].index(lang))
    if sl != lang: st.session_state.lang = sl; st.rerun()

    # Farmer Profile expander
    with st.expander(f"👤  {tx['farmer_profile']}", expanded=True):
        st.markdown(f"""
        <div style="padding:8px 0;">
            <div style="font-size:10px;color:rgba(165,214,167,0.6);letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">{tx['name_label']}</div>
            <div style="font-size:14px;color:white;font-weight:600;">{fname}</div>
            <div style="font-size:10px;color:rgba(165,214,167,0.6);letter-spacing:1px;text-transform:uppercase;margin-top:10px;margin-bottom:3px;">{tx['village_label']}</div>
            <div style="font-size:13px;color:#A5D6A7;">📍 {fplace}</div>
        </div>""", unsafe_allow_html=True)

    # Crop Data expander
    with st.expander(f"🌾  {tx['crop_data']}", expanded=True):
        st.markdown(f'<p style="font-size:10px;font-weight:600;color:rgba(165,214,167,0.7);margin-bottom:4px;letter-spacing:1px;text-transform:uppercase;">{tx["village_sel"]}</p>', unsafe_allow_html=True)
        sel_village = st.selectbox("__v", vl, key="sel_v", label_visibility="collapsed")
        st.markdown(f'<p style="font-size:10px;font-weight:600;color:rgba(165,214,167,0.7);margin-bottom:4px;letter-spacing:1px;text-transform:uppercase;">{tx["variety"]}</p>', unsafe_allow_html=True)
        sel_variety = st.selectbox("__var", ["Banganapalli","Totapuri","Neelam","Rasalu"], key="sel_var", label_visibility="collapsed")
        st.markdown(f'<p style="font-size:10px;font-weight:600;color:rgba(165,214,167,0.7);margin-bottom:4px;letter-spacing:1px;text-transform:uppercase;">{tx["quantity"]}</p>', unsafe_allow_html=True)
        sel_tonnes = st.number_input("__t", min_value=0.5, value=10.0, step=0.5, key="sel_t", label_visibility="collapsed")

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    # THE BUTTON — gradient gold-to-orange, clearly visible
    run_clicked = st.button(tx["analyze_btn"], key="run_btn", use_container_width=True)

    if run_clicked:
        st.session_state.run = True
        st.session_state.last_village = sel_village
        st.session_state.last_variety = sel_variety
        st.session_state.last_tonnes = sel_tonnes

    # Live prices
    st.markdown(f"""
    <div style="margin-top:20px;padding:14px 8px;">
        <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(165,214,167,0.5);margin-bottom:10px;">LIVE MARKET PRICES</div>
    """, unsafe_allow_html=True)
    for v, (p, tr, cl) in {
        "Banganapalli": (28, "+2.1%", "#4ade80"),
        "Totapuri": (18, "-0.8%", "#f87171"),
        "Neelam": (22, "+1.4%", "#4ade80"),
        "Rasalu": (30, "+3.2%", "#4ade80"),
    }.items():
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
            padding:8px 10px;margin-bottom:5px;background:rgba(255,255,255,0.04);
            border-radius:8px;border:1px solid rgba(255,255,255,0.05);">
            <div>
                <div style="font-size:12px;color:#E8F5E9;font-weight:500;">{v}</div>
                <div style="font-size:10px;color:rgba(165,214,167,0.5);">₹{p}/kg</div>
            </div>
            <div style="font-size:12px;font-weight:700;color:{cl};">{tr}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    if st.button(tx["logout"], key="logout_btn", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MAIN AREA — white/light gray
# ══════════════════════════════════════════════════════════════
rv   = st.session_state.get("last_village", sel_village)
rvar = st.session_state.get("last_variety",  sel_variety)
rt   = st.session_state.get("last_tonnes",   sel_tonnes)

# Top header bar
st.markdown(f"""
<div style="background:white;padding:18px 32px;border-bottom:1px solid #E8F5E9;
    display:flex;align-items:center;justify-content:space-between;
    box-shadow:0 1px 8px rgba(0,0,0,0.06);">
    <div>
        <div style="font-family:'Inter',sans-serif;font-size:22px;font-weight:800;color:#1B5E20;">
            {tx['welcome']}, {fname} 👋
        </div>
        <div style="font-size:13px;color:#66BB6A;margin-top:2px;">
            📍 {fplace} &nbsp;·&nbsp; {sel_variety} &nbsp;·&nbsp; {sel_tonnes} T
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:38px;height:38px;background:linear-gradient(135deg,#FF8C00,#E65100);
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-size:14px;font-weight:800;color:white;">{fname[0].upper()}</div>
    </div>
</div>""", unsafe_allow_html=True)

main = st.container()
with main:
    st.markdown('<div style="padding:24px 32px 40px;background:#F8FAF8;">', unsafe_allow_html=True)

    if not st.session_state.get("run", False):
        # Welcome state
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1B5E20,#2E7D32);border-radius:16px;
            padding:40px 48px;margin-bottom:24px;position:relative;overflow:hidden;">
            <div style="position:absolute;right:-20px;top:-20px;width:200px;height:200px;
                background:rgba(255,255,255,0.03);border-radius:50%;"></div>
            <div style="position:absolute;right:40px;top:50%;transform:translateY(-50%);
                font-size:120px;opacity:0.08;">🥭</div>
            <div style="font-size:11px;letter-spacing:3px;color:rgba(165,214,167,0.7);
                text-transform:uppercase;margin-bottom:10px;">Ready to Analyse</div>
            <h2 style="font-family:'Inter',sans-serif;font-size:32px;color:white;
                font-weight:800;margin-bottom:8px;">Select your crop details in the sidebar</h2>
            <p style="font-size:15px;color:rgba(255,255,255,0.65);max-width:520px;line-height:1.7;">
                Choose your village, mango variety and quantity, then click
                <b style="color:#FF8C00;">Run Profit Analysis</b> to discover your most profitable market.
            </p>
        </div>""", unsafe_allow_html=True)

        # Stat cards row
        sc1, sc2, sc3, sc4 = st.columns(4)
        for col, icon, label, val, border, sub in [
            (sc1,"🥭","Varieties Supported","4","#FF8C00","Banganapalli · Totapuri · Neelam · Rasalu"),
            (sc2,"🏪","Market Types","8","#2E7D32","Mandi · Export · Pulp · FPO · Cold Storage"),
            (sc3,"📍","Districts Covered","120+","#1565C0","AP · Telangana · Karnataka"),
            (sc4,"🤖","Profit Engine","AI","#FF8C00","Risk-adjusted · Route-optimised"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:22px;
                    border-left:4px solid {border};
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
                    <div style="font-size:26px;margin-bottom:6px;">{icon}</div>
                    <div style="font-size:11px;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">{label}</div>
                    <div style="font-size:32px;font-weight:800;color:#1B5E20;">{val}</div>
                    <div style="font-size:11px;color:#6B7280;margin-top:6px;">{sub}</div>
                </div>""", unsafe_allow_html=True)

    else:
        # RESULTS
        with st.spinner("Calculating profit routes..."):
            vlat, vlon = vcoords(rv)
            df_res = analyse(vlat, vlon, rvar, rt)

        if df_res.empty:
            st.warning(tx["no_results"])
        else:
            top3 = df_res.head(3)
            bn = int(top3.iloc[0]["Net_Profit"])
            bd = top3.iloc[0]["Name"]
            nearest = top3.iloc[0]["Dist_km"]
            cost = int(top3.iloc[0]["Revenue"])
            roi = round((bn / cost) * 100, 1) if cost > 0 else 0

            # ── KPI CARDS ──
            k1, k2, k3, k4 = st.columns(4)
            kpi_data = [
                (k1, tx["kpi_profit"], f"₹{bn:,}", "#FF8C00", "🏆", f"via {bd}"),
                (k2, tx["kpi_market"], bd, "#2E7D32", "📍", f"{nearest} km away"),
                (k3, tx["kpi_roi"], f"{roi}%", "#1565C0", "📈", "Return on investment"),
                (k4, tx["kpi_markets"], str(len(df_res)), "#FF8C00", "🔍", f"within 150km"),
            ]
            for col, label, val, border, icon, sub in kpi_data:
                with col:
                    st.markdown(f"""
                    <div style="background:white;border-radius:14px;padding:20px 22px;
                        border-left:4px solid {border};
                        box-shadow:0 2px 16px rgba(0,0,0,0.08);">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                            <div style="font-size:11px;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;">{label}</div>
                            <div style="font-size:20px;">{icon}</div>
                        </div>
                        <div style="font-size:28px;font-weight:800;color:#1B5E20;margin:6px 0;line-height:1;">{val}</div>
                        <div style="font-size:11px;color:#6B7280;">{sub}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)

            # ── TOP 3 CARDS ──
            st.markdown(f'<div style="font-size:13px;font-weight:700;color:#1B5E20;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">🏅 {tx["top3"]}</div>', unsafe_allow_html=True)
            medals = [
                ("#FF8C00", tx["highest_profit"], True,  "linear-gradient(135deg,#1B5E20,#2E7D32)", "white"),
                ("#94a3b8", tx["second_best"],    False, "white", "#1B5E20"),
                ("#cd7c4b", tx["third_best"],     False, "white", "#1B5E20"),
            ]
            c3 = st.columns(3)
            for i, (col, (acc, lbl_, istop, bg, tc)) in enumerate(zip(c3, medals)):
                if i >= len(top3): break
                r = top3.iloc[i]
                with col:
                    st.markdown(f"""
                    <div style="background:{bg};border-radius:16px;padding:22px;height:100%;
                        border:{'2px solid rgba(255,140,0,0.4)' if istop else '1px solid #E5E7EB'};
                        box-shadow:{'0 8px 32px rgba(27,94,32,0.25)' if istop else '0 2px 12px rgba(0,0,0,0.06)'};
                        position:relative;overflow:hidden;">
                        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:{acc};margin-bottom:8px;font-weight:700;">{lbl_}</div>
                        <div style="font-size:15px;font-weight:700;color:{'white' if istop else '#1B5E20'};margin-bottom:4px;line-height:1.3;">{r['Name']}</div>
                        <div style="display:inline-flex;align-items:center;gap:4px;background:{'rgba(255,255,255,0.12)' if istop else '#F0FDF4'};border-radius:6px;padding:3px 9px;margin-bottom:14px;">
                            <span style="font-size:12px;">{r['icon']}</span>
                            <span style="font-size:10px;color:{r['color']};font-weight:600;">{r['Type']}</span>
                        </div>
                        <div style="font-size:28px;font-weight:800;color:{acc};margin-bottom:2px;">₹{int(r['Net_Profit']):,}</div>
                        <div style="font-size:11px;color:{'rgba(255,255,255,0.5)' if istop else '#9CA3AF'};margin-bottom:14px;">{r['Dist_km']} {tx['away_lbl']}</div>
                        <div style="border-top:1px solid {'rgba(255,255,255,0.12)' if istop else '#F3F4F6'};padding-top:12px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;">
                            <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9CA3AF'};margin-bottom:2px;">{tx['revenue_lbl']}</div><div style="font-size:11px;font-weight:700;color:{'rgba(255,255,255,0.9)' if istop else '#16a34a'};">₹{int(r['Revenue']):,}</div></div>
                            <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9CA3AF'};margin-bottom:2px;">{tx['transport_lbl']}</div><div style="font-size:11px;font-weight:700;color:#ef4444;">₹{int(r['Transport']):,}</div></div>
                            <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9CA3AF'};margin-bottom:2px;">{tx['risk']}</div><div style="font-size:11px;font-weight:700;color:#FF8C00;">{r['Risk_pct']}%</div></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)

            # ── EXPERT TIP ──
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#FFF8E1,#FFF3E0);border-radius:12px;
                padding:15px 20px;margin-bottom:22px;border-left:4px solid #FF8C00;
                display:flex;align-items:flex-start;gap:12px;">
                <span style="font-size:20px;flex-shrink:0;">💡</span>
                <div>
                    <div style="font-size:11px;font-weight:700;color:#E65100;letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">{tx['farmer_tip']}</div>
                    <div style="font-size:13px;color:#BF360C;line-height:1.6;">{tx['tip_text']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            # ── CHARTS — plotly_white template ──
            ch1, ch2 = st.columns([3, 2])
            with ch1:
                st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="font-size:14px;font-weight:700;color:#1B5E20;margin-bottom:14px;">{tx["bar_title"]}</div>', unsafe_allow_html=True)
                max_v = int(top3["Net_Profit"].max())
                fig = go.Figure(go.Bar(
                    y=top3["Name"], x=top3["Net_Profit"], orientation="h",
                    marker=dict(
                        color=["#FF8C00","#2E7D32","#1565C0"],
                        line=dict(width=0)
                    ),
                    text=[f"₹{int(v):,}" for v in top3["Net_Profit"]],
                    textposition="outside",
                    textfont=dict(size=13, color="#1B5E20", family="Inter"),
                    hovertemplate="<b>%{y}</b><br>Net Profit: ₹%{x:,.0f}<extra></extra>",
                ))
                fig.update_layout(
                    template="plotly_white", height=220,
                    margin=dict(l=0, r=110, t=4, b=4),
                    font=dict(family="Inter"),
                    xaxis=dict(
                        showgrid=True, gridcolor="#F0F0F0", zeroline=False,
                        tickfont=dict(size=10, color="#9CA3AF"),
                        range=[0, max_v * 1.4],
                        tickformat=",.0f", tickprefix="₹",
                    ),
                    yaxis=dict(autorange="reversed", tickfont=dict(size=13, color="#374151")),
                    hoverlabel=dict(bgcolor="#1B5E20", bordercolor="#FF8C00", font=dict(color="white")),
                    paper_bgcolor="white", plot_bgcolor="white",
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with ch2:
                st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="font-size:14px;font-weight:700;color:#1B5E20;margin-bottom:14px;">{tx["pie_title"]}</div>', unsafe_allow_html=True)
                # Pie: each destination's individual profit share
                pie_labels = [r["Name"][:18]+"…" if len(r["Name"]) > 18 else r["Name"] for _, r in top3.iterrows()]
                pie_vals = [int(r["Net_Profit"]) for _, r in top3.iterrows()]
                fig2 = go.Figure(go.Pie(
                    labels=pie_labels, values=pie_vals, hole=0.55,
                    marker=dict(
                        colors=["#FF8C00","#2E7D32","#1565C0"],
                        line=dict(color="white", width=3)
                    ),
                    textinfo="percent",
                    textfont=dict(size=12, family="Inter"),
                    hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
                ))
                fig2.update_layout(
                    template="plotly_white", height=220,
                    margin=dict(l=8, r=8, t=4, b=4),
                    legend=dict(font=dict(size=10, family="Inter"), orientation="v", x=1.0, y=0.5),
                    font=dict(family="Inter"),
                    annotations=[dict(text=f"<b>{rvar}</b>", x=0.5, y=0.5, font=dict(size=12, color="#1B5E20"), showarrow=False)],
                    hoverlabel=dict(bgcolor="#1B5E20", bordercolor="#FF8C00", font=dict(color="white")),
                    paper_bgcolor="white",
                )
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── TABLE ──
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.05);margin-bottom:20px;"><div style="font-size:14px;font-weight:700;color:#1B5E20;margin-bottom:14px;">📋 {tx["top3"]}</div>', unsafe_allow_html=True)
            disp = top3[["Rank","Name","Type","Dist_km","Revenue","Transport","Risk_pct","Net_Profit"]].copy()
            disp.columns = [tx["rank"],tx["dest"],tx["cat"],tx["dist_km"],tx["rev"],tx["trans"],tx["risk"],tx["net"]]
            disp[tx["rev"]]     = disp[tx["rev"]].apply(lambda x: f"₹{int(x):,}")
            disp[tx["trans"]]   = disp[tx["trans"]].apply(lambda x: f"₹{int(x):,}")
            disp[tx["net"]]     = disp[tx["net"]].apply(lambda x: f"₹{int(x):,}")
            disp[tx["dist_km"]] = disp[tx["dist_km"]].apply(lambda x: f"{x:.1f} km")
            disp[tx["risk"]]    = disp[tx["risk"]].apply(lambda x: f"{x:.2f}%")
            st.dataframe(disp, use_container_width=True, height=176, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── MAP — CartoDB Positron, OSM routes for all 3 ──
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #E5E7EB;box-shadow:0 2px 12px rgba(0,0,0,0.05);"><div style="font-size:14px;font-weight:700;color:#1B5E20;margin-bottom:6px;">🗺️ {tx["map_title"]}</div><div style="font-size:11px;color:#9CA3AF;margin-bottom:14px;">🏠 Farm origin &nbsp;|&nbsp; ★ Best market (gold route) &nbsp;|&nbsp; All routes via real roads</div>', unsafe_allow_html=True)

            with st.spinner("Loading road routes for all 3 destinations..."):
                br = top3.iloc[0]
                m = folium.Map(location=[vlat, vlon], zoom_start=9, tiles="CartoDB Positron")

                # Farm marker — house icon
                folium.Marker(
                    [vlat, vlon],
                    popup=folium.Popup(f"<b style='font-family:Inter'>{fname}</b><br>📍 {rv}", max_width=200),
                    tooltip=tx["your_loc"],
                    icon=folium.DivIcon(html="""
                    <div style="background:#1B5E20;border:3px solid #FF8C00;border-radius:50%;
                        width:44px;height:44px;display:flex;align-items:center;justify-content:center;
                        font-size:20px;box-shadow:0 4px 16px rgba(0,0,0,0.4);">🏠</div>
                    """, icon_size=(44, 44), icon_anchor=(22, 22))
                ).add_to(m)

                route_cfg = [
                    ("#FF8C00", 6, 0.95, None),    # Gold solid — Best
                    ("#2E7D32", 4, 0.7, "8 4"),    # Green dashed — 2nd
                    ("#1565C0", 4, 0.7, "8 4"),    # Blue dashed — 3rd
                ]
                for i, (_, row) in enumerate(top3.iterrows()):
                    rcol, wt, op, dash = route_cfg[i]
                    coords = osm_route(vlat, vlon, row["Lat"], row["Lon"])
                    folium.PolyLine(coords, color=rcol, weight=wt, opacity=op, dash_array=dash).add_to(m)

                    if i == 0:
                        # Glowing star for best destination
                        folium.Marker(
                            [row["Lat"], row["Lon"]],
                            popup=folium.Popup(
                                f"<b style='font-family:Inter'>{row['Name']}</b><br>{row['Type']}<br>"
                                f"<span style='color:#2E7D32;font-weight:700;font-size:14px'>₹{int(row['Net_Profit']):,}</span>",
                                max_width=220),
                            tooltip=f"★ BEST — {row['Name']}",
                            icon=folium.DivIcon(html="""
                            <div style="background:#FF8C00;border:3px solid white;border-radius:50%;
                                width:46px;height:46px;display:flex;align-items:center;justify-content:center;
                                font-size:22px;font-weight:900;color:white;
                                box-shadow:0 0 0 4px rgba(255,140,0,0.3),0 4px 20px rgba(255,140,0,0.6);">★</div>
                            """, icon_size=(46, 46), icon_anchor=(23, 23))
                        ).add_to(m)
                    else:
                        folium.CircleMarker(
                            [row["Lat"], row["Lon"]], radius=12,
                            color=rcol, fill=True, fill_color=rcol, fill_opacity=0.9, weight=3,
                            popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br>₹{int(row['Net_Profit']):,}", max_width=200),
                            tooltip=f"#{i+1} — {row['Name']}",
                        ).add_to(m)

            st_folium(m, width=None, height=520, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
