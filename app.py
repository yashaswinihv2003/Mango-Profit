import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import numpy as np
import random
import requests
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="MangoNav",
                   page_icon="🥭", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English": {
        "title":"MangoNav","tagline":"Smart Profit Intelligence for Mango Farmers",
        "sign_in":"Sign In","create_account":"Register",
        "phone":"Phone Number","password":"Password",
        "phone_ph":"10-digit mobile number","pass_ph":"Your password",
        "login_btn":"Sign In","forgot":"Forgot Password?",
        "otp_opt":"Login with OTP","send_otp":"Send OTP",
        "verify_otp":"Verify OTP","otp_ph":"6-digit OTP",
        "name":"Full Name","place":"Village / District","reg_btn":"Create Account",
        "select_lang":"Language","village_sel":"Select Your Village",
        "variety":"Mango Variety","quantity":"Quantity (Tonnes)",
        "analyze_btn":"Find Best Markets",
        "top3":"Top 3 Most Profitable Destinations",
        "bar_title":"Net Profit Comparison","pie_title":"Market Share",
        "map_title":"Route Map to Best Market",
        "rank":"Rank","dest":"Destination","cat":"Category",
        "dist_km":"Distance (km)","rev":"Revenue (₹)","trans":"Transport (₹)",
        "risk":"Risk (%)","net":"Net Profit (₹)",
        "logout":"Sign Out","reset_pw":"Reset Password",
        "new_pw":"New Password","conf_pw":"Confirm Password","upd_pw":"Update Password",
        "back":"Back","use_pw":"Use password instead",
        "live_prices":"Today's Mango Prices",
        "highest_profit":"BEST PROFIT","second_best":"2ND BEST","third_best":"3RD BEST",
        "net_profit_lbl":"Net Profit","away_lbl":"km away",
        "your_loc":"Your Farm","best_dest":"Best Market",
        "revenue_lbl":"Revenue","transport_lbl":"Transport",
        "profit_summary":"Your Profit Analysis",
        "variety_lbl":"Variety","qty_lbl":"Quantity",
        "best_market":"Best Market","est_profit":"Est. Profit",
        "farmer_tip":"Expert Insight",
        "tip_text":"Abroad Export gives the highest return (+7% premium) but requires quality grading. Local Export hubs are nearest and easiest to access for most farmers.",
        "no_results":"No markets found within 150km. Try a different village or variety.",
        "welcome":"Welcome back",
        "fill_details":"Enter Your Farm Details",
        "hero_title":"Find Your Most\nProfitable Mango Market",
        "hero_sub":"AI-powered analysis across mandis, processing units,\nexport hubs — with real road routes.",
    },
    "Telugu": {
        "title":"MangoNav","tagline":"మామిడి రైతుల స్మార్ట్ లాభ సమాచారం",
        "sign_in":"లాగిన్","create_account":"నమోదు చేయండి",
        "phone":"ఫోన్ నంబర్","password":"పాస్‌వర్డ్",
        "phone_ph":"10 అంకెల నంబర్","pass_ph":"మీ పాస్‌వర్డ్",
        "login_btn":"లాగిన్ చేయండి","forgot":"పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt":"OTP తో లాగిన్","send_otp":"OTP పంపండి",
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"6 అంకెల OTP",
        "name":"పూర్తి పేరు","place":"గ్రామం / జిల్లా","reg_btn":"ఖాతా తెరవండి",
        "select_lang":"భాష","village_sel":"మీ గ్రామం ఎంచుకోండి",
        "variety":"మామిడి రకం","quantity":"పరిమాణం (టన్నులు)",
        "analyze_btn":"ఉత్తమ మార్కెట్లు కనుగొనండి",
        "top3":"అగ్ర 3 లాభ గమ్యాలు",
        "bar_title":"నికర లాభం పోలిక","pie_title":"మార్కెట్ వాటా",
        "map_title":"ఉత్తమ మార్కెట్‌కు మార్గ మ్యాప్",
        "rank":"స్థానం","dest":"గమ్యం","cat":"వర్గం",
        "dist_km":"దూరం (కి.మీ)","rev":"ఆదాయం (₹)","trans":"రవాణా (₹)",
        "risk":"రిస్క్ (%)","net":"నికర లాభం (₹)",
        "logout":"నిష్క్రమించు","reset_pw":"పాస్‌వర్డ్ రీసెట్",
        "new_pw":"కొత్త పాస్‌వర్డ్","conf_pw":"నిర్ధారించండి","upd_pw":"అప్‌డేట్ చేయండి",
        "back":"తిరిగి వెళ్ళండి","use_pw":"పాస్‌వర్డ్ ఉపయోగించండి",
        "live_prices":"నేటి మామిడి ధరలు",
        "highest_profit":"అత్యుత్తమ లాభం","second_best":"2వ ఉత్తమం","third_best":"3వ ఉత్తమం",
        "net_profit_lbl":"నికర లాభం","away_lbl":"కి.మీ దూరం",
        "your_loc":"మీ పొలం","best_dest":"ఉత్తమ మార్కెట్",
        "revenue_lbl":"ఆదాయం","transport_lbl":"రవాణా",
        "profit_summary":"మీ లాభం విశ్లేషణ",
        "variety_lbl":"రకం","qty_lbl":"పరిమాణం",
        "best_market":"ఉత్తమ మార్కెట్","est_profit":"అంచనా లాభం",
        "farmer_tip":"నిపుణుల అభిప్రాయం",
        "tip_text":"విదేశీ ఎగుమతి అత్యధిక లాభం (+7%) ఇస్తుంది కానీ నాణ్యత ధృవీకరణ అవసరం.",
        "no_results":"150 కి.మీ పరిధిలో మార్కెట్లు కనుగొనబడలేదు.",
        "welcome":"స్వాగతం","fill_details":"మీ పొలం వివరాలు నమోదు చేయండి",
        "hero_title":"మీ అత్యంత లాభదాయక\nమామిడి మార్కెట్ కనుగొనండి",
        "hero_sub":"మండీలు, ప్రాసెసింగ్ యూనిట్లు, ఎగుమతి కేంద్రాల\nఅంతటా AI విశ్లేషణ.",
    },
    "Hindi": {
        "title":"MangoNav","tagline":"आम किसानों के लिए स्मार्ट लाभ जानकारी",
        "sign_in":"साइन इन","create_account":"पंजीकरण करें",
        "phone":"फ़ोन नंबर","password":"पासवर्ड",
        "phone_ph":"10 अंकों का नंबर","pass_ph":"आपका पासवर्ड",
        "login_btn":"साइन इन करें","forgot":"पासवर्ड भूल गए?",
        "otp_opt":"OTP से लॉगिन","send_otp":"OTP भेजें",
        "verify_otp":"OTP सत्यापित करें","otp_ph":"6 अंकों का OTP",
        "name":"पूरा नाम","place":"गाँव / जिला","reg_btn":"खाता बनाएं",
        "select_lang":"भाषा","village_sel":"अपना गाँव चुनें",
        "variety":"आम की किस्म","quantity":"मात्रा (टन)",
        "analyze_btn":"सर्वोत्तम बाज़ार खोजें",
        "top3":"शीर्ष 3 लाभदायक गंतव्य",
        "bar_title":"शुद्ध लाभ तुलना","pie_title":"बाज़ार हिस्सेदारी",
        "map_title":"सर्वोत्तम बाज़ार का मार्ग",
        "rank":"रैंक","dest":"गंतव्य","cat":"श्रेणी",
        "dist_km":"दूरी (कि.मी.)","rev":"राजस्व (₹)","trans":"परिवहन (₹)",
        "risk":"जोखिम (%)","net":"शुद्ध लाभ (₹)",
        "logout":"साइन आउट","reset_pw":"पासवर्ड रीसेट",
        "new_pw":"नया पासवर्ड","conf_pw":"पुष्टि करें","upd_pw":"अपडेट करें",
        "back":"वापस जाएं","use_pw":"पासवर्ड का उपयोग करें",
        "live_prices":"आज के आम के भाव",
        "highest_profit":"सर्वोत्तम लाभ","second_best":"दूसरा सर्वश्रेष्ठ","third_best":"तीसरा सर्वश्रेष्ठ",
        "net_profit_lbl":"शुद्ध लाभ","away_lbl":"कि.मी. दूर",
        "your_loc":"आपका खेत","best_dest":"सर्वोत्तम बाज़ार",
        "revenue_lbl":"राजस्व","transport_lbl":"परिवहन",
        "profit_summary":"आपका लाभ विश्लेषण",
        "variety_lbl":"किस्म","qty_lbl":"मात्रा",
        "best_market":"सर्वोत्तम बाज़ार","est_profit":"अनुमानित लाभ",
        "farmer_tip":"विशेषज्ञ सुझाव",
        "tip_text":"विदेश निर्यात सबसे अधिक लाभ (+7%) देता है लेकिन गुणवत्ता प्रमाणीकरण आवश्यक है।",
        "no_results":"150 कि.मी. के भीतर कोई बाज़ार नहीं मिला।",
        "welcome":"स्वागत है","fill_details":"अपने खेत की जानकारी दर्ज करें",
        "hero_title":"अपना सबसे लाभदायक\nआम बाज़ार खोजें",
        "hero_sub":"मंडी, प्रोसेसिंग यूनिट, निर्यात केंद्र —\nAI से पूर्ण विश्लेषण।",
    },
    "Kannada": {
        "title":"MangoNav","tagline":"ಮಾವು ರೈತರಿಗೆ ಸ್ಮಾರ್ಟ್ ಲಾಭ ಮಾಹಿತಿ",
        "sign_in":"ಸೈನ್ ಇನ್","create_account":"ನೋಂದಣಿ",
        "phone":"ಫೋನ್ ಸಂಖ್ಯೆ","password":"ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph":"10 ಅಂಕಿಯ ಸಂಖ್ಯೆ","pass_ph":"ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್",
        "login_btn":"ಸೈನ್ ಇನ್ ಮಾಡಿ","forgot":"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt":"OTP ಮೂಲಕ ಲಾಗಿನ್","send_otp":"OTP ಕಳುಹಿಸಿ",
        "verify_otp":"OTP ಪರಿಶೀಲಿಸಿ","otp_ph":"6 ಅಂಕಿಯ OTP",
        "name":"ಪೂರ್ಣ ಹೆಸರು","place":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ","reg_btn":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "select_lang":"ಭಾಷೆ","village_sel":"ನಿಮ್ಮ ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ",
        "variety":"ಮಾವಿನ ತಳಿ","quantity":"ಪ್ರಮಾಣ (ಟನ್)",
        "analyze_btn":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "top3":"ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title":"ನಿವ್ವಳ ಲಾಭ ಹೋಲಿಕೆ","pie_title":"ಮಾರುಕಟ್ಟೆ ಪಾಲು",
        "map_title":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಮಾರ್ಗ ನಕ್ಷೆ",
        "rank":"ಶ್ರೇಣಿ","dest":"ಗಮ್ಯ","cat":"ವರ್ಗ",
        "dist_km":"ದೂರ (ಕಿ.ಮೀ)","rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)",
        "risk":"ಅಪಾಯ (%)","net":"ನಿವ್ವಳ ಲಾಭ (₹)",
        "logout":"ಸೈನ್ ಔಟ್","reset_pw":"ಪಾಸ್‌ವರ್ಡ್ ರೀಸೆಟ್",
        "new_pw":"ಹೊಸ ಪಾಸ್‌ವರ್ಡ್","conf_pw":"ದೃಢಪಡಿಸಿ","upd_pw":"ನವೀಕರಿಸಿ",
        "back":"ಹಿಂತಿರುಗಿ","use_pw":"ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ",
        "live_prices":"ಇಂದಿನ ಮಾವಿನ ಬೆಲೆಗಳು",
        "highest_profit":"ಅತ್ಯುತ್ತಮ ಲಾಭ","second_best":"2ನೇ ಉತ್ತಮ","third_best":"3ನೇ ಉತ್ತಮ",
        "net_profit_lbl":"ನಿವ್ವಳ ಲಾಭ","away_lbl":"ಕಿ.ಮೀ ದೂರ",
        "your_loc":"ನಿಮ್ಮ ಹೊಲ","best_dest":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "revenue_lbl":"ಆದಾಯ","transport_lbl":"ಸಾರಿಗೆ",
        "profit_summary":"ನಿಮ್ಮ ಲಾಭ ವಿಶ್ಲೇಷಣೆ",
        "variety_lbl":"ತಳಿ","qty_lbl":"ಪ್ರಮಾಣ",
        "best_market":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ","est_profit":"ಅಂದಾಜು ಲಾಭ",
        "farmer_tip":"ತಜ್ಞರ ಅಭಿಪ್ರಾಯ",
        "tip_text":"ವಿದೇಶ ರಫ್ತು ಅತ್ಯಧಿಕ ಲಾಭ (+7%) ನೀಡುತ್ತದೆ ಆದರೆ ಗುಣಮಟ್ಟ ಪ್ರಮಾಣೀಕರಣ ಅಗತ್ಯ.",
        "no_results":"150 ಕಿ.ಮೀ ಪರಿಧಿಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "welcome":"ಸ್ವಾಗತ","fill_details":"ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "hero_title":"ನಿಮ್ಮ ಅತ್ಯಂತ ಲಾಭದಾಯಕ\nಮಾವಿನ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "hero_sub":"ಮಂಡಿ, ಸಂಸ್ಕರಣಾ ಘಟಕ, ರಫ್ತು ಕೇಂದ್ರ —\nAI ವಿಶ್ಲೇಷಣೆ.",
    },
}

