import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import numpy as np
import random
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="Mango Profit Navigator",
                   page_icon="🥭", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English": {
        "title":"Mango Profit Navigator","tagline":"Agricultural Intelligence Platform",
        "sign_in":"Sign In","create_account":"Create Account",
        "phone":"Phone Number","password":"Password",
        "phone_ph":"Enter 10-digit mobile number","pass_ph":"Enter your password",
        "login_btn":"Sign In","forgot":"Forgot Password?",
        "otp_opt":"Sign in with OTP","send_otp":"Send OTP",
        "verify_otp":"Verify OTP","otp_ph":"Enter 6-digit OTP",
        "name":"Full Name","place":"Village / District","reg_btn":"Create Account",
        "select_lang":"Language","village_sel":"Select Village",
        "variety":"Mango Variety","quantity":"Quantity (Tonnes)",
        "analyze_btn":"Run Smart Analysis",
        "top3":"Top 3 Most Profitable Destinations",
        "bar_title":"Net Profit by Destination","pie_title":"Market Category Share",
        "map_title":"Route Map to Best Destination","table_title":"All Destinations Compared",
        "rank":"Rank","dest":"Destination","cat":"Category",
        "dist_km":"Distance (km)","rev":"Revenue (₹)","trans":"Transport (₹)",
        "risk":"Risk (%)","net":"Net Profit (₹)",
        "logout":"Sign Out","reset_pw":"Reset Password",
        "new_pw":"New Password","conf_pw":"Confirm Password","upd_pw":"Update Password",
        "back":"Back to Sign In","use_pw":"Use password instead",
        "live_market":"Live Market Prices",
        "highest_profit":"HIGHEST PROFIT","second_best":"2ND BEST","third_best":"3RD BEST",
        "net_profit_lbl":"Net Profit","away_lbl":"km away",
        "your_loc":"Your Farm","best_dest":"Best Destination",
        "revenue_lbl":"Revenue","transport_lbl":"Transport",
        "profit_summary":"Your Profit Summary",
        "variety_lbl":"Variety","qty_lbl":"Quantity",
        "best_market":"Best Market","est_profit":"Estimated Profit",
        "farmer_tip":"Farmer Tip",
        "tip_text":"Abroad Export gives highest premium (+7%) but needs quality certification. Local Export is the easiest entry point.",
        "no_results":"No markets found within 150km. Try a different village or variety.",
        "welcome":"Welcome back",
        "hero_sub":"Select your village, variety and quantity below, then click Run Smart Analysis.",
        "fill_details":"Your Farm Details",
    },
    "Telugu": {
        "title":"మామిడి లాభం నావిగేటర్","tagline":"వ్యవసాయ సమాచార వేదిక",
        "sign_in":"లాగిన్","create_account":"ఖాతా తెరవండి",
        "phone":"ఫోన్ నంబర్","password":"పాస్‌వర్డ్",
        "phone_ph":"10 అంకెల నంబర్","pass_ph":"పాస్‌వర్డ్ నమోదు చేయండి",
        "login_btn":"లాగిన్ చేయండి","forgot":"పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt":"OTP తో లాగిన్","send_otp":"OTP పంపండి",
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"6 అంకెల OTP",
        "name":"పూర్తి పేరు","place":"గ్రామం / జిల్లా","reg_btn":"ఖాతా తెరవండి",
        "select_lang":"భాష","village_sel":"గ్రామం ఎంచుకోండి",
        "variety":"మామిడి రకం","quantity":"పరిమాణం (టన్నులు)",
        "analyze_btn":"స్మార్ట్ విశ్లేషణ అమలు చేయండి",
        "top3":"అగ్ర 3 లాభదాయక గమ్యాలు",
        "bar_title":"గమ్యం వారీగా నికర లాభం","pie_title":"మార్కెట్ వర్గం వాటా",
        "map_title":"ఉత్తమ గమ్యానికి మార్గ మ్యాప్","table_title":"అన్ని గమ్యాల పోలిక",
        "rank":"స్థానం","dest":"గమ్యం","cat":"వర్గం",
        "dist_km":"దూరం (కి.మీ)","rev":"ఆదాయం (₹)","trans":"రవాణా (₹)",
        "risk":"రిస్క్ (%)","net":"నికర లాభం (₹)",
        "logout":"నిష్క్రమించు","reset_pw":"పాస్‌వర్డ్ రీసెట్",
        "new_pw":"కొత్త పాస్‌వర్డ్","conf_pw":"నిర్ధారించండి","upd_pw":"అప్‌డేట్ చేయండి",
        "back":"లాగిన్‌కు తిరిగి","use_pw":"పాస్‌వర్డ్ ఉపయోగించండి",
        "live_market":"ప్రస్తుత మార్కెట్ ధరలు",
        "highest_profit":"అత్యధిక లాభం","second_best":"2వ ఉత్తమం","third_best":"3వ ఉత్తమం",
        "net_profit_lbl":"నికర లాభం","away_lbl":"కి.మీ దూరం",
        "your_loc":"మీ పొలం","best_dest":"ఉత్తమ గమ్యం",
        "revenue_lbl":"ఆదాయం","transport_lbl":"రవాణా",
        "profit_summary":"మీ లాభం సారాంశం",
        "variety_lbl":"రకం","qty_lbl":"పరిమాణం",
        "best_market":"ఉత్తమ మార్కెట్","est_profit":"అంచనా లాభం",
        "farmer_tip":"రైతు సలహా",
        "tip_text":"విదేశీ ఎగుమతి అత్యధిక ప్రీమియం (+7%) ఇస్తుంది కానీ నాణ్యత ధృవీకరణ అవసరం.",
        "no_results":"150 కి.మీ పరిధిలో మార్కెట్లు కనుగొనబడలేదు.",
        "welcome":"స్వాగతం",
        "hero_sub":"క్రింద మీ వివరాలు నమోదు చేసి స్మార్ట్ విశ్లేషణ నొక్కండి.",
        "fill_details":"మీ పొలం వివరాలు",
    },
    "Hindi": {
        "title":"आम लाभ नेविगेटर","tagline":"कृषि बुद्धिमत्ता मंच",
        "sign_in":"साइन इन","create_account":"खाता बनाएं",
        "phone":"फ़ोन नंबर","password":"पासवर्ड",
        "phone_ph":"10 अंकों का नंबर","pass_ph":"पासवर्ड दर्ज करें",
        "login_btn":"साइन इन करें","forgot":"पासवर्ड भूल गए?",
        "otp_opt":"OTP से साइन इन","send_otp":"OTP भेजें",
        "verify_otp":"OTP सत्यापित करें","otp_ph":"6 अंकों का OTP",
        "name":"पूरा नाम","place":"गाँव / जिला","reg_btn":"खाता बनाएं",
        "select_lang":"भाषा","village_sel":"गाँव चुनें",
        "variety":"आम की किस्म","quantity":"मात्रा (टन)",
        "analyze_btn":"स्मार्ट विश्लेषण चलाएं",
        "top3":"शीर्ष 3 लाभदायक गंतव्य",
        "bar_title":"गंतव्य अनुसार शुद्ध लाभ","pie_title":"बाज़ार श्रेणी हिस्सेदारी",
        "map_title":"सर्वोत्तम गंतव्य का मार्ग","table_title":"सभी गंतव्यों की तुलना",
        "rank":"रैंक","dest":"गंतव्य","cat":"श्रेणी",
        "dist_km":"दूरी (कि.मी.)","rev":"राजस्व (₹)","trans":"परिवहन (₹)",
        "risk":"जोखिम (%)","net":"शुद्ध लाभ (₹)",
        "logout":"साइन आउट","reset_pw":"पासवर्ड रीसेट",
        "new_pw":"नया पासवर्ड","conf_pw":"पुष्टि करें","upd_pw":"अपडेट करें",
        "back":"साइन इन पर वापस","use_pw":"पासवर्ड का उपयोग करें",
        "live_market":"लाइव बाज़ार भाव",
        "highest_profit":"सर्वाधिक लाभ","second_best":"दूसरा सर्वश्रेष्ठ","third_best":"तीसरा सर्वश्रेष्ठ",
        "net_profit_lbl":"शुद्ध लाभ","away_lbl":"कि.मी. दूर",
        "your_loc":"आपका खेत","best_dest":"सर्वोत्तम गंतव्य",
        "revenue_lbl":"राजस्व","transport_lbl":"परिवहन",
        "profit_summary":"आपका लाभ सारांश",
        "variety_lbl":"किस्म","qty_lbl":"मात्रा",
        "best_market":"सर्वोत्तम बाज़ार","est_profit":"अनुमानित लाभ",
        "farmer_tip":"किसान सुझाव",
        "tip_text":"विदेश निर्यात सबसे अधिक प्रीमियम (+7%) देता है लेकिन गुणवत्ता प्रमाणीकरण आवश्यक है।",
        "no_results":"150 कि.मी. के भीतर कोई बाज़ार नहीं मिला।",
        "welcome":"स्वागत है",
        "hero_sub":"नीचे अपने विवरण भरें और स्मार्ट विश्लेषण चलाएं।",
        "fill_details":"आपके खेत की जानकारी",
    },
    "Kannada": {
        "title":"ಮಾವಿನ ಲಾಭ ನ್ಯಾವಿಗೇಟರ್","tagline":"ಕೃಷಿ ಬುದ್ಧಿಮತ್ತೆ ವೇದಿಕೆ",
        "sign_in":"ಸೈನ್ ಇನ್","create_account":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "phone":"ಫೋನ್ ಸಂಖ್ಯೆ","password":"ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph":"10 ಅಂಕಿಯ ಸಂಖ್ಯೆ","pass_ph":"ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ",
        "login_btn":"ಸೈನ್ ಇನ್ ಮಾಡಿ","forgot":"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt":"OTP ಮೂಲಕ ಸೈನ್ ಇನ್","send_otp":"OTP ಕಳುಹಿಸಿ",
        "verify_otp":"OTP ಪರಿಶೀಲಿಸಿ","otp_ph":"6 ಅಂಕಿಯ OTP",
        "name":"ಪೂರ್ಣ ಹೆಸರು","place":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ","reg_btn":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "select_lang":"ಭಾಷೆ","village_sel":"ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ",
        "variety":"ಮಾವಿನ ತಳಿ","quantity":"ಪ್ರಮಾಣ (ಟನ್)",
        "analyze_btn":"ಸ್ಮಾರ್ಟ್ ವಿಶ್ಲೇಷಣೆ ಚಲಾಯಿಸಿ",
        "top3":"ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title":"ಗಮ್ಯದ ಪ್ರಕಾರ ನಿವ್ವಳ ಲಾಭ","pie_title":"ಮಾರುಕಟ್ಟೆ ವಿಭಾಗ ಪಾಲು",
        "map_title":"ಉತ್ತಮ ಗಮ್ಯಕ್ಕೆ ಮಾರ್ಗ ನಕ್ಷೆ","table_title":"ಎಲ್ಲಾ ಗಮ್ಯಗಳ ಹೋಲಿಕೆ",
        "rank":"ಶ್ರೇಣಿ","dest":"ಗಮ್ಯ","cat":"ವರ್ಗ",
        "dist_km":"ದೂರ (ಕಿ.ಮೀ)","rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)",
        "risk":"ಅಪಾಯ (%)","net":"ನಿವ್ವಳ ಲಾಭ (₹)",
        "logout":"ಸೈನ್ ಔಟ್","reset_pw":"ಪಾಸ್‌ವರ್ಡ್ ರೀಸೆಟ್",
        "new_pw":"ಹೊಸ ಪಾಸ್‌ವರ್ಡ್","conf_pw":"ದೃಢಪಡಿಸಿ","upd_pw":"ನವೀಕರಿಸಿ",
        "back":"ಸೈನ್ ಇನ್‌ಗೆ ಹಿಂತಿರುಗಿ","use_pw":"ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ",
        "live_market":"ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "highest_profit":"ಅತ್ಯಧಿಕ ಲಾಭ","second_best":"2ನೇ ಉತ್ತಮ","third_best":"3ನೇ ಉತ್ತಮ",
        "net_profit_lbl":"ನಿವ್ವಳ ಲಾಭ","away_lbl":"ಕಿ.ಮೀ ದೂರ",
        "your_loc":"ನಿಮ್ಮ ಹೊಲ","best_dest":"ಉತ್ತಮ ಗಮ್ಯ",
        "revenue_lbl":"ಆದಾಯ","transport_lbl":"ಸಾರಿಗೆ",
        "profit_summary":"ನಿಮ್ಮ ಲಾಭ ಸಾರಾಂಶ",
        "variety_lbl":"ತಳಿ","qty_lbl":"ಪ್ರಮಾಣ",
        "best_market":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ","est_profit":"ಅಂದಾಜು ಲಾಭ",
        "farmer_tip":"ರೈತ ಸಲಹೆ",
        "tip_text":"ವಿದೇಶ ರಫ್ತು ಅತ್ಯಧಿಕ ಪ್ರೀಮಿಯಂ (+7%) ನೀಡುತ್ತದೆ ಆದರೆ ಗುಣಮಟ್ಟ ಪ್ರಮಾಣೀಕರಣ ಅಗತ್ಯ.",
        "no_results":"150 ಕಿ.ಮೀ ಪರಿಧಿಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "welcome":"ಸ್ವಾಗತ",
        "hero_sub":"ಕೆಳಗೆ ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಮತ್ತು ಸ್ಮಾರ್ಟ್ ವಿಶ್ಲೇಷಣೆ ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "fill_details":"ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳು",
    },
}