# ══════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect("farmers.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, place TEXT, phone TEXT PRIMARY KEY, password TEXT)")
    conn.commit(); conn.close()

def register_user(name, place, phone, password):
    conn = sqlite3.connect("farmers.db")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        conn.execute("INSERT INTO users VALUES (?,?,?,?)", (name,place,phone,hashed))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def login_user(phone, password):
    conn = sqlite3.connect("farmers.db")
    c = conn.cursor(); c.execute("SELECT * FROM users WHERE phone=?", (phone,))
    u = c.fetchone(); conn.close()
    if u and bcrypt.checkpw(password.encode(), u[3]): return u
    return None

def get_user(phone):
    conn = sqlite3.connect("farmers.db")
    c = conn.cursor(); c.execute("SELECT * FROM users WHERE phone=?", (phone,))
    u = c.fetchone(); conn.close(); return u

def update_pw(phone, pw):
    conn = sqlite3.connect("farmers.db")
    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    conn.execute("UPDATE users SET password=? WHERE phone=?", (hashed,phone))
    conn.commit(); conn.close()

init_db()

# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
for k,v in {
    "logged_in":False,"auth_mode":"login",
    "otp_mode":False,"otp_sent":False,"otp_code":None,"otp_phone":None,
    "forgot":False,"f_otp_sent":False,"f_otp_ok":False,"f_code":None,
    "lang":"English","run":False,
    "last_village":None,"last_variety":"Banganapalli","last_tonnes":10.0,
}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Merriweather:wght@400;700&display=swap');
*{box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stDecoration"]{visibility:hidden;display:none!important;}
.stApp{font-family:'Nunito',sans-serif;}
.main .block-container{padding:0!important;max-width:100%!important;}
.stTextInput>label{display:none!important;}
.stButton>button{
    font-family:'Nunito',sans-serif!important;font-size:13px!important;
    font-weight:800!important;border-radius:10px!important;
    padding:12px 20px!important;transition:all 0.2s!important;cursor:pointer!important;
    letter-spacing:0.3px!important;
}
.stButton>button:not([kind="secondary"]){
    background:linear-gradient(135deg,#16a34a,#15803d)!important;
    color:white!important;border:none!important;
    box-shadow:0 4px 16px rgba(22,163,74,0.4)!important;
}
.stButton>button:not([kind="secondary"]):hover{
    background:linear-gradient(135deg,#15803d,#166534)!important;
    transform:translateY(-1px)!important;
}
.stButton>button[kind="secondary"]{
    background:rgba(255,255,255,0.08)!important;color:rgba(255,255,255,0.7)!important;
    border:1px solid rgba(255,255,255,0.2)!important;
    font-size:12px!important;padding:10px 14px!important;
}
.stButton>button[kind="secondary"]:hover{
    color:white!important;border-color:rgba(255,255,255,0.5)!important;
    background:rgba(255,255,255,0.12)!important;
}
.stSelectbox>label{font-size:11px!important;font-weight:800!important;color:#374151!important;letter-spacing:0.5px!important;text-transform:uppercase!important;}
.stSelectbox>div>div{background:white!important;border:2px solid #d1d5db!important;border-radius:10px!important;color:#111827!important;font-family:'Nunito',sans-serif!important;font-size:14px!important;}
.stSelectbox>div>div:focus-within{border-color:#16a34a!important;}
.stNumberInput>label{font-size:11px!important;font-weight:800!important;color:#374151!important;letter-spacing:0.5px!important;text-transform:uppercase!important;}
.stNumberInput>div>div>input{background:white!important;border:2px solid #d1d5db!important;border-radius:10px!important;color:#111827!important;font-family:'Nunito',sans-serif!important;font-size:14px!important;padding:10px 14px!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#052e16,#14532d)!important;border-right:none!important;}
[data-testid="stSidebar"] label{color:#86efac!important;font-size:10px!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(134,239,172,0.2)!important;color:#dcfce7!important;border-radius:8px!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOGIN — FULL SCREEN WITH FARM IMAGE
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    lang=st.session_state.lang; tx=T[lang]

    # Inject login-specific styles: full page farm image + dark input overrides
    st.markdown("""
    <style>
    [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important;}

    /* Full page farm background */
    .stApp {
        background-image:
            linear-gradient(135deg, rgba(2,30,8,0.80) 0%, rgba(4,46,16,0.72) 50%, rgba(2,24,6,0.88) 100%),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=90&fit=crop&crop=center') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: scroll !important;
        min-height: 100vh !important;
    }

    /* Make login inputs dark-themed */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 14px !important;
        padding: 13px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4ade80 !important;
        outline: none !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.35) !important;
    }

    /* Login selectbox dark */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stSelectbox > label { color: rgba(255,255,255,0.55) !important; }

    /* Hide streamlit top padding */
    .main .block-container { padding-top: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── TOP NAV ──
    st.markdown(f"""
    <div style="background:rgba(2,30,8,0.55);backdrop-filter:blur(12px);
        padding:14px 36px;display:flex;align-items:center;
        justify-content:space-between;border-bottom:1px solid rgba(74,222,128,0.12);">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;background:linear-gradient(135deg,#16a34a,#4ade80);
                border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;">🥭</div>
            <div>
                <div style="font-family:'Nunito',sans-serif;font-size:22px;font-weight:900;color:white;letter-spacing:-0.5px;">{tx['title']}</div>
                <div style="font-size:10px;color:rgba(74,222,128,0.65);letter-spacing:2px;text-transform:uppercase;">{tx['tagline']}</div>
            </div>
        </div>
        <div>
            <div style="font-size:12px;color:rgba(255,255,255,0.4);">Andhra Pradesh · Telangana · Karnataka</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── HERO + FORM SIDE BY SIDE ──
    hero_col, form_col = st.columns([1.25, 1])

    with hero_col:
        st.markdown(f"""
        <div style="padding:70px 40px 40px 48px;">
            <div style="font-family:'Merriweather',serif;font-size:46px;color:white;font-weight:700;
                line-height:1.18;margin-bottom:18px;letter-spacing:-1px;">
                Find Your Most<br><span style="color:#4ade80;">Profitable</span><br>Mango Market
            </div>
            <p style="font-size:15px;color:rgba(255,255,255,0.6);line-height:1.75;max-width:440px;margin-bottom:32px;">
                {tx['hero_sub']}
            </p>
        </div>""", unsafe_allow_html=True)

    with form_col:
        # Language selector — top right of form column
        lc1,lc2 = st.columns([2,1])
        with lc2:
            c=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],
                index=["English","Telugu","Hindi","Kannada"].index(lang),
                key="lang_sel",label_visibility="collapsed")
            if c!=lang: st.session_state.lang=c; st.rerun()

        # Login card
        st.markdown("""
        <div style="background:rgba(2,20,6,0.78);backdrop-filter:blur(28px);
            border:1px solid rgba(74,222,128,0.15);border-radius:20px;
            padding:36px 36px 30px;margin:10px 36px 20px 0;
            box-shadow:0 32px 80px rgba(0,0,0,0.55);">
        """, unsafe_allow_html=True)

        # Tab buttons
        tb1,tb2 = st.columns(2)
        with tb1:
            if st.button(tx["sign_in"], key="tab_si", use_container_width=True,
                type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login";st.session_state.otp_mode=False
                st.session_state.forgot=False;st.rerun()
        with tb2:
            if st.button(tx["create_account"], key="tab_ca", use_container_width=True,
                type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register";st.session_state.otp_mode=False
                st.session_state.forgot=False;st.rerun()

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        def lbl(text):
            st.markdown(f'<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(74,222,128,0.7);margin-bottom:6px;font-weight:700;">{text}</div>', unsafe_allow_html=True)

        # ── FORGOT PASSWORD ──
        if st.session_state.forgot:
            lbl(tx["reset_pw"])
            fph = st.text_input("_fph", placeholder=tx["phone_ph"], key="fp_ph", label_visibility="collapsed")
            if not st.session_state.f_otp_sent:
                if st.button(tx["send_otp"], key="fp_send", use_container_width=True):
                    if fph and len(fph)==10 and fph.isdigit():
                        u = get_user(fph)
                        if u:
                            code = str(random.randint(100000,999999))
                            st.session_state.f_code=code; st.session_state.f_otp_sent=True
                            st.session_state.otp_phone=fph
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found with this number.")
                    else: st.warning("Enter valid 10-digit number.")
            elif not st.session_state.f_otp_ok:
                lbl(tx["otp_ph"])
                eo = st.text_input("_fov", placeholder=tx["otp_ph"], key="fp_ov", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="fp_ver", use_container_width=True):
                    if eo==st.session_state.f_code: st.session_state.f_otp_ok=True; st.rerun()
                    else: st.error("Incorrect OTP.")
            else:
                lbl(tx["new_pw"])
                np_ = st.text_input("_npw", placeholder=tx["new_pw"], type="password", key="fp_np", label_visibility="collapsed")
                lbl(tx["conf_pw"])
                cp_ = st.text_input("_cpw", placeholder=tx["conf_pw"], type="password", key="fp_cp", label_visibility="collapsed")
                if st.button(tx["upd_pw"], key="fp_upd", use_container_width=True):
                    if np_ and np_==cp_:
                        update_pw(st.session_state.otp_phone, np_)
                        st.success("Password updated. Please sign in.")
                        st.session_state.forgot=False; st.session_state.f_otp_sent=False
                        st.session_state.f_otp_ok=False; st.session_state.f_code=None; st.rerun()
                    else: st.error("Passwords do not match.")
            if st.button(tx["back"], key="fp_back", use_container_width=True, type="secondary"):
                st.session_state.forgot=False; st.rerun()

        # ── OTP LOGIN ──
        elif st.session_state.auth_mode=="login" and st.session_state.otp_mode:
            lbl(tx["phone"])
            op = st.text_input("_op", placeholder=tx["phone_ph"], key="otp_ph_in", label_visibility="collapsed")
            if not st.session_state.otp_sent:
                if st.button(tx["send_otp"], key="s_otp", use_container_width=True):
                    if op and len(op)==10 and op.isdigit():
                        u = get_user(op)
                        if u:
                            code = str(random.randint(100000,999999))
                            st.session_state.otp_code=code; st.session_state.otp_sent=True
                            st.session_state.otp_phone=op
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            else:
                lbl(tx["otp_ph"])
                eo = st.text_input("_eov", placeholder=tx["otp_ph"], key="otp_v", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="v_otp", use_container_width=True):
                    if eo==st.session_state.otp_code:
                        u = get_user(st.session_state.otp_phone)
                        st.session_state.logged_in=True; st.session_state.user=u
                        st.session_state.otp_sent=False; st.rerun()
                    else: st.error("Incorrect OTP.")
            if st.button(tx["use_pw"], key="use_pw_btn", use_container_width=True, type="secondary"):
                st.session_state.otp_mode=False; st.rerun()

        # ── PASSWORD LOGIN ──
        elif st.session_state.auth_mode=="login":
            lbl(tx["phone"])
            ph = st.text_input("_lph", placeholder=tx["phone_ph"], key="l_ph", label_visibility="collapsed")
            lbl(tx["password"])
            pw = st.text_input("_lpw", placeholder=tx["pass_ph"], type="password", key="l_pw", label_visibility="collapsed")
            if st.button(tx["login_btn"], key="do_login", use_container_width=True):
                if ph and pw:
                    u = login_user(ph, pw)
                    if u: st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
                    else: st.error("Incorrect phone or password.")
                else: st.warning("Please fill all fields.")
            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
            fa, oa = st.columns(2)
            with fa:
                if st.button(tx["forgot"], key="frg_btn", use_container_width=True, type="secondary"):
                    st.session_state.forgot=True; st.rerun()
            with oa:
                if st.button(tx["otp_opt"], key="otp_sw", use_container_width=True, type="secondary"):
                    st.session_state.otp_mode=True; st.rerun()

        # ── REGISTER ──
        else:
            for label,key_,ph_,is_pw in [
                (tx["name"],"r_nm","Your full name",False),
                (tx["place"],"r_pl","Village, Mandal, District",False),
                (tx["phone"],"r_ph",tx["phone_ph"],False),
                (tx["password"],"r_pw",tx["pass_ph"],True),
            ]:
                lbl(label)
                if is_pw: st.text_input(f"_{key_}",placeholder=ph_,key=key_,type="password",label_visibility="collapsed")
                else: st.text_input(f"_{key_}",placeholder=ph_,key=key_,label_visibility="collapsed")
            if st.button(tx["reg_btn"], key="do_reg", use_container_width=True):
                n=st.session_state.get("r_nm",""); p=st.session_state.get("r_pl","")
                ph=st.session_state.get("r_ph",""); pw=st.session_state.get("r_pw","")
                if n and p and ph and pw:
                    if register_user(n,p,ph,pw):
                        st.success("Account created! Please sign in.")
                        st.session_state.auth_mode="login"; st.rerun()
                    else: st.error("Phone number already registered.")
                else: st.warning("All fields are required.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:10px;font-size:10px;color:rgba(255,255,255,0.2);letter-spacing:1.5px;">SECURE · ENCRYPTED · YOUR DATA IS SAFE</div>', unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_all():
    def safe(p):
        try:
            df=pd.read_csv(p); df.columns=df.columns.str.strip().str.lower(); return df
        except: return pd.DataFrame()
    return (safe("Village data.csv"),safe("cleaned_price_data.csv"),
            safe("cleaned_mandi_location.csv"),safe("cleaned_processing_facilities.csv"),
            safe("Pulp_units_merged_lat_long.csv"),safe("cleaned_pickle_units.csv"),
            safe("cleaned_local_export.csv"),safe("cleaned_abroad_export.csv"),
            safe("cleaned_cold_storage.csv"),safe("cleaned_fpo.csv"))

villages,prices,geo,processing,pulp,pickle_u,local_exp,abroad_exp,cold,fpo=load_all()

def haversine(la1,lo1,la2,lo2):
    R=6371; la1,lo1,la2,lo2=map(np.radians,[la1,lo1,la2,lo2])
    d=np.sin((la2-la1)/2)**2+np.cos(la1)*np.cos(la2)*np.sin((lo2-lo1)/2)**2
    return R*2*np.arcsin(np.sqrt(d))

def dcols(df):
    nm=la=lo=None
    for c in df.columns:
        cl=c.lower()
        if "lat" in cl and la is None: la=c
        if ("lon" in cl or "lng" in cl) and lo is None: lo=c
        if any(x in cl for x in ["name","firm","facility","hub","market","place","panchayat","company","unit","mandal"]) and nm is None: nm=c
    if nm is None and len(df.columns)>0: nm=df.columns[0]
    return nm,la,lo

def village_list():
    nc,_,_=dcols(villages)
    if nc and nc in villages.columns: return sorted(villages[nc].dropna().unique().tolist())
    return ["Default Village"]

def village_coords(vname):
    nc,lc,loc=dcols(villages)
    if nc and lc and loc:
        r=villages[villages[nc]==vname]
        if not r.empty: return float(r.iloc[0][lc]),float(r.iloc[0][loc])
    return 15.9129,79.7400

def get_base_price(vlat,vlon):
    try:
        m=prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices.copy()
        lc=next((c for c in m.columns if "lat" in c.lower()),None)
        loc=next((c for c in m.columns if "lon" in c.lower()),None)
        pc=next((c for c in m.columns if "price" in c.lower()),None)
        if lc and loc and pc:
            m=m.dropna(subset=[lc,loc,pc])
            m["d"]=m.apply(lambda r:haversine(vlat,vlon,r[lc],r[loc]),axis=1)
            return float(m.loc[m["d"].idxmin()][pc])
    except: pass
    return 25.0

def get_osm_route(lat1,lon1,lat2,lon2):
    try:
        url=(f"http://router.project-osrm.org/route/v1/driving/"
             f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson")
        r=requests.get(url,timeout=8)
        data=r.json()
        if "routes" in data and data["routes"]:
            route=data["routes"][0]
            coords=[(c[1],c[0]) for c in route["geometry"]["coordinates"]]
            dist_km=round(route["distance"]/1000,2)
            return coords,dist_km
    except: pass
    return [(lat1,lon1),(lat2,lon2)], round(haversine(lat1,lon1,lat2,lon2),2)

def get_road_dist(vlat,vlon,rlat,rlon):
    try:
        url=(f"http://router.project-osrm.org/route/v1/driving/"
             f"{vlon},{vlat};{rlon},{rlat}?overview=false")
        r=requests.get(url,timeout=5)
        data=r.json()
        if "routes" in data and data["routes"]:
            return round(data["routes"][0]["distance"]/1000,2)
    except: pass
    return round(haversine(vlat,vlon,rlat,rlon),2)

def run_analysis(vlat,vlon,variety,tonnes):
    VACC={"Mandi":["Banganapalli","Totapuri","Neelam","Rasalu"],
          "Processing":["Totapuri","Neelam"],"Pulp":["Totapuri"],
          "Pickle":["Totapuri","Rasalu"],"Local Export":["Banganapalli"],
          "Abroad Export":["Banganapalli"],
          "Cold Storage":["Banganapalli","Totapuri","Neelam","Rasalu"],
          "FPO":["Banganapalli","Totapuri","Neelam","Rasalu"]}
    mdf=prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices
    CATS={
        "Mandi":      {"mg":0.00,"col":"#3b82f6","ic":"🏪","df":mdf},
        "Processing": {"mg":0.03,"col":"#7c3aed","ic":"🏭","df":processing},
        "Pulp":       {"mg":0.04,"col":"#d97706","ic":"🧃","df":pulp},
        "Pickle":     {"mg":0.025,"col":"#db2777","ic":"🫙","df":pickle_u},
        "Local Export":{"mg":0.05,"col":"#16a34a","ic":"🚛","df":local_exp},
        "Abroad Export":{"mg":0.07,"col":"#b45309","ic":"✈️","df":abroad_exp},
        "Cold Storage":{"mg":0.01,"col":"#0891b2","ic":"🧊","df":cold},
        "FPO":        {"mg":0.02,"col":"#65a30d","ic":"👥","df":fpo},
    }
    HND={"Mandi":0,"Processing":300,"Pulp":400,"Pickle":250,"Local Export":500,"Abroad Export":700,"Cold Storage":200,"FPO":150}
    DLY={"Mandi":0,"Processing":7,"Pulp":10,"Pickle":5,"Local Export":14,"Abroad Export":30,"Cold Storage":3,"FPO":2}
    bp=get_base_price(vlat,vlon); rows=[]
    for cat,cfg in CATS.items():
        if variety not in VACC.get(cat,[]): continue
        df_=cfg["df"]
        if df_ is None or df_.empty: continue
        nc,lc,loc=dcols(df_)
        if not lc or not loc: continue
        for _,row in df_.iterrows():
            try:
                rlat=float(row[lc]); rlon=float(row[loc])
                if haversine(vlat,vlon,rlat,rlon)>150: continue
                dist=get_road_dist(vlat,vlon,rlat,rlon)
                nm=str(row[nc]) if nc and nc in row.index else cat
                adj=bp*(1+cfg["mg"]); rev=adj*1000*tonnes
                tra=5000+dist*200*tonnes+300*tonnes
                fin=rev*(DLY.get(cat,0)/365)*0.12
                rr=(0.004*(dist/10))+0.002; rc=rev*rr
                net=rev-tra-HND.get(cat,0)*tonnes-fin-rc
                rows.append({"Type":cat,"Name":nm,"Dist_km":dist,
                             "Revenue":round(rev),"Transport":round(tra),
                             "Risk_pct":round(rr*100,2),"Net_Profit":round(net),
                             "Lat":rlat,"Lon":rlon,"color":cfg["col"],"icon":cfg["ic"]})
            except: continue
    if not rows: return pd.DataFrame()
    df=pd.DataFrame(rows).drop_duplicates(subset=["Type","Name"])
    df=df.sort_values("Net_Profit",ascending=False).reset_index(drop=True)
    df["Rank"]=df.index+1
    return df

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
lang=st.session_state.get("lang","English"); tx=T[lang]
fname=st.session_state.user[0]; fplace=st.session_state.user[1]

# Dashboard background
st.markdown("<style>.stApp{background:#f0f4f0!important;}</style>", unsafe_allow_html=True)

# ── TOP NAV ──
st.markdown(f"""
<div style="background:linear-gradient(135deg,#052e16 0%,#14532d 100%);
    padding:0 28px;height:66px;display:flex;align-items:center;
    justify-content:space-between;box-shadow:0 4px 24px rgba(0,0,0,0.25);
    position:sticky;top:0;z-index:999;">
    <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:42px;height:42px;background:linear-gradient(135deg,#16a34a,#4ade80);
            border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:22px;">🥭</div>
        <div>
            <div style="font-family:'Nunito',sans-serif;font-size:22px;font-weight:900;color:white;letter-spacing:-0.5px;">{tx['title']}</div>
            <div style="font-size:9px;color:rgba(74,222,128,0.6);letter-spacing:2.5px;text-transform:uppercase;">Farmer Profit Intelligence</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:38px;height:38px;background:rgba(74,222,128,0.15);
            border:2px solid rgba(74,222,128,0.35);border-radius:50%;
            display:flex;align-items:center;justify-content:center;
            font-size:14px;font-weight:900;color:#4ade80;">{fname[0].upper()}</div>
        <div>
            <div style="font-size:13px;color:white;font-weight:700;">{fname}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.4);">📍 {fplace}</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""<div style="padding:16px 2px 10px;">
        <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#86efac;
            margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(134,239,172,0.1);">Settings</div>
    </div>""", unsafe_allow_html=True)
    sl=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],
                     index=["English","Telugu","Hindi","Kannada"].index(lang))
    if sl!=lang: st.session_state.lang=sl; st.rerun()

    st.markdown(f'<div style="margin-top:16px;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#86efac;margin-bottom:10px;">{tx["live_prices"]}</div>', unsafe_allow_html=True)
    for v,(p,tr,cl) in {"Banganapalli":(28,"↑ +2.1%","#4ade80"),"Totapuri":(18,"↓ -0.8%","#f87171"),
                         "Neelam":(22,"↑ +1.4%","#4ade80"),"Rasalu":(30,"↑ +3.2%","#4ade80")}.items():
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
            padding:8px 10px;margin-bottom:5px;background:rgba(255,255,255,0.05);
            border-radius:8px;border:1px solid rgba(255,255,255,0.06);">
            <div><div style="font-size:12px;color:#dcfce7;font-weight:700;">{v}</div>
            <div style="font-size:10px;color:#86efac;">₹{p}/kg</div></div>
            <div style="font-size:12px;font-weight:800;color:{cl};">{tr}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    if st.button(tx["logout"], use_container_width=True, type="secondary"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════
# HERO + FORM (no technical jargon shown to user)
# ══════════════════════════════════════════════════════════════
vlist=village_list()
sel_variety_now = st.session_state.get("sel_var","Banganapalli")

st.markdown(f"""
<div style="
    background-image:
        linear-gradient(rgba(2,44,8,0.68),rgba(5,46,22,0.75)),
        url('https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=1400&q=85&fit=crop&crop=center');
    background-size:cover;background-position:center;
    padding:44px 32px 36px;">
    <div style="max-width:520px;">
        <h1 style="font-family:'Merriweather',serif;font-size:36px;color:white;
            font-weight:700;line-height:1.22;margin-bottom:10px;">
            {tx['fill_details']}
        </h1>
        <p style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.7;">{tx['hero_sub']}</p>
    </div>
</div>""", unsafe_allow_html=True)

# ── PRICES TICKER ──
st.markdown(f"""
<div style="background:#052e16;padding:11px 32px;border-bottom:1px solid rgba(74,222,128,0.1);">
    <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
        <span style="font-size:10px;font-weight:800;color:#4ade80;letter-spacing:2px;text-transform:uppercase;margin-right:8px;">{tx['live_prices']}</span>
        <span style="font-size:12px;color:white;font-weight:600;">Banganapalli <b style="color:#4ade80;">₹28</b> ↑+2.1%</span>
        <span style="color:rgba(74,222,128,0.2);margin:0 10px;">|</span>
        <span style="font-size:12px;color:white;font-weight:600;">Totapuri <b style="color:#f87171;">₹18</b> ↓-0.8%</span>
        <span style="color:rgba(74,222,128,0.2);margin:0 10px;">|</span>
        <span style="font-size:12px;color:white;font-weight:600;">Neelam <b style="color:#4ade80;">₹22</b> ↑+1.4%</span>
        <span style="color:rgba(74,222,128,0.2);margin:0 10px;">|</span>
        <span style="font-size:12px;color:white;font-weight:600;">Rasalu <b style="color:#4ade80;">₹30</b> ↑+3.2%</span>
    </div>
</div>""", unsafe_allow_html=True)

# ── MAIN CONTENT AREA ──
st.markdown('<div style="padding:0 28px 36px;background:#f0f4f0;">', unsafe_allow_html=True)

# ── INPUT FORM ──
st.markdown(f"""
<div style="background:white;border-radius:16px;padding:24px 28px 20px;
    box-shadow:0 8px 32px rgba(0,0,0,0.1);border:1px solid #e5e7eb;
    margin-top:0;margin-bottom:22px;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;
        padding-bottom:14px;border-bottom:2px solid #f0f4f0;">
        <div style="width:34px;height:34px;background:#052e16;border-radius:8px;
            display:flex;align-items:center;justify-content:center;font-size:17px;">🌾</div>
        <div style="font-size:16px;font-weight:900;color:#052e16;">{tx['fill_details']}</div>
    </div>
</div>""", unsafe_allow_html=True)

fc1,fc2,fc3,fc4 = st.columns([2.2,1.8,1,1.6])
with fc1:
    st.markdown(f'<p style="font-size:11px;font-weight:800;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">📍 {tx["village_sel"]}</p>', unsafe_allow_html=True)
    sel_village = st.selectbox("__v", vlist, key="sel_v", label_visibility="collapsed")
with fc2:
    st.markdown(f'<p style="font-size:11px;font-weight:800;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">🥭 {tx["variety"]}</p>', unsafe_allow_html=True)
    sel_variety = st.selectbox("__var", ["Banganapalli","Totapuri","Neelam","Rasalu"], key="sel_var", label_visibility="collapsed")
with fc3:
    st.markdown(f'<p style="font-size:11px;font-weight:800;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">⚖️ {tx["quantity"]}</p>', unsafe_allow_html=True)
    sel_tonnes = st.number_input("__t", min_value=0.5, value=10.0, step=0.5, key="sel_t", label_visibility="collapsed")
with fc4:
    st.markdown('<p style="font-size:11px;font-weight:800;color:transparent;margin-bottom:4px;">.</p>', unsafe_allow_html=True)
    run_clicked = st.button(f"🔍  {tx['analyze_btn']}", key="run_btn", use_container_width=True)

if run_clicked:
    st.session_state.run=True
    st.session_state.last_village=sel_village
    st.session_state.last_variety=sel_variety
    st.session_state.last_tonnes=sel_tonnes

# ══════════════════════════════════════════════════════════════
# RESULTS — TOP 3 ONLY
# ══════════════════════════════════════════════════════════════
if st.session_state.get("run", False):
    rv  = st.session_state.get("last_village", sel_village)
    rvar= st.session_state.get("last_variety", sel_variety)
    rt  = st.session_state.get("last_tonnes",  sel_tonnes)

    with st.spinner("Analysing all nearby markets..."):
        vlat,vlon = village_coords(rv)
        df_res = run_analysis(vlat,vlon,rvar,rt)

    if df_res.empty:
        st.warning(tx["no_results"])
    else:
        top3 = df_res.head(3)
        bn=int(top3.iloc[0]["Net_Profit"])
        bd=top3.iloc[0]["Name"]
        bc=top3.iloc[0]["Type"]

        # ── SUMMARY BANNER ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#052e16,#14532d);border-radius:16px;
            padding:24px 32px;margin-bottom:22px;
            border:1px solid rgba(74,222,128,0.15);position:relative;overflow:hidden;">
            <div style="position:absolute;right:28px;top:50%;transform:translateY(-50%);
                font-size:80px;opacity:0.06;pointer-events:none;">🏆</div>
            <div style="font-size:9px;letter-spacing:3px;text-transform:uppercase;
                color:#4ade80;margin-bottom:10px;font-weight:800;">{tx['profit_summary']}</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
                <div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px;">{tx['variety_lbl']}</div>
                    <div style="font-size:20px;font-weight:900;color:white;">{rvar}</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px;">{tx['qty_lbl']}</div>
                    <div style="font-size:20px;font-weight:900;color:white;">{rt} Tonnes</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px;">{tx['best_market']}</div>
                    <div style="font-size:16px;font-weight:800;color:#4ade80;line-height:1.25;">{bd}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.4);">{bc}</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px;">{tx['est_profit']}</div>
                    <div style="font-size:32px;font-weight:900;color:#4ade80;">₹{bn:,}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── TOP 3 CARDS ──
        st.markdown(f'<div style="font-size:11px;font-weight:900;color:#052e16;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;"><span style="display:inline-block;width:4px;height:20px;background:#16a34a;border-radius:2px;"></span>{tx["top3"]}</div>', unsafe_allow_html=True)

        medals=[
            ("#f59e0b",tx["highest_profit"],True,"🥇","linear-gradient(145deg,#052e16,#14532d)"),
            ("#9ca3af",tx["second_best"],False,"🥈","white"),
            ("#b45309",tx["third_best"],False,"🥉","white"),
        ]
        c3 = st.columns(3)
        for i,(col,(acc,lbl_,istop,med,bg)) in enumerate(zip(c3,medals)):
            if i>=len(top3): break
            r = top3.iloc[i]
            with col:
                st.markdown(f"""
                <div style="background:{bg};border-radius:16px;padding:22px;height:100%;
                    border:{'2px solid rgba(245,158,11,0.4)' if istop else '1px solid #e5e7eb'};
                    box-shadow:{'0 16px 48px rgba(5,46,22,0.22)' if istop else '0 4px 18px rgba(0,0,0,0.07)'};
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:12px;right:14px;font-size:26px;opacity:0.15;">{med}</div>
                    <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;
                        color:{acc};margin-bottom:10px;font-weight:900;">{lbl_}</div>
                    <div style="font-size:16px;font-weight:800;
                        color:{'#f0fdf4' if istop else '#052e16'};
                        margin-bottom:4px;line-height:1.3;">{r['Name']}</div>
                    <div style="display:inline-flex;align-items:center;gap:5px;
                        background:{'rgba(255,255,255,0.08)' if istop else '#f0fdf4'};
                        border-radius:6px;padding:3px 10px;margin-bottom:16px;">
                        <span style="font-size:13px;">{r['icon']}</span>
                        <span style="font-size:10px;color:{r['color']};font-weight:800;">{r['Type']}</span>
                    </div>
                    <div style="font-size:30px;font-weight:900;color:{acc};margin-bottom:2px;">₹{int(r['Net_Profit']):,}</div>
                    <div style="font-size:11px;color:{'rgba(255,255,255,0.35)' if istop else '#9ca3af'};margin-bottom:16px;">
                        {r['Dist_km']} {tx['away_lbl']}
                    </div>
                    <div style="border-top:1px solid {'rgba(255,255,255,0.07)' if istop else '#f3f4f6'};
                        padding-top:14px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.38)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['revenue_lbl']}</div>
                            <div style="font-size:12px;font-weight:800;color:{'rgba(255,255,255,0.85)' if istop else '#16a34a'};">₹{int(r['Revenue']):,}</div>
                        </div>
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.38)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['transport_lbl']}</div>
                            <div style="font-size:12px;font-weight:800;color:#ef4444;">₹{int(r['Transport']):,}</div>
                        </div>
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.38)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['risk']}</div>
                            <div style="font-size:12px;font-weight:800;color:#f59e0b;">{r['Risk_pct']}%</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)

        # ── EXPERT TIP ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:12px;
            padding:14px 20px;margin-bottom:22px;border-left:4px solid #f59e0b;
            display:flex;align-items:flex-start;gap:12px;">
            <span style="font-size:20px;flex-shrink:0;">💡</span>
            <div>
                <div style="font-size:11px;font-weight:900;color:#92400e;letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">{tx['farmer_tip']}</div>
                <div style="font-size:13px;color:#78350f;line-height:1.6;">{tx['tip_text']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── CHARTS ──
        cc1,cc2 = st.columns([3,2])
        with cc1:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);"><div style="font-size:13px;font-weight:900;color:#052e16;margin-bottom:14px;">{tx["bar_title"]}</div>', unsafe_allow_html=True)
            fig=go.Figure(go.Bar(
                y=top3["Name"], x=top3["Net_Profit"], orientation="h",
                marker=dict(color=["#f59e0b","#9ca3af","#b45309"], line=dict(width=0)),
                text=[f"₹{int(v):,}" for v in top3["Net_Profit"]],
                textposition="outside", textfont=dict(size=12,color="#374151",family="Nunito"),
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>",
            ))
            fig.update_layout(height=220,paper_bgcolor="white",plot_bgcolor="white",
                margin=dict(l=0,r=90,t=4,b=4),font=dict(family="Nunito"),
                xaxis=dict(showgrid=True,gridcolor="#f0f4f0",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
                yaxis=dict(autorange="reversed",tickfont=dict(size=12,color="#052e16",family="Nunito")),
                hoverlabel=dict(bgcolor="#052e16",bordercolor="#4ade80",font=dict(color="white")))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cc2:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);"><div style="font-size:13px;font-weight:900;color:#052e16;margin-bottom:14px;">{tx["pie_title"]}</div>', unsafe_allow_html=True)
            pdata=top3.groupby("Type")["Net_Profit"].sum().reset_index()
            cmap={"Mandi":"#3b82f6","Processing":"#7c3aed","Pulp":"#d97706","Pickle":"#db2777",
                  "Local Export":"#16a34a","Abroad Export":"#b45309","Cold Storage":"#0891b2","FPO":"#65a30d"}
            fig2=go.Figure(go.Pie(
                labels=pdata["Type"], values=pdata["Net_Profit"], hole=0.55,
                marker=dict(colors=[cmap.get(c,"#888") for c in pdata["Type"]],line=dict(color="white",width=2.5)),
                textinfo="percent+label", textfont=dict(size=11,family="Nunito"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} · %{percent}<extra></extra>",
            ))
            fig2.update_layout(height=220,paper_bgcolor="white",margin=dict(l=8,r=8,t=4,b=4),
                legend=dict(font=dict(size=10,family="Nunito"),orientation="v",x=1.0,y=0.5),
                font=dict(family="Nunito"),
                annotations=[dict(text=f"<b>{rvar}</b>",x=0.5,y=0.5,font=dict(size=12,color="#052e16"),showarrow=False)],
                hoverlabel=dict(bgcolor="#052e16",bordercolor="#4ade80",font=dict(color="white")))
            st.plotly_chart(fig2,use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        # ── TABLE (TOP 3) ──
        st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:22px;"><div style="font-size:13px;font-weight:900;color:#052e16;margin-bottom:14px;">📋 {tx["top3"]} — Detailed Breakdown</div>', unsafe_allow_html=True)
        disp=top3[["Rank","Name","Type","Dist_km","Revenue","Transport","Risk_pct","Net_Profit"]].copy()
        disp.columns=[tx["rank"],tx["dest"],tx["cat"],tx["dist_km"],tx["rev"],tx["trans"],tx["risk"],tx["net"]]
        disp[tx["rev"]]    = disp[tx["rev"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["trans"]]  = disp[tx["trans"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["net"]]    = disp[tx["net"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["dist_km"]]= disp[tx["dist_km"]].apply(lambda x: f"{x:.1f} km")
        disp[tx["risk"]]   = disp[tx["risk"]].apply(lambda x: f"{x:.2f}%")
        st.dataframe(disp, use_container_width=True, height=176, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── MAP WITH REAL OSM ROUTES ──
        st.markdown(f'<div style="font-size:11px;font-weight:900;color:#052e16;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:8px;"><span style="display:inline-block;width:4px;height:20px;background:#16a34a;border-radius:2px;"></span>{tx["map_title"]}</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:white;border-radius:16px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 20px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#6b7280;margin-bottom:12px;">🏠 Your farm &nbsp;&nbsp;★ Best market &nbsp;&nbsp;Colored dots = other top markets</div>', unsafe_allow_html=True)

        br=top3.iloc[0]
        m=folium.Map(location=[vlat,vlon], zoom_start=9, tiles="CartoDB Positron")

        # Farmer
        folium.Marker([vlat,vlon],
            popup=folium.Popup(f"<b>{fname}</b><br>📍 {rv}", max_width=200),
            tooltip=tx["your_loc"],
            icon=folium.DivIcon(html="""
            <div style="background:#052e16;border:3px solid #4ade80;border-radius:50%;
                width:40px;height:40px;display:flex;align-items:center;justify-content:center;
                font-size:18px;box-shadow:0 3px 14px rgba(0,0,0,0.5);">🏠</div>
            """, icon_size=(40,40), icon_anchor=(20,20))
        ).add_to(m)

        route_colors=["#f59e0b","#9ca3af","#b45309"]
        for i,(_,row) in enumerate(top3.iterrows()):
            is_best=(i==0)
            rcol=route_colors[i]
            # Real OSM road route
            route_coords,road_dist = get_osm_route(vlat,vlon,row["Lat"],row["Lon"])
            folium.PolyLine(
                route_coords, color=rcol,
                weight=5 if is_best else 3,
                opacity=0.92 if is_best else 0.55,
                dash_array=None if is_best else "8 5",
            ).add_to(m)
            if is_best:
                folium.Marker([row["Lat"],row["Lon"]],
                    popup=folium.Popup(
                        f"<b>{row['Name']}</b><br>{row['Type']}<br>"
                        f"<span style='color:#16a34a;font-weight:700;font-size:14px'>₹{int(row['Net_Profit']):,}</span>",
                        max_width=220),
                    tooltip=f"★ {row['Name']}",
                    icon=folium.DivIcon(html="""
                    <div style="background:#f59e0b;border:3px solid white;border-radius:50%;
                        width:42px;height:42px;display:flex;align-items:center;justify-content:center;
                        font-size:21px;font-weight:900;color:#1a1a1a;
                        box-shadow:0 4px 16px rgba(245,158,11,0.65);">★</div>
                    """, icon_size=(42,42), icon_anchor=(21,21))
                ).add_to(m)
            else:
                folium.CircleMarker(
                    [row["Lat"],row["Lon"]], radius=11,
                    color=rcol, fill=True, fill_color=rcol, fill_opacity=0.9, weight=3,
                    popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br>₹{int(row['Net_Profit']):,}", max_width=200),
                    tooltip=f"#{i+1} — {row['Name']}",
                ).add_to(m)

        st_folium(m, width=None, height=540, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── FOOTER ──
st.markdown(f"""
<div style="background:#052e16;padding:20px 32px;margin-top:24px;text-align:center;">
    <div style="font-size:15px;font-weight:900;color:white;margin-bottom:3px;">🥭 {tx['title']}</div>
    <div style="font-size:10px;color:rgba(74,222,128,0.35);letter-spacing:1px;">
        © 2025 · Smart Farmer Profit Intelligence · AP · Telangana · Karnataka
    </div>
</div>""", unsafe_allow_html=True)