# ══════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect("farmers.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users
        (name TEXT, place TEXT, phone TEXT PRIMARY KEY, password TEXT)""")
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
}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');
*{box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stDecoration"]{visibility:hidden;display:none!important;}
.stApp{font-family:'Inter',sans-serif;}
.main .block-container{padding:0!important;max-width:100%!important;}
.stTextInput>label{display:none!important;}
.stTextInput>div>div>input{
    background:rgba(255,255,255,0.08)!important;border:1px solid rgba(212,175,55,0.3)!important;
    border-radius:8px!important;color:#f5f0e8!important;font-family:'Inter',sans-serif!important;
    font-size:14px!important;padding:13px 16px!important;transition:all 0.2s!important;
}
.stTextInput>div>div>input:focus{border-color:#d4af37!important;outline:none!important;}
.stTextInput>div>div>input::placeholder{color:rgba(245,240,232,0.3)!important;}
.stButton>button{
    font-family:'Inter',sans-serif!important;font-size:12.5px!important;font-weight:600!important;
    letter-spacing:0.8px!important;text-transform:uppercase!important;border-radius:8px!important;
    padding:12px 18px!important;transition:all 0.22s!important;cursor:pointer!important;
}
.stButton>button:not([kind="secondary"]){
    background:linear-gradient(135deg,#d4af37,#b8942a)!important;color:#0a1a0f!important;
    border:none!important;box-shadow:0 4px 16px rgba(212,175,55,0.28)!important;
}
.stButton>button:not([kind="secondary"]):hover{transform:translateY(-1px)!important;}
.stButton>button[kind="secondary"]{
    background:transparent!important;color:rgba(245,240,232,0.55)!important;
    border:1px solid rgba(212,175,55,0.25)!important;font-size:11px!important;padding:9px 14px!important;
}
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#040e07 0%,#071209 100%)!important;
    border-right:1px solid rgba(212,175,55,0.1)!important;
}
[data-testid="stSidebar"] label{
    color:rgba(212,175,55,0.65)!important;font-size:10px!important;
    letter-spacing:1.5px!important;text-transform:uppercase!important;
}
[data-testid="stSidebar"] .stSelectbox>div>div{
    background:rgba(255,255,255,0.05)!important;border:1px solid rgba(212,175,55,0.16)!important;
    color:#e8e0d0!important;border-radius:8px!important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    lang=st.session_state.lang; tx=T[lang]
    st.markdown("""
    <style>
    [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important;}
    .stApp{
        background:
            linear-gradient(to bottom,rgba(3,10,5,0.78) 0%,rgba(5,15,8,0.68) 50%,rgba(3,8,4,0.85) 100%),
            url('https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=1920&q=90&fit=crop');
        background-size:cover;background-position:center;background-attachment:fixed;
    }
    .stSelectbox>div>div{background:rgba(255,255,255,0.08)!important;border:1px solid rgba(212,175,55,0.3)!important;color:#f5f0e8!important;}
    </style>""", unsafe_allow_html=True)

    _l1,_l2=st.columns([5.5,1])
    with _l2:
        c=st.selectbox("",["English","Telugu","Hindi","Kannada"],
            index=["English","Telugu","Hindi","Kannada"].index(lang),
            key="lang_sel",label_visibility="collapsed")
        if c!=lang: st.session_state.lang=c; st.rerun()

    st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)
    _,mid,_=st.columns([1,1.08,1])
    with mid:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:26px;">
            <div style="font-size:10px;letter-spacing:5px;text-transform:uppercase;color:rgba(212,175,55,0.6);margin-bottom:10px;">Agricultural Intelligence</div>
            <div style="font-family:'Playfair Display',serif;font-size:40px;font-weight:400;color:#f5f0e8;line-height:1.1;">{tx['title']}</div>
            <div style="width:48px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:14px auto 12px;"></div>
            <div style="font-size:10.5px;color:rgba(245,240,232,0.36);letter-spacing:3px;text-transform:uppercase;">{tx['tagline']}</div>
        </div>""",unsafe_allow_html=True)

        st.markdown("""<div style="background:rgba(3,10,6,0.82);backdrop-filter:blur(36px);border:1px solid rgba(212,175,55,0.14);border-radius:16px;padding:36px 36px 30px;box-shadow:0 48px 96px rgba(0,0,0,0.6);">""",unsafe_allow_html=True)

        t1,t2=st.columns(2)
        with t1:
            if st.button(tx["sign_in"],key="tab_si",use_container_width=True,
                type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login";st.session_state.otp_mode=False;st.session_state.forgot=False;st.rerun()
        with t2:
            if st.button(tx["create_account"],key="tab_ca",use_container_width=True,
                type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register";st.session_state.otp_mode=False;st.session_state.forgot=False;st.rerun()

        st.markdown('<div style="height:22px"></div>',unsafe_allow_html=True)

        def lbl(t):
            st.markdown(f'<div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.6);margin-bottom:6px;">{t}</div>',unsafe_allow_html=True)

        if st.session_state.forgot:
            lbl(tx["reset_pw"])
            fph=st.text_input("_fph",placeholder=tx["phone_ph"],key="fp_ph",label_visibility="collapsed")
            if not st.session_state.f_otp_sent:
                if st.button(tx["send_otp"],key="fp_send",use_container_width=True):
                    if fph and len(fph)==10 and fph.isdigit():
                        u=get_user(fph)
                        if u:
                            code=str(random.randint(100000,999999))
                            st.session_state.f_code=code;st.session_state.f_otp_sent=True;st.session_state.otp_phone=fph
                            st.info(f"Demo OTP: **{code}**");st.rerun()
                        else: st.error("No account with this number.")
                    else: st.warning("Enter valid 10-digit number.")
            elif not st.session_state.f_otp_ok:
                lbl(tx["otp_ph"])
                eo=st.text_input("_fov",placeholder=tx["otp_ph"],key="fp_ov",label_visibility="collapsed")
                if st.button(tx["verify_otp"],key="fp_ver",use_container_width=True):
                    if eo==st.session_state.f_code: st.session_state.f_otp_ok=True;st.rerun()
                    else: st.error("Incorrect OTP.")
            else:
                lbl(tx["new_pw"])
                np_=st.text_input("_npw",placeholder=tx["new_pw"],type="password",key="fp_np",label_visibility="collapsed")
                lbl(tx["conf_pw"])
                cp_=st.text_input("_cpw",placeholder=tx["conf_pw"],type="password",key="fp_cp",label_visibility="collapsed")
                if st.button(tx["upd_pw"],key="fp_upd",use_container_width=True):
                    if np_ and np_==cp_:
                        update_pw(st.session_state.otp_phone,np_)
                        st.success("Password updated.")
                        st.session_state.forgot=False;st.session_state.f_otp_sent=False;st.session_state.f_otp_ok=False;st.session_state.f_code=None;st.rerun()
                    else: st.error("Passwords do not match.")
            st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
            if st.button(tx["back"],key="fp_back",use_container_width=True,type="secondary"):
                st.session_state.forgot=False;st.rerun()

        elif st.session_state.auth_mode=="login" and st.session_state.otp_mode:
            lbl(tx["phone"])
            op=st.text_input("_op",placeholder=tx["phone_ph"],key="otp_ph_in",label_visibility="collapsed")
            if not st.session_state.otp_sent:
                if st.button(tx["send_otp"],key="s_otp",use_container_width=True):
                    if op and len(op)==10 and op.isdigit():
                        u=get_user(op)
                        if u:
                            code=str(random.randint(100000,999999))
                            st.session_state.otp_code=code;st.session_state.otp_sent=True;st.session_state.otp_phone=op
                            st.info(f"Demo OTP: **{code}**");st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            else:
                lbl(tx["otp_ph"])
                eo=st.text_input("_eov",placeholder=tx["otp_ph"],key="otp_v",label_visibility="collapsed")
                if st.button(tx["verify_otp"],key="v_otp",use_container_width=True):
                    if eo==st.session_state.otp_code:
                        u=get_user(st.session_state.otp_phone)
                        st.session_state.logged_in=True;st.session_state.user=u;st.session_state.otp_sent=False;st.rerun()
                    else: st.error("Incorrect OTP.")
            st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
            if st.button(tx["use_pw"],key="use_pw_btn",use_container_width=True,type="secondary"):
                st.session_state.otp_mode=False;st.rerun()

        elif st.session_state.auth_mode=="login":
            lbl(tx["phone"])
            ph=st.text_input("_lph",placeholder=tx["phone_ph"],key="l_ph",label_visibility="collapsed")
            lbl(tx["password"])
            pw=st.text_input("_lpw",placeholder=tx["pass_ph"],type="password",key="l_pw",label_visibility="collapsed")
            if st.button(tx["login_btn"],key="do_login",use_container_width=True):
                if ph and pw:
                    u=login_user(ph,pw)
                    if u: st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
                    else: st.error("Incorrect phone or password.")
                else: st.warning("Please fill all fields.")
            st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
            fa,oa=st.columns(2)
            with fa:
                if st.button(tx["forgot"],key="frg_btn",use_container_width=True,type="secondary"):
                    st.session_state.forgot=True;st.rerun()
            with oa:
                if st.button(tx["otp_opt"],key="otp_sw",use_container_width=True,type="secondary"):
                    st.session_state.otp_mode=True;st.rerun()
        else:
            for label,key_,ph_,is_pw in [
                (tx["name"],"r_nm","Full name",False),(tx["place"],"r_pl","Village, District",False),
                (tx["phone"],"r_ph",tx["phone_ph"],False),(tx["password"],"r_pw",tx["pass_ph"],True),
            ]:
                lbl(label)
                if is_pw: st.text_input(f"_{key_}",placeholder=ph_,key=key_,type="password",label_visibility="collapsed")
                else: st.text_input(f"_{key_}",placeholder=ph_,key=key_,label_visibility="collapsed")
            if st.button(tx["reg_btn"],key="do_reg",use_container_width=True):
                n=st.session_state.get("r_nm","");p=st.session_state.get("r_pl","")
                ph=st.session_state.get("r_ph","");pw=st.session_state.get("r_pw","")
                if n and p and ph and pw:
                    if register_user(n,p,ph,pw):
                        st.success("Account created. Please sign in.")
                        st.session_state.auth_mode="login";st.rerun()
                    else: st.error("Phone number already registered.")
                else: st.warning("All fields are required.")

        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("""<div style="text-align:center;margin-top:18px;font-size:10px;color:rgba(245,240,232,0.18);letter-spacing:2px;">SECURE · ENCRYPTED · FARMER DATA PROTECTED</div>""",unsafe_allow_html=True)
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

def run_analysis(vlat,vlon,variety,tonnes):
    VACC={"Mandi":["Banganapalli","Totapuri","Neelam","Rasalu"],
          "Processing":["Totapuri","Neelam"],"Pulp":["Totapuri"],
          "Pickle":["Totapuri","Rasalu"],"Local Export":["Banganapalli"],
          "Abroad Export":["Banganapalli"],
          "Cold Storage":["Banganapalli","Totapuri","Neelam","Rasalu"],
          "FPO":["Banganapalli","Totapuri","Neelam","Rasalu"]}
    CATS={
        "Mandi":{"mg":0.00,"col":"#3b82f6","ic":"🏪","df":prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices},
        "Processing":{"mg":0.03,"col":"#8b5cf6","ic":"🏭","df":processing},
        "Pulp":{"mg":0.04,"col":"#f59e0b","ic":"🧃","df":pulp},
        "Pickle":{"mg":0.025,"col":"#ec4899","ic":"🫙","df":pickle_u},
        "Local Export":{"mg":0.05,"col":"#22c55e","ic":"🚛","df":local_exp},
        "Abroad Export":{"mg":0.07,"col":"#d4af37","ic":"✈️","df":abroad_exp},
        "Cold Storage":{"mg":0.01,"col":"#06b6d4","ic":"🧊","df":cold},
        "FPO":{"mg":0.02,"col":"#84cc16","ic":"👥","df":fpo},
    }
    HND={"Mandi":0,"Processing":300,"Pulp":400,"Pickle":250,"Local Export":500,"Abroad Export":700,"Cold Storage":200,"FPO":150}
    DLY={"Mandi":0,"Processing":7,"Pulp":10,"Pickle":5,"Local Export":14,"Abroad Export":30,"Cold Storage":3,"FPO":2}
    bp=get_base_price(vlat,vlon)
    rows=[]
    for cat,cfg in CATS.items():
        if variety not in VACC.get(cat,[]): continue
        df_=cfg["df"]
        if df_ is None or df_.empty: continue
        nc,lc,loc=dcols(df_)
        if not lc or not loc: continue
        for _,row in df_.iterrows():
            try:
                rlat=float(row[lc]); rlon=float(row[loc])
                dist=haversine(vlat,vlon,rlat,rlon)
                if dist>150: continue
                nm=str(row[nc]) if nc and nc in row.index else cat
                adj=bp*(1+cfg["mg"]); rev=adj*1000*tonnes
                tra=5000+dist*200*tonnes+300*tonnes
                fin=rev*(DLY.get(cat,0)/365)*0.12
                rr=(0.004*(dist/10))+0.002; rc=rev*rr
                net=rev-tra-HND.get(cat,0)*tonnes-fin-rc
                rows.append({"Type":cat,"Name":nm,"Dist_km":round(dist,2),
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

st.markdown("<style>.stApp{background:#eceae4!important;}</style>",unsafe_allow_html=True)

# NAV BAR
st.markdown(f"""
<div style="background:linear-gradient(135deg,#040e07 0%,#0a1c10 60%,#040e07 100%);
    padding:0 32px;height:64px;display:flex;align-items:center;
    justify-content:space-between;border-bottom:1px solid rgba(212,175,55,0.15);
    box-shadow:0 4px 32px rgba(0,0,0,0.3);position:sticky;top:0;z-index:999;">
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:38px;height:38px;background:linear-gradient(135deg,#d4af37,#b8942a);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">🥭</div>
        <div>
            <div style="font-family:'Playfair Display',serif;font-size:18px;color:#f5f0e8;">{tx['title']}</div>
            <div style="font-size:9px;color:rgba(212,175,55,0.5);letter-spacing:3px;text-transform:uppercase;">{tx['tagline']}</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="text-align:right;">
            <div style="font-size:13px;color:#f5f0e8;font-weight:500;">{fname}</div>
            <div style="font-size:10px;color:rgba(212,175,55,0.5);">📍 {fplace}</div>
        </div>
        <div style="width:36px;height:36px;background:rgba(212,175,55,0.12);border:1.5px solid rgba(212,175,55,0.3);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#d4af37;">{fname[0].upper()}</div>
    </div>
</div>""",unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""<div style="padding:18px 2px 10px;"><div style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.45);margin-bottom:14px;border-bottom:1px solid rgba(212,175,55,0.07);padding-bottom:8px;">Settings</div></div>""",unsafe_allow_html=True)
    sl=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],index=["English","Telugu","Hindi","Kannada"].index(lang))
    if sl!=lang: st.session_state.lang=sl;st.rerun()
    st.markdown(f"""<div style="margin-top:16px;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(212,175,55,0.45);margin-bottom:10px;">{tx['live_market']}</div>""",unsafe_allow_html=True)
    for v,(p,tr,cl) in {"Banganapalli":(28,"+2.1%","#22c55e"),"Totapuri":(18,"-0.8%","#ef4444"),"Neelam":(22,"+1.4%","#22c55e"),"Rasalu":(30,"+3.2%","#22c55e")}.items():
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 10px;margin-bottom:5px;background:rgba(255,255,255,0.03);border-radius:7px;"><div><div style="font-size:12px;color:#e8e0d0;">{v}</div><div style="font-size:10px;color:rgba(212,175,55,0.45);">₹{p}/kg</div></div><div style="font-size:12px;font-weight:600;color:{cl};">{tr}</div></div>""",unsafe_allow_html=True)
    st.markdown('<div style="height:12px"></div>',unsafe_allow_html=True)
    if st.button(tx["logout"],use_container_width=True,type="secondary"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════
pad=st.container()
with pad:
    st.markdown('<div style="padding:24px 28px 48px;">',unsafe_allow_html=True)

    # HERO
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(4,14,7,0.95) 0%,rgba(7,24,12,0.92) 100%),url('https://images.unsplash.com/photo-1592991538534-00e70e6a5b3f?w=1400&q=85&fit=crop');background-size:cover;background-position:center;border-radius:16px;padding:32px 36px 28px;margin-bottom:20px;border:1px solid rgba(212,175,55,0.12);position:relative;overflow:hidden;">
        <div style="position:absolute;right:36px;top:50%;transform:translateY(-50%);font-size:100px;opacity:0.06;">🥭</div>
        <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;color:rgba(212,175,55,0.65);margin-bottom:6px;">Dashboard</div>
        <div style="font-family:'Playfair Display',serif;font-size:28px;color:#f5f0e8;font-weight:400;margin-bottom:6px;">{tx['welcome']}, {fname}</div>
        <div style="font-size:13px;color:rgba(245,240,232,0.5);max-width:520px;line-height:1.65;">{tx['hero_sub']}</div>
    </div>""",unsafe_allow_html=True)

    # ══ INPUT FORM ══
    vlist=village_list()

    st.markdown(f"""
    <div style="background:white;border-radius:14px;padding:24px 28px 20px;border:1px solid rgba(0,0,0,0.07);box-shadow:0 4px 20px rgba(0,0,0,0.06);margin-bottom:20px;">
        <div style="font-size:13px;font-weight:700;color:#1a2e1f;margin-bottom:18px;">🌾 &nbsp;{tx['fill_details']}</div>
    </div>""",unsafe_allow_html=True)

    # KEY FIX: use st.columns for form — no HTML wrapper around widgets
    fc1,fc2,fc3,fc4=st.columns([2,1.8,1,1.6])
    with fc1:
        st.markdown(f'<div style="background:white;border-radius:10px;padding:12px 16px 8px;border:1px solid #e5e7eb;margin-top:-52px;margin-bottom:20px;"><div style="font-size:11px;font-weight:600;color:#6b7280;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">📍 {tx["village_sel"]}</div>',unsafe_allow_html=True)
        sel_village=st.selectbox("__v",vlist,key="sel_v",label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)
    with fc2:
        st.markdown(f'<div style="background:white;border-radius:10px;padding:12px 16px 8px;border:1px solid #e5e7eb;margin-top:-52px;margin-bottom:20px;"><div style="font-size:11px;font-weight:600;color:#6b7280;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">🥭 {tx["variety"]}</div>',unsafe_allow_html=True)
        sel_variety=st.selectbox("__var",["Banganapalli","Totapuri","Neelam","Rasalu"],key="sel_var",label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)
    with fc3:
        st.markdown(f'<div style="background:white;border-radius:10px;padding:12px 16px 8px;border:1px solid #e5e7eb;margin-top:-52px;margin-bottom:20px;"><div style="font-size:11px;font-weight:600;color:#6b7280;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">⚖️ {tx["quantity"]}</div>',unsafe_allow_html=True)
        sel_tonnes=st.number_input("__t",min_value=0.5,value=10.0,step=0.5,key="sel_t",label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)
    with fc4:
        st.markdown('<div style="height:36px"></div>',unsafe_allow_html=True)
        run_clicked=st.button(f"🔍 {tx['analyze_btn']}",key="run_btn",use_container_width=True)

    # Store run state
    if run_clicked:
        st.session_state.run=True
        st.session_state.last_village=sel_village
        st.session_state.last_variety=sel_variety
        st.session_state.last_tonnes=sel_tonnes

    # MARKET PRICES — use st.columns (no HTML grid)
    st.markdown(f"""<div style="background:white;border-radius:14px;padding:20px 24px 16px;border:1px solid rgba(0,0,0,0.06);box-shadow:0 2px 14px rgba(0,0,0,0.04);margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
        <div style="font-size:12px;font-weight:700;color:#1a2e1f;">{tx['live_market']}</div>
        <div style="font-size:11px;color:#22c55e;font-weight:600;">● Live</div>
    </div></div>""",unsafe_allow_html=True)

    mp1,mp2,mp3,mp4=st.columns(4)
    for col,v,p,tr,cl,desc in [
        (mp1,"Banganapalli",28,"+2.1%","#22c55e","Best for export"),
        (mp2,"Totapuri",18,"-0.8%","#ef4444","Pulp & processing"),
        (mp3,"Neelam",22,"+1.4%","#22c55e","Local market"),
        (mp4,"Rasalu",30,"+3.2%","#22c55e","Premium table fruit"),
    ]:
        sel=sel_variety==v
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:18px 10px;
                background:{'linear-gradient(135deg,#071209,#0f2318)' if sel else '#f8f6f0'};
                border-radius:12px;border:1px solid {'rgba(212,175,55,0.35)' if sel else '#e5e7eb'};
                box-shadow:{'0 4px 16px rgba(212,175,55,0.15)' if sel else 'none'};
                margin-top:-52px;margin-bottom:16px;">
                <div style="font-size:11px;font-weight:600;color:{'rgba(212,175,55,0.8)' if sel else '#6b7280'};margin-bottom:5px;">{v}</div>
                <div style="font-size:28px;font-weight:700;color:{'#f5f0e8' if sel else '#1a2e1f'};margin-bottom:4px;">₹{p}</div>
                <div style="font-size:12px;font-weight:700;color:{cl};margin-bottom:6px;">{tr}</div>
                <div style="font-size:10px;color:{'rgba(245,240,232,0.45)' if sel else '#9ca3af'};">{desc}</div>
            </div>""",unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # RESULTS
    # ══════════════════════════════════════════════════════════════
    if st.session_state.get("run",False):

        # Use stored values so results persist after rerun
        rv=st.session_state.get("last_village",sel_village)
        rvar=st.session_state.get("last_variety",sel_variety)
        rt=st.session_state.get("last_tonnes",sel_tonnes)

        with st.spinner("Analysing all markets within 150km..."):
            vlat,vlon=village_coords(rv)
            df_res=run_analysis(vlat,vlon,rvar,rt)

        if df_res.empty:
            st.warning(tx["no_results"])
        else:
            top10=df_res.head(10).copy()
            top3=df_res.head(3)
            bn=int(top3.iloc[0]["Net_Profit"]); bd=top3.iloc[0]["Name"]; bc=top3.iloc[0]["Type"]

            # SUMMARY BANNER
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(4,14,7,0.96),rgba(7,24,12,0.94));border-radius:16px;padding:26px 32px;margin-bottom:18px;border:1px solid rgba(212,175,55,0.2);position:relative;overflow:hidden;">
                <div style="position:absolute;right:24px;top:50%;transform:translateY(-50%);font-size:70px;opacity:0.06;">🏆</div>
                <div style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:rgba(212,175,55,0.65);margin-bottom:10px;">{tx['profit_summary']}</div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
                    <div><div style="font-size:10px;color:rgba(245,240,232,0.4);margin-bottom:3px;">{tx['variety_lbl']}</div><div style="font-size:20px;font-weight:700;color:#f5f0e8;">{rvar}</div></div>
                    <div><div style="font-size:10px;color:rgba(245,240,232,0.4);margin-bottom:3px;">{tx['qty_lbl']}</div><div style="font-size:20px;font-weight:700;color:#f5f0e8;">{rt} T</div></div>
                    <div><div style="font-size:10px;color:rgba(245,240,232,0.4);margin-bottom:3px;">{tx['best_market']}</div><div style="font-size:16px;font-weight:700;color:#d4af37;line-height:1.2;">{bd}</div><div style="font-size:10px;color:rgba(212,175,55,0.5);">{bc}</div></div>
                    <div><div style="font-size:10px;color:rgba(245,240,232,0.4);margin-bottom:3px;">{tx['est_profit']}</div><div style="font-size:28px;font-weight:800;color:#22c55e;">₹{bn:,}</div></div>
                </div>
            </div>""",unsafe_allow_html=True)

            # TOP 3
            st.markdown(f'<div style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#6b7c6e;margin-bottom:12px;">{tx["top3"]}</div>',unsafe_allow_html=True)
            medals=[("#d4af37",tx["highest_profit"],True,"🥇"),("#94a3b8",tx["second_best"],False,"🥈"),("#a0785a",tx["third_best"],False,"🥉")]
            c3=st.columns(3)
            for i,(col,(acc,lbl_,istop,med)) in enumerate(zip(c3,medals)):
                if i>=len(top3): break
                r=top3.iloc[i]
                with col:
                    st.markdown(f"""
                    <div style="background:{'linear-gradient(145deg,#040e07,#0a1c10)' if istop else 'white'};border-radius:14px;padding:20px;height:100%;border:1px solid {acc if istop else 'rgba(0,0,0,0.06)'};box-shadow:{'0 12px 36px rgba(212,175,55,0.18)' if istop else '0 2px 12px rgba(0,0,0,0.05)'};position:relative;overflow:hidden;">
                        <div style="position:absolute;top:10px;right:12px;font-size:22px;opacity:0.12;">{med}</div>
                        <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{acc};margin-bottom:8px;font-weight:600;">{lbl_}</div>
                        <div style="font-size:15px;font-weight:700;color:{'#f5f0e8' if istop else '#1a2e1f'};margin-bottom:4px;line-height:1.3;">{r['Name']}</div>
                        <div style="display:inline-flex;align-items:center;gap:4px;background:{'rgba(255,255,255,0.06)' if istop else '#f3f4f6'};border-radius:5px;padding:3px 8px;margin-bottom:12px;">
                            <span>{r['icon']}</span><span style="font-size:10px;color:{r['color']};font-weight:500;">{r['Type']}</span>
                        </div>
                        <div style="font-size:26px;font-weight:800;color:{acc};margin-bottom:2px;">₹{int(r['Net_Profit']):,}</div>
                        <div style="font-size:10px;color:{'rgba(245,240,232,0.3)' if istop else '#9ca3af'};margin-bottom:12px;">{tx['net_profit_lbl']} · {r['Dist_km']} {tx['away_lbl']}</div>
                        <div style="border-top:1px solid {'rgba(255,255,255,0.06)' if istop else '#f3f4f6'};padding-top:10px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;">
                            <div><div style="font-size:9px;color:{'rgba(245,240,232,0.35)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['revenue_lbl']}</div><div style="font-size:11px;font-weight:600;color:{'rgba(245,240,232,0.8)' if istop else '#374151'};">₹{int(r['Revenue']):,}</div></div>
                            <div><div style="font-size:9px;color:{'rgba(245,240,232,0.35)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['transport_lbl']}</div><div style="font-size:11px;font-weight:600;color:#ef4444;">₹{int(r['Transport']):,}</div></div>
                            <div><div style="font-size:9px;color:{'rgba(245,240,232,0.35)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['risk']}</div><div style="font-size:11px;font-weight:600;color:#f59e0b;">{r['Risk_pct']}%</div></div>
                        </div>
                    </div>""",unsafe_allow_html=True)

            st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)

            # FARMER TIP
            st.markdown(f"""<div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:12px;padding:14px 20px;margin-bottom:18px;border:1px solid #fcd34d;display:flex;align-items:flex-start;gap:12px;"><span style="font-size:20px;">💡</span><div><div style="font-size:11px;font-weight:700;color:#92400e;letter-spacing:1px;text-transform:uppercase;margin-bottom:2px;">{tx['farmer_tip']}</div><div style="font-size:12.5px;color:#78350f;line-height:1.5;">{tx['tip_text']}</div></div></div>""",unsafe_allow_html=True)

            # BAR + PIE CHARTS
            cc1,cc2=st.columns([3,2])
            with cc1:
                st.markdown(f'<div style="background:white;border-radius:14px;padding:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 2px 12px rgba(0,0,0,0.04);"><div style="font-size:11px;font-weight:700;color:#1a2e1f;margin-bottom:12px;">{tx["bar_title"]}</div>',unsafe_allow_html=True)
                fig=go.Figure(go.Bar(y=top10["Name"],x=top10["Net_Profit"],orientation="h",
                    marker=dict(color=top10["color"].tolist(),line=dict(width=0)),
                    text=[f"₹{int(v):,}" for v in top10["Net_Profit"]],textposition="outside",
                    textfont=dict(size=11,color="#374151",family="Inter"),
                    hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>"))
                fig.update_layout(height=340,paper_bgcolor="white",plot_bgcolor="white",
                    margin=dict(l=0,r=80,t=4,b=4),font=dict(family="Inter"),
                    xaxis=dict(showgrid=True,gridcolor="#f5f3ef",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
                    yaxis=dict(autorange="reversed",tickfont=dict(size=11,color="#374151")),
                    hoverlabel=dict(bgcolor="#0a1c10",bordercolor="#d4af37",font=dict(color="white")))
                st.plotly_chart(fig,use_container_width=True)
                st.markdown("</div>",unsafe_allow_html=True)

            with cc2:
                st.markdown(f'<div style="background:white;border-radius:14px;padding:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 2px 12px rgba(0,0,0,0.04);"><div style="font-size:11px;font-weight:700;color:#1a2e1f;margin-bottom:12px;">{tx["pie_title"]}</div>',unsafe_allow_html=True)
                pdata=top10.groupby("Type")["Net_Profit"].sum().reset_index()
                cmap={"Mandi":"#3b82f6","Processing":"#8b5cf6","Pulp":"#f59e0b","Pickle":"#ec4899","Local Export":"#22c55e","Abroad Export":"#d4af37","Cold Storage":"#06b6d4","FPO":"#84cc16"}
                fig2=go.Figure(go.Pie(labels=pdata["Type"],values=pdata["Net_Profit"],hole=0.55,
                    marker=dict(colors=[cmap.get(c,"#888") for c in pdata["Type"]],line=dict(color="white",width=2)),
                    textinfo="percent+label",textfont=dict(size=10,family="Inter"),
                    hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} · %{percent}<extra></extra>"))
                fig2.update_layout(height=340,paper_bgcolor="white",margin=dict(l=8,r=8,t=4,b=4),
                    legend=dict(font=dict(size=10,family="Inter"),orientation="v",x=1.0,y=0.5),
                    font=dict(family="Inter"),
                    annotations=[dict(text=f"<b>{rvar}</b>",x=0.5,y=0.5,font=dict(size=12,color="#374151"),showarrow=False)],
                    hoverlabel=dict(bgcolor="#0a1c10",bordercolor="#d4af37",font=dict(color="white")))
                st.plotly_chart(fig2,use_container_width=True)
                st.markdown("</div>",unsafe_allow_html=True)

            st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)

            # STACKED BAR
            st.markdown(f'<div style="background:white;border-radius:14px;padding:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 2px 12px rgba(0,0,0,0.04);margin-bottom:16px;"><div style="font-size:11px;font-weight:700;color:#1a2e1f;margin-bottom:12px;">{tx["revenue_lbl"]} vs {tx["transport_lbl"]} — Top 10</div>',unsafe_allow_html=True)
            fig3=go.Figure()
            fig3.add_trace(go.Bar(name=tx["trans"],x=top10["Name"],y=top10["Transport"],marker_color="#ef4444",opacity=0.85,hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>"))
            fig3.add_trace(go.Bar(name=tx["net"],x=top10["Name"],y=top10["Net_Profit"],marker_color="#22c55e",opacity=0.9,hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>"))
            fig3.update_layout(barmode="stack",height=260,paper_bgcolor="white",plot_bgcolor="white",
                margin=dict(l=0,r=0,t=4,b=4),font=dict(family="Inter"),
                xaxis=dict(tickfont=dict(size=10,color="#6b7280"),tickangle=-20),
                yaxis=dict(showgrid=True,gridcolor="#f5f3ef",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
                legend=dict(orientation="h",y=1.1,font=dict(size=11)),
                hoverlabel=dict(bgcolor="#0a1c10",bordercolor="#d4af37",font=dict(color="white")))
            st.plotly_chart(fig3,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

            # TABLE
            st.markdown(f'<div style="background:white;border-radius:14px;padding:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 2px 12px rgba(0,0,0,0.04);margin-bottom:16px;"><div style="font-size:11px;font-weight:700;color:#1a2e1f;margin-bottom:12px;">{tx["table_title"]}</div>',unsafe_allow_html=True)
            disp=top10[["Rank","Name","Type","Dist_km","Revenue","Transport","Risk_pct","Net_Profit"]].copy()
            disp.columns=[tx["rank"],tx["dest"],tx["cat"],tx["dist_km"],tx["rev"],tx["trans"],tx["risk"],tx["net"]]
            st.dataframe(
                disp.style
                .background_gradient(subset=[tx["net"]],cmap="YlGn")
                .background_gradient(subset=[tx["dist_km"]],cmap="Oranges_r")
                .format({tx["rev"]:"₹{:,.0f}",tx["trans"]:"₹{:,.0f}",tx["net"]:"₹{:,.0f}",tx["dist_km"]:"{:.1f}",tx["risk"]:"{:.2f}%"})
                .set_properties(**{"font-family":"Inter,sans-serif","font-size":"13px"}),
                use_container_width=True,height=320)
            st.markdown("</div>",unsafe_allow_html=True)

            # MAP
            st.markdown(f'<div style="background:white;border-radius:14px;padding:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 2px 12px rgba(0,0,0,0.04);"><div style="font-size:11px;font-weight:700;color:#1a2e1f;margin-bottom:4px;">{tx["map_title"]}</div><div style="font-size:11px;color:#6b7280;margin-bottom:12px;">🏠 Your farm &nbsp;|&nbsp; ★ Best destination (gold dashed line) &nbsp;|&nbsp; Dots = other top markets</div>',unsafe_allow_html=True)
            br=top3.iloc[0]
            m=folium.Map(location=[vlat,vlon],zoom_start=8,tiles="CartoDB Positron")
            folium.Marker([vlat,vlon],
                popup=folium.Popup(f"<b>{fname}</b><br>📍 {rv}",max_width=200),tooltip=tx["your_loc"],
                icon=folium.DivIcon(html='<div style="background:#0a1c10;border:2.5px solid #d4af37;border-radius:50%;width:36px;height:36px;display:flex;align-items:center;justify-content:center;font-size:17px;box-shadow:0 3px 14px rgba(0,0,0,0.4);">🏠</div>',icon_size=(36,36),icon_anchor=(18,18))
            ).add_to(m)
            folium.Marker([br["Lat"],br["Lon"]],
                popup=folium.Popup(f"<b>{br['Name']}</b><br>{br['Type']}<br><span style='color:#22c55e;font-weight:700'>₹{int(br['Net_Profit']):,}</span>",max_width=220),tooltip=tx["best_dest"],
                icon=folium.DivIcon(html='<div style="background:#d4af37;border:2.5px solid white;border-radius:50%;width:38px;height:38px;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:900;color:#040e07;box-shadow:0 3px 16px rgba(212,175,55,0.55);">★</div>',icon_size=(38,38),icon_anchor=(19,19))
            ).add_to(m)
            folium.PolyLine([(vlat,vlon),(br["Lat"],br["Lon"])],color="#d4af37",weight=4,opacity=0.9,dash_array="8 5").add_to(m)
            for _,row in top10.iloc[1:].iterrows():
                folium.CircleMarker([row["Lat"],row["Lon"]],radius=9,color=row["color"],fill=True,fill_color=row["color"],fill_opacity=0.8,weight=2,
                    popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br>₹{int(row['Net_Profit']):,}",max_width=200),tooltip=row["Name"]).add_to(m)
            st_folium(m,width=None,height=500,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

    st.markdown('</div>',unsafe_allow_html=True)
