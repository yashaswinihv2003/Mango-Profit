import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import numpy as np
import random
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="Mango Profit Navigator",
    page_icon="🥭",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English": {
        "title":"Mango Profit Navigator","tagline":"Smart Agricultural Decision Platform",
        "sign_in":"Sign In","create_account":"Create Account",
        "phone":"Phone Number","password":"Password",
        "phone_ph":"Enter 10-digit mobile number","pass_ph":"Enter your password",
        "login_btn":"Sign In","forgot":"Forgot Password?",
        "otp_opt":"Sign in with OTP","send_otp":"Send OTP",
        "verify_otp":"Verify OTP","otp_ph":"Enter 6-digit OTP",
        "name":"Full Name","place":"Village / District","reg_btn":"Create Account",
        "select_lang":"🌐 Language","village_sel":"Select Your Village",
        "variety":"Mango Variety","quantity":"Quantity (Tonnes)",
        "analyze_btn":"Find Best Markets & Profit",
        "top3":"Top 3 Most Profitable Destinations",
        "bar_title":"Net Profit Comparison","pie_title":"Market Share by Category",
        "map_title":"Route Map to Best Destination","table_title":"Complete Destination Analysis",
        "rank":"Rank","dest":"Destination","cat":"Category",
        "dist_km":"Distance (km)","rev":"Revenue (₹)","trans":"Transport (₹)",
        "risk":"Risk (%)","net":"Net Profit (₹)",
        "logout":"Sign Out","reset_pw":"Reset Password",
        "new_pw":"New Password","conf_pw":"Confirm Password","upd_pw":"Update Password",
        "back":"Back to Sign In","use_pw":"Use password instead",
        "live_market":"Today's Mango Prices","highest_profit":"HIGHEST PROFIT",
        "second_best":"2ND BEST","third_best":"3RD BEST",
        "net_profit_lbl":"Net Profit","away_lbl":"km away",
        "your_loc":"Your Farm","best_dest":"Best Destination",
        "revenue_lbl":"Revenue","transport_lbl":"Transport Cost",
        "profit_summary":"Your Profit Analysis",
        "variety_lbl":"Variety","qty_lbl":"Quantity",
        "best_market":"Best Market","est_profit":"Estimated Profit",
        "farmer_tip":"Expert Tip",
        "tip_text":"Abroad Export gives highest premium (+7%) but needs quality certification. Local Export is the easiest entry point for most farmers.",
        "no_results":"No markets found within 150km. Try a different village or variety.",
        "welcome":"Welcome back","hero_title":"Find Your Most Profitable Mango Market",
        "hero_sub":"Select your village, variety and quantity — our AI engine analyses all nearby markets and finds you the best profit.",
        "fill_details":"Enter Your Farm Details",
        "how_works":"How It Works",
        "step1_t":"Select Your Village","step1_d":"Choose from real village data",
        "step2_t":"Enter Variety & Qty","step2_d":"Tell us what you have to sell",
        "step3_t":"AI Analyses Markets","step3_d":"We check all mandis, exporters, factories",
        "step4_t":"Get Best Profit Route","step4_d":"See ranked results with map",
    },
    "Telugu": {
        "title":"మామిడి లాభం నావిగేటర్","tagline":"స్మార్ట్ వ్యవసాయ నిర్ణయ వేదిక",
        "sign_in":"లాగిన్","create_account":"ఖాతా తెరవండి",
        "phone":"ఫోన్ నంబర్","password":"పాస్‌వర్డ్",
        "phone_ph":"10 అంకెల నంబర్","pass_ph":"పాస్‌వర్డ్ నమోదు చేయండి",
        "login_btn":"లాగిన్ చేయండి","forgot":"పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt":"OTP తో లాగిన్","send_otp":"OTP పంపండి",
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"6 అంకెల OTP",
        "name":"పూర్తి పేరు","place":"గ్రామం / జిల్లా","reg_btn":"ఖాతా తెరవండి",
        "select_lang":"🌐 భాష","village_sel":"మీ గ్రామాన్ని ఎంచుకోండి",
        "variety":"మామిడి రకం","quantity":"పరిమాణం (టన్నులు)",
        "analyze_btn":"ఉత్తమ మార్కెట్లు కనుగొనండి",
        "top3":"అగ్ర 3 లాభదాయక గమ్యాలు",
        "bar_title":"నికర లాభం పోలిక","pie_title":"మార్కెట్ వర్గం వాటా",
        "map_title":"ఉత్తమ గమ్యానికి మార్గ మ్యాప్","table_title":"పూర్తి గమ్యం విశ్లేషణ",
        "rank":"స్థానం","dest":"గమ్యం","cat":"వర్గం",
        "dist_km":"దూరం (కి.మీ)","rev":"ఆదాయం (₹)","trans":"రవాణా (₹)",
        "risk":"రిస్క్ (%)","net":"నికర లాభం (₹)",
        "logout":"నిష్క్రమించు","reset_pw":"పాస్‌వర్డ్ రీసెట్",
        "new_pw":"కొత్త పాస్‌వర్డ్","conf_pw":"నిర్ధారించండి","upd_pw":"అప్‌డేట్ చేయండి",
        "back":"లాగిన్‌కు తిరిగి","use_pw":"పాస్‌వర్డ్ ఉపయోగించండి",
        "live_market":"నేటి మామిడి ధరలు","highest_profit":"అత్యధిక లాభం",
        "second_best":"2వ ఉత్తమం","third_best":"3వ ఉత్తమం",
        "net_profit_lbl":"నికర లాభం","away_lbl":"కి.మీ దూరం",
        "your_loc":"మీ పొలం","best_dest":"ఉత్తమ గమ్యం",
        "revenue_lbl":"ఆదాయం","transport_lbl":"రవాణా ఖర్చు",
        "profit_summary":"మీ లాభం విశ్లేషణ",
        "variety_lbl":"రకం","qty_lbl":"పరిమాణం",
        "best_market":"ఉత్తమ మార్కెట్","est_profit":"అంచనా లాభం",
        "farmer_tip":"నిపుణుల సలహా",
        "tip_text":"విదేశీ ఎగుమతి అత్యధిక ప్రీమియం (+7%) ఇస్తుంది కానీ నాణ్యత ధృవీకరణ అవసరం.",
        "no_results":"150 కి.మీ పరిధిలో మార్కెట్లు కనుగొనబడలేదు.",
        "welcome":"స్వాగతం","hero_title":"మీ అత్యంత లాభదాయక మామిడి మార్కెట్ కనుగొనండి",
        "hero_sub":"మీ గ్రామం, రకం మరియు పరిమాణాన్ని ఎంచుకోండి — మా AI ఇంజన్ అన్ని సమీప మార్కెట్లను విశ్లేషిస్తుంది.",
        "fill_details":"మీ పొలం వివరాలు నమోదు చేయండి",
        "how_works":"ఇది ఎలా పని చేస్తుంది",
        "step1_t":"మీ గ్రామం ఎంచుకోండి","step1_d":"నిజమైన గ్రామ డేటా నుండి ఎంచుకోండి",
        "step2_t":"రకం & పరిమాణం నమోదు చేయండి","step2_d":"మీరు అమ్మాలనుకున్నది చెప్పండి",
        "step3_t":"AI మార్కెట్లను విశ్లేషిస్తుంది","step3_d":"అన్ని మండీలు, ఎగుమతిదారులు తనిఖీ",
        "step4_t":"ఉత్తమ లాభ మార్గం పొందండి","step4_d":"మ్యాప్‌తో ర్యాంక్ ఫలితాలు చూడండి",
    },
    "Hindi": {
        "title":"आम लाभ नेविगेटर","tagline":"स्मार्ट कृषि निर्णय मंच",
        "sign_in":"साइन इन","create_account":"खाता बनाएं",
        "phone":"फ़ोन नंबर","password":"पासवर्ड",
        "phone_ph":"10 अंकों का नंबर","pass_ph":"पासवर्ड दर्ज करें",
        "login_btn":"साइन इन करें","forgot":"पासवर्ड भूल गए?",
        "otp_opt":"OTP से साइन इन","send_otp":"OTP भेजें",
        "verify_otp":"OTP सत्यापित करें","otp_ph":"6 अंकों का OTP",
        "name":"पूरा नाम","place":"गाँव / जिला","reg_btn":"खाता बनाएं",
        "select_lang":"🌐 भाषा","village_sel":"अपना गाँव चुनें",
        "variety":"आम की किस्म","quantity":"मात्रा (टन)",
        "analyze_btn":"सर्वोत्तम बाज़ार खोजें",
        "top3":"शीर्ष 3 लाभदायक गंतव्य",
        "bar_title":"शुद्ध लाभ तुलना","pie_title":"बाज़ार श्रेणी हिस्सेदारी",
        "map_title":"सर्वोत्तम गंतव्य का मार्ग","table_title":"पूर्ण गंतव्य विश्लेषण",
        "rank":"रैंक","dest":"गंतव्य","cat":"श्रेणी",
        "dist_km":"दूरी (कि.मी.)","rev":"राजस्व (₹)","trans":"परिवहन (₹)",
        "risk":"जोखिम (%)","net":"शुद्ध लाभ (₹)",
        "logout":"साइन आउट","reset_pw":"पासवर्ड रीसेट",
        "new_pw":"नया पासवर्ड","conf_pw":"पुष्टि करें","upd_pw":"अपडेट करें",
        "back":"साइन इन पर वापस","use_pw":"पासवर्ड का उपयोग करें",
        "live_market":"आज के आम के भाव","highest_profit":"सर्वाधिक लाभ",
        "second_best":"दूसरा सर्वश्रेष्ठ","third_best":"तीसरा सर्वश्रेष्ठ",
        "net_profit_lbl":"शुद्ध लाभ","away_lbl":"कि.मी. दूर",
        "your_loc":"आपका खेत","best_dest":"सर्वोत्तम गंतव्य",
        "revenue_lbl":"राजस्व","transport_lbl":"परिवहन लागत",
        "profit_summary":"आपका लाभ विश्लेषण",
        "variety_lbl":"किस्म","qty_lbl":"मात्रा",
        "best_market":"सर्वोत्तम बाज़ार","est_profit":"अनुमानित लाभ",
        "farmer_tip":"विशेषज्ञ सुझाव",
        "tip_text":"विदेश निर्यात सबसे अधिक प्रीमियम (+7%) देता है लेकिन गुणवत्ता प्रमाणीकरण आवश्यक है।",
        "no_results":"150 कि.मी. के भीतर कोई बाज़ार नहीं मिला।",
        "welcome":"स्वागत है","hero_title":"अपना सबसे लाभदायक आम बाज़ार खोजें",
        "hero_sub":"अपना गाँव, किस्म और मात्रा चुनें — हमारा AI इंजन सभी पास के बाज़ारों का विश्लेषण करता है।",
        "fill_details":"अपने खेत की जानकारी दर्ज करें",
        "how_works":"यह कैसे काम करता है",
        "step1_t":"अपना गाँव चुनें","step1_d":"वास्तविक गाँव डेटा से चुनें",
        "step2_t":"किस्म और मात्रा दर्ज करें","step2_d":"बताएं आप क्या बेचना चाहते हैं",
        "step3_t":"AI बाज़ारों का विश्लेषण करता है","step3_d":"सभी मंडी, निर्यातकों की जाँच",
        "step4_t":"सर्वोत्तम लाभ मार्ग पाएं","step4_d":"मानचित्र के साथ रैंक परिणाम देखें",
    },
    "Kannada": {
        "title":"ಮಾವಿನ ಲಾಭ ನ್ಯಾವಿಗೇಟರ್","tagline":"ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ನಿರ್ಧಾರ ವೇದಿಕೆ",
        "sign_in":"ಸೈನ್ ಇನ್","create_account":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "phone":"ಫೋನ್ ಸಂಖ್ಯೆ","password":"ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph":"10 ಅಂಕಿಯ ಸಂಖ್ಯೆ","pass_ph":"ಪಾಸ್‌ವರ್ಡ್ ನಮೂದಿಸಿ",
        "login_btn":"ಸೈನ್ ಇನ್ ಮಾಡಿ","forgot":"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt":"OTP ಮೂಲಕ ಸೈನ್ ಇನ್","send_otp":"OTP ಕಳುಹಿಸಿ",
        "verify_otp":"OTP ಪರಿಶೀಲಿಸಿ","otp_ph":"6 ಅಂಕಿಯ OTP",
        "name":"ಪೂರ್ಣ ಹೆಸರು","place":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ","reg_btn":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "select_lang":"🌐 ಭಾಷೆ","village_sel":"ನಿಮ್ಮ ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ",
        "variety":"ಮಾವಿನ ತಳಿ","quantity":"ಪ್ರಮಾಣ (ಟನ್)",
        "analyze_btn":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "top3":"ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title":"ನಿವ್ವಳ ಲಾಭ ಹೋಲಿಕೆ","pie_title":"ಮಾರುಕಟ್ಟೆ ವಿಭಾಗ ಪಾಲು",
        "map_title":"ಉತ್ತಮ ಗಮ್ಯಕ್ಕೆ ಮಾರ್ಗ ನಕ್ಷೆ","table_title":"ಸಂಪೂರ್ಣ ಗಮ್ಯ ವಿಶ್ಲೇಷಣೆ",
        "rank":"ಶ್ರೇಣಿ","dest":"ಗಮ್ಯ","cat":"ವರ್ಗ",
        "dist_km":"ದೂರ (ಕಿ.ಮೀ)","rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)",
        "risk":"ಅಪಾಯ (%)","net":"ನಿವ್ವಳ ಲಾಭ (₹)",
        "logout":"ಸೈನ್ ಔಟ್","reset_pw":"ಪಾಸ್‌ವರ್ಡ್ ರೀಸೆಟ್",
        "new_pw":"ಹೊಸ ಪಾಸ್‌ವರ್ಡ್","conf_pw":"ದೃಢಪಡಿಸಿ","upd_pw":"ನವೀಕರಿಸಿ",
        "back":"ಸೈನ್ ಇನ್‌ಗೆ ಹಿಂತಿರುಗಿ","use_pw":"ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ",
        "live_market":"ಇಂದಿನ ಮಾವಿನ ಬೆಲೆಗಳು","highest_profit":"ಅತ್ಯಧಿಕ ಲಾಭ",
        "second_best":"2ನೇ ಉತ್ತಮ","third_best":"3ನೇ ಉತ್ತಮ",
        "net_profit_lbl":"ನಿವ್ವಳ ಲಾಭ","away_lbl":"ಕಿ.ಮೀ ದೂರ",
        "your_loc":"ನಿಮ್ಮ ಹೊಲ","best_dest":"ಉತ್ತಮ ಗಮ್ಯ",
        "revenue_lbl":"ಆದಾಯ","transport_lbl":"ಸಾರಿಗೆ ವೆಚ್ಚ",
        "profit_summary":"ನಿಮ್ಮ ಲಾಭ ವಿಶ್ಲೇಷಣೆ",
        "variety_lbl":"ತಳಿ","qty_lbl":"ಪ್ರಮಾಣ",
        "best_market":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ","est_profit":"ಅಂದಾಜು ಲಾಭ",
        "farmer_tip":"ತಜ್ಞರ ಸಲಹೆ",
        "tip_text":"ವಿದೇಶ ರಫ್ತು ಅತ್ಯಧಿಕ ಪ್ರೀಮಿಯಂ (+7%) ನೀಡುತ್ತದೆ ಆದರೆ ಗುಣಮಟ್ಟ ಪ್ರಮಾಣೀಕರಣ ಅಗತ್ಯ.",
        "no_results":"150 ಕಿ.ಮೀ ಪರಿಧಿಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "welcome":"ಸ್ವಾಗತ","hero_title":"ನಿಮ್ಮ ಅತ್ಯಂತ ಲಾಭದಾಯಕ ಮಾವಿನ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "hero_sub":"ನಿಮ್ಮ ಗ್ರಾಮ, ತಳಿ ಮತ್ತು ಪ್ರಮಾಣ ಆಯ್ಕೆ ಮಾಡಿ — ನಮ್ಮ AI ಎಲ್ಲಾ ಸಮೀಪ ಮಾರುಕಟ್ಟೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ.",
        "fill_details":"ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "how_works":"ಇದು ಹೇಗೆ ಕಾರ್ಯ ನಿರ್ವಹಿಸುತ್ತದೆ",
        "step1_t":"ನಿಮ್ಮ ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ","step1_d":"ನಿಜ ಗ್ರಾಮ ಡೇಟಾದಿಂದ ಆಯ್ಕೆ ಮಾಡಿ",
        "step2_t":"ತಳಿ ಮತ್ತು ಪ್ರಮಾಣ ನಮೂದಿಸಿ","step2_d":"ನೀವು ಮಾರಾಟ ಮಾಡಲು ಬಯಸುವುದನ್ನು ತಿಳಿಸಿ",
        "step3_t":"AI ಮಾರುಕಟ್ಟೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ","step3_d":"ಎಲ್ಲಾ ಮಂಡಿ, ರಫ್ತುದಾರರನ್ನು ಪರಿಶೀಲಿಸಿ",
        "step4_t":"ಉತ್ತಮ ಲಾಭ ಮಾರ್ಗ ಪಡೆಯಿರಿ","step4_d":"ನಕ್ಷೆಯೊಂದಿಗೆ ಶ್ರೇಣೀಕೃತ ಫಲಿತಾಂಶಗಳು",
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
    "last_village":None,"last_variety":"Banganapalli","last_tonnes":10.0,
}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS — Agricultural Website Theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600&display=swap');

*{box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stDecoration"]{visibility:hidden;display:none!important;}
.stApp{font-family:'Poppins',sans-serif;background:#f0f4f0!important;}
.main .block-container{padding:0!important;max-width:100%!important;}

/* ── Login inputs ── */
.stTextInput>label{display:none!important;}
.stTextInput>div>div>input{
    background:rgba(255,255,255,0.15)!important;
    border:1.5px solid rgba(255,255,255,0.3)!important;
    border-radius:8px!important;color:white!important;
    font-family:'Poppins',sans-serif!important;font-size:14px!important;
    padding:13px 16px!important;
}
.stTextInput>div>div>input:focus{border-color:#fbbf24!important;outline:none!important;}
.stTextInput>div>div>input::placeholder{color:rgba(255,255,255,0.5)!important;}

/* ── All buttons ── */
.stButton>button{
    font-family:'Poppins',sans-serif!important;font-size:13px!important;
    font-weight:600!important;border-radius:8px!important;
    padding:12px 20px!important;transition:all 0.2s!important;cursor:pointer!important;
    text-transform:uppercase!important;letter-spacing:0.5px!important;
}
.stButton>button:not([kind="secondary"]){
    background:#1a7a1a!important;color:white!important;border:none!important;
    box-shadow:0 4px 15px rgba(26,122,26,0.35)!important;
}
.stButton>button:not([kind="secondary"]):hover{
    background:#156015!important;transform:translateY(-1px)!important;
    box-shadow:0 6px 20px rgba(26,122,26,0.5)!important;
}
.stButton>button[kind="secondary"]{
    background:transparent!important;color:rgba(255,255,255,0.7)!important;
    border:1px solid rgba(255,255,255,0.3)!important;font-size:11px!important;
    padding:8px 14px!important;text-transform:none!important;letter-spacing:0!important;
}
.stButton>button[kind="secondary"]:hover{border-color:white!important;color:white!important;}

/* ── Dashboard selectbox ── */
.stSelectbox>label{
    font-size:11px!important;font-weight:600!important;color:#374151!important;
    text-transform:uppercase!important;letter-spacing:0.5px!important;
}
.stSelectbox>div>div{
    background:white!important;border:2px solid #e5e7eb!important;
    border-radius:8px!important;color:#1a1a1a!important;
    font-family:'Poppins',sans-serif!important;font-size:14px!important;
}
.stSelectbox>div>div:hover{border-color:#1a7a1a!important;}

/* ── Number input ── */
.stNumberInput>label{
    font-size:11px!important;font-weight:600!important;color:#374151!important;
    text-transform:uppercase!important;letter-spacing:0.5px!important;
}
.stNumberInput>div>div>input{
    background:white!important;border:2px solid #e5e7eb!important;
    border-radius:8px!important;color:#1a1a1a!important;
    font-family:'Poppins',sans-serif!important;font-size:14px!important;
    padding:11px 14px!important;
}
.stNumberInput>div>div>input:focus{border-color:#1a7a1a!important;}

/* ── Sidebar ── */
[data-testid="stSidebar"]{
    background:#1a3a1a!important;
    border-right:3px solid #2d5a2d!important;
}
[data-testid="stSidebar"] label{
    color:#86efac!important;font-size:10px!important;
    letter-spacing:1.5px!important;text-transform:uppercase!important;
}
[data-testid="stSidebar"] .stSelectbox>div>div{
    background:rgba(255,255,255,0.08)!important;
    border:1px solid rgba(134,239,172,0.3)!important;
    color:#e8f5e9!important;border-radius:8px!important;
}

/* ── Green run button override for dashboard ── */
.run-btn .stButton>button{
    background:linear-gradient(135deg,#1a7a1a,#156015)!important;
    font-size:14px!important;padding:14px 20px!important;
    box-shadow:0 6px 20px rgba(26,122,26,0.4)!important;
    border-radius:10px!important;
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
        background-image:
            linear-gradient(rgba(0,60,0,0.72),rgba(0,40,0,0.80)),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=90&fit=crop');
        background-size:cover!important;
        background-position:center!important;
        background-attachment:fixed!important;
    }
    .stSelectbox>div>div{background:rgba(255,255,255,0.15)!important;border:1.5px solid rgba(255,255,255,0.3)!important;color:white!important;}
    .stSelectbox>label{color:rgba(255,255,255,0.7)!important;}
    </style>""", unsafe_allow_html=True)

    # Top green navbar
    st.markdown(f"""
    <div style="background:#1a7a1a;padding:12px 36px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 3px 15px rgba(0,0,0,0.3);">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:40px;height:40px;background:#fbbf24;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 2px 8px rgba(0,0,0,0.2);">🥭</div>
            <div>
                <div style="font-family:'Poppins',sans-serif;font-size:18px;font-weight:700;color:white;">{tx['title']}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.7);">{tx['tagline']}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:24px;">
            <div style="font-size:12px;color:rgba(255,255,255,0.8);">Home</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.8);">About</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.8);">Contact</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Language selector
    _l1,_l2=st.columns([5,1])
    with _l2:
        c=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],
            index=["English","Telugu","Hindi","Kannada"].index(lang),
            key="lang_sel",label_visibility="collapsed")
        if c!=lang: st.session_state.lang=c; st.rerun()

    st.markdown('<div style="height:40px"></div>',unsafe_allow_html=True)

    # Hero text + login card side by side
    hero_col, form_col = st.columns([1.2, 1])

    with hero_col:
        st.markdown(f"""
        <div style="padding:40px 40px;">
            <div style="display:inline-block;background:#fbbf24;color:#1a1a1a;font-size:11px;font-weight:700;padding:5px 14px;border-radius:20px;letter-spacing:1px;text-transform:uppercase;margin-bottom:16px;">
                Farmer Intelligence Platform
            </div>
            <h1 style="font-family:'Playfair Display',serif;font-size:44px;color:white;font-weight:600;line-height:1.2;margin-bottom:16px;">
                {tx['hero_title']}
            </h1>
            <p style="font-size:15px;color:rgba(255,255,255,0.75);line-height:1.7;max-width:480px;margin-bottom:28px;">
                {tx['hero_sub']}
            </p>
            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <div style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:10px 16px;display:flex;align-items:center;gap:8px;">
                    <span style="font-size:18px;">🗺️</span>
                    <span style="font-size:12px;color:white;font-weight:500;">Real Map Routes</span>
                </div>
                <div style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:10px 16px;display:flex;align-items:center;gap:8px;">
                    <span style="font-size:18px;">📊</span>
                    <span style="font-size:12px;color:white;font-weight:500;">AI Profit Analysis</span>
                </div>
                <div style="background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:10px 16px;display:flex;align-items:center;gap:8px;">
                    <span style="font-size:18px;">🌐</span>
                    <span style="font-size:12px;color:white;font-weight:500;">4 Languages</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with form_col:
        st.markdown("""
        <div style="background:rgba(0,30,0,0.75);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.15);border-radius:16px;padding:36px;margin:20px 40px 20px 0;box-shadow:0 20px 60px rgba(0,0,0,0.4);">
        """, unsafe_allow_html=True)

        t1,t2=st.columns(2)
        with t1:
            if st.button(tx["sign_in"],key="tab_si",use_container_width=True,
                type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login";st.session_state.otp_mode=False
                st.session_state.forgot=False;st.rerun()
        with t2:
            if st.button(tx["create_account"],key="tab_ca",use_container_width=True,
                type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register";st.session_state.otp_mode=False
                st.session_state.forgot=False;st.rerun()

        st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)

        def lbl(t):
            st.markdown(f'<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.6);margin-bottom:6px;font-weight:500;">{t}</div>',unsafe_allow_html=True)

        if st.session_state.forgot:
            lbl(tx["reset_pw"])
            fph=st.text_input("_fph",placeholder=tx["phone_ph"],key="fp_ph",label_visibility="collapsed")
            if not st.session_state.f_otp_sent:
                if st.button(tx["send_otp"],key="fp_send",use_container_width=True):
                    if fph and len(fph)==10 and fph.isdigit():
                        u=get_user(fph)
                        if u:
                            code=str(random.randint(100000,999999))
                            st.session_state.f_code=code;st.session_state.f_otp_sent=True
                            st.session_state.otp_phone=fph
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
                        st.session_state.forgot=False;st.session_state.f_otp_sent=False
                        st.session_state.f_otp_ok=False;st.session_state.f_code=None;st.rerun()
                    else: st.error("Passwords do not match.")
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
                            st.session_state.otp_code=code;st.session_state.otp_sent=True
                            st.session_state.otp_phone=op
                            st.info(f"Demo OTP: **{code}**");st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            else:
                lbl(tx["otp_ph"])
                eo=st.text_input("_eov",placeholder=tx["otp_ph"],key="otp_v",label_visibility="collapsed")
                if st.button(tx["verify_otp"],key="v_otp",use_container_width=True):
                    if eo==st.session_state.otp_code:
                        u=get_user(st.session_state.otp_phone)
                        st.session_state.logged_in=True;st.session_state.user=u
                        st.session_state.otp_sent=False;st.rerun()
                    else: st.error("Incorrect OTP.")
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
            st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
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

    # How it works section
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4);padding:40px;margin-top:20px;">
        <h2 style="font-family:'Playfair Display',serif;color:white;text-align:center;margin-bottom:30px;font-size:28px;">{tx['how_works']}</h2>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;max-width:900px;margin:0 auto;">
    """,unsafe_allow_html=True)

    steps=[("01","🏘️",tx['step1_t'],tx['step1_d']),("02","🥭",tx['step2_t'],tx['step2_d']),
           ("03","🤖",tx['step3_t'],tx['step3_d']),("04","🗺️",tx['step4_t'],tx['step4_d'])]
    steps_html="".join([f"""
    <div style="text-align:center;padding:20px;background:rgba(255,255,255,0.08);border-radius:12px;border:1px solid rgba(255,255,255,0.12);">
        <div style="font-size:11px;color:#fbbf24;font-weight:700;letter-spacing:2px;margin-bottom:8px;">STEP {n}</div>
        <div style="font-size:30px;margin-bottom:8px;">{ic}</div>
        <div style="font-size:13px;font-weight:600;color:white;margin-bottom:4px;">{t}</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.55);">{d}</div>
    </div>""" for n,ic,t,d in steps])
    st.markdown(steps_html+"</div></div>",unsafe_allow_html=True)
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
    mdf=prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices
    CATS={
        "Mandi":{"mg":0.00,"col":"#3b82f6","ic":"🏪","df":mdf},
        "Processing":{"mg":0.03,"col":"#8b5cf6","ic":"🏭","df":processing},
        "Pulp":{"mg":0.04,"col":"#f59e0b","ic":"🧃","df":pulp},
        "Pickle":{"mg":0.025,"col":"#ec4899","ic":"🫙","df":pickle_u},
        "Local Export":{"mg":0.05,"col":"#16a34a","ic":"🚛","df":local_exp},
        "Abroad Export":{"mg":0.07,"col":"#d97706","ic":"✈️","df":abroad_exp},
        "Cold Storage":{"mg":0.01,"col":"#0891b2","ic":"🧊","df":cold},
        "FPO":{"mg":0.02,"col":"#65a30d","ic":"👥","df":fpo},
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

# ── GREEN NAV BAR (like Seodo/Agricul) ──
st.markdown(f"""
<div style="background:#1a7a1a;padding:0 32px;height:68px;display:flex;align-items:center;
    justify-content:space-between;box-shadow:0 4px 20px rgba(0,0,0,0.25);position:sticky;top:0;z-index:999;">
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:42px;height:42px;background:#fbbf24;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 2px 10px rgba(0,0,0,0.2);">🥭</div>
        <div>
            <div style="font-family:'Poppins',sans-serif;font-size:20px;font-weight:700;color:white;">{tx['title']}</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.65);letter-spacing:2px;text-transform:uppercase;">{tx['tagline']}</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:28px;">
        <div style="font-size:13px;color:rgba(255,255,255,0.85);font-weight:500;cursor:pointer;">Dashboard</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.85);font-weight:500;cursor:pointer;">Markets</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.85);font-weight:500;cursor:pointer;">Help</div>
        <div style="display:flex;align-items:center;gap:10px;border-left:1px solid rgba(255,255,255,0.2);padding-left:20px;">
            <div style="width:34px;height:34px;background:#fbbf24;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;color:#1a1a1a;">{fname[0].upper()}</div>
            <div>
                <div style="font-size:13px;color:white;font-weight:500;">{fname}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.6);">📍 {fplace}</div>
            </div>
        </div>
    </div>
</div>""",unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""<div style="padding:18px 4px 10px;">
        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#86efac;margin-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:10px;">Settings</div>
    </div>""",unsafe_allow_html=True)
    sl=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],
                     index=["English","Telugu","Hindi","Kannada"].index(lang))
    if sl!=lang: st.session_state.lang=sl;st.rerun()

    st.markdown(f"""<div style="margin-top:18px;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#86efac;margin-bottom:10px;">{tx['live_market']}</div>""",unsafe_allow_html=True)
    for v,(p,tr,cl) in {"Banganapalli":(28,"+2.1%","#4ade80"),"Totapuri":(18,"-0.8%","#f87171"),
                         "Neelam":(22,"+1.4%","#4ade80"),"Rasalu":(30,"+3.2%","#4ade80")}.items():
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 10px;margin-bottom:5px;background:rgba(255,255,255,0.06);border-radius:7px;border:1px solid rgba(255,255,255,0.08);">
            <div><div style="font-size:12px;color:#e8f5e9;font-weight:500;">{v}</div><div style="font-size:10px;color:#86efac;">₹{p}/kg</div></div>
            <div style="font-size:12px;font-weight:700;color:{cl};">{tr}</div>
        </div>""",unsafe_allow_html=True)

    st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)
    if st.button(tx["logout"],use_container_width=True,type="secondary"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════
# HERO SECTION WITH FARM IMAGE BACKGROUND
# ══════════════════════════════════════════════════════════════
vlist=village_list()

st.markdown(f"""
<div style="
    background-image:linear-gradient(rgba(0,40,0,0.65),rgba(0,30,0,0.75)),
        url('https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=1400&q=85&fit=crop');
    background-size:cover;background-position:center;
    padding:56px 40px 44px;position:relative;overflow:hidden;">
    <div style="max-width:600px;">
        <div style="display:inline-block;background:#fbbf24;color:#1a1a1a;font-size:11px;font-weight:700;padding:5px 14px;border-radius:20px;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;">AI-Powered Profit Engine</div>
        <h1 style="font-family:'Playfair Display',serif;font-size:38px;color:white;font-weight:600;line-height:1.25;margin-bottom:10px;">{tx['hero_title']}</h1>
        <p style="font-size:14px;color:rgba(255,255,255,0.75);line-height:1.7;margin-bottom:0;">{tx['hero_sub']}</p>
    </div>
</div>""",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# INPUT FORM SECTION — white card overlapping hero
# ══════════════════════════════════════════════════════════════
st.markdown("""<div style="background:#f0f4f0;padding:0 32px;">""",unsafe_allow_html=True)

st.markdown(f"""
<div style="background:white;border-radius:16px;padding:28px 32px 24px;
    box-shadow:0 10px 40px rgba(0,0,0,0.12);border:1px solid #e5e7eb;
    margin-top:-24px;margin-bottom:24px;position:relative;z-index:10;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;border-bottom:2px solid #f0f4f0;padding-bottom:14px;">
        <div style="width:36px;height:36px;background:#1a7a1a;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;">🌾</div>
        <div>
            <div style="font-size:15px;font-weight:700;color:#1a2e1f;">{tx['fill_details']}</div>
            <div style="font-size:11px;color:#6b7280;">Fill all fields and click the button to see results</div>
        </div>
    </div>
</div>""",unsafe_allow_html=True)

fc1,fc2,fc3,fc4=st.columns([2,1.8,1,1.6])
with fc1:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">📍 {tx["village_sel"]}</p>',unsafe_allow_html=True)
    sel_village=st.selectbox("__v",vlist,key="sel_v",label_visibility="collapsed")
with fc2:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">🥭 {tx["variety"]}</p>',unsafe_allow_html=True)
    sel_variety=st.selectbox("__var",["Banganapalli","Totapuri","Neelam","Rasalu"],key="sel_var",label_visibility="collapsed")
with fc3:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">⚖️ {tx["quantity"]}</p>',unsafe_allow_html=True)
    sel_tonnes=st.number_input("__t",min_value=0.5,value=10.0,step=0.5,key="sel_t",label_visibility="collapsed")
with fc4:
    st.markdown('<p style="font-size:11px;font-weight:700;color:white;margin-bottom:4px;">.</p>',unsafe_allow_html=True)
    run_clicked=st.button(f"🔍  {tx['analyze_btn']}",key="run_btn",use_container_width=True)

if run_clicked:
    st.session_state.run=True
    st.session_state.last_village=sel_village
    st.session_state.last_variety=sel_variety
    st.session_state.last_tonnes=sel_tonnes

# ── TODAY'S PRICES (green strip like agri website) ──
st.markdown(f"""
<div style="background:#1a7a1a;padding:16px 0;margin:0 -32px 24px;overflow:hidden;">
    <div style="padding:0 32px;">
        <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;">
            <div style="font-size:11px;font-weight:700;color:#fbbf24;letter-spacing:2px;text-transform:uppercase;white-space:nowrap;">{tx['live_market']}</div>
""",unsafe_allow_html=True)

prices_ticker=""
for v,(p,tr,cl,desc) in {
    "Banganapalli":(28,"+2.1%","#4ade80","Export Quality"),
    "Totapuri":(18,"-0.8%","#fca5a5","Processing Grade"),
    "Neelam":(22,"+1.4%","#4ade80","Table Fruit"),
    "Rasalu":(30,"+3.2%","#4ade80","Premium Grade"),
}.items():
    sel="★ " if sel_variety==v else ""
    prices_ticker+=f"""
    <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.1);border-radius:8px;padding:8px 14px;border:1px solid {'rgba(251,191,36,0.5)' if sel else 'rgba(255,255,255,0.1)'};">
        <div>
            <div style="font-size:12px;font-weight:600;color:{'#fbbf24' if sel else 'white'};">{sel}{v}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.5);">{desc}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:18px;font-weight:700;color:white;">₹{p}</div>
            <div style="font-size:11px;font-weight:600;color:{cl};">{tr}</div>
        </div>
    </div>"""
st.markdown(prices_ticker+"</div></div></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════
if st.session_state.get("run",False):
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

        # ── RESULTS HEADER STRIP ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a7a1a,#2d6a4f);border-radius:14px;padding:24px 32px;margin-bottom:20px;position:relative;overflow:hidden;">
            <div style="position:absolute;right:24px;top:50%;transform:translateY(-50%);font-size:80px;opacity:0.08;">🏆</div>
            <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#86efac;margin-bottom:10px;">{tx['profit_summary']}</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
                <div><div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:3px;">{tx['variety_lbl']}</div><div style="font-size:20px;font-weight:700;color:white;">{rvar}</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:3px;">{tx['qty_lbl']}</div><div style="font-size:20px;font-weight:700;color:white;">{rt} Tonnes</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:3px;">{tx['best_market']}</div><div style="font-size:16px;font-weight:700;color:#fbbf24;line-height:1.25;">{bd}</div><div style="font-size:10px;color:rgba(255,255,255,0.5);">{bc}</div></div>
                <div><div style="font-size:10px;color:rgba(255,255,255,0.5);margin-bottom:3px;">{tx['est_profit']}</div><div style="font-size:30px;font-weight:800;color:#4ade80;">₹{bn:,}</div></div>
            </div>
        </div>""",unsafe_allow_html=True)

        # ── TOP 3 CARDS ──
        st.markdown(f'<div style="font-size:11px;font-weight:700;color:#1a7a1a;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;"><span style="width:4px;height:18px;background:#1a7a1a;border-radius:2px;display:inline-block;"></span>{tx["top3"]}</div>',unsafe_allow_html=True)

        medals=[("#fbbf24",tx["highest_profit"],True,"🥇"),
                ("#9ca3af",tx["second_best"],False,"🥈"),
                ("#cd7c4b",tx["third_best"],False,"🥉")]
        c3=st.columns(3)
        for i,(col,(acc,lbl_,istop,med)) in enumerate(zip(c3,medals)):
            if i>=len(top3): break
            r=top3.iloc[i]
            with col:
                st.markdown(f"""
                <div style="background:{'linear-gradient(145deg,#0f3320,#1a5c2e)' if istop else 'white'};
                    border-radius:14px;padding:22px;height:100%;
                    border:{'2px solid #fbbf24' if istop else '1px solid #e5e7eb'};
                    box-shadow:{'0 12px 40px rgba(251,191,36,0.2)' if istop else '0 4px 20px rgba(0,0,0,0.06)'};
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:12px;right:14px;font-size:24px;opacity:0.15;">{med}</div>
                    <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{acc};margin-bottom:10px;font-weight:700;">{lbl_}</div>
                    <div style="font-size:15px;font-weight:700;color:{'#f0fdf4' if istop else '#1a2e1f'};margin-bottom:4px;line-height:1.3;">{r['Name']}</div>
                    <div style="display:inline-flex;align-items:center;gap:4px;background:{'rgba(255,255,255,0.08)' if istop else '#f0fdf4'};border-radius:5px;padding:3px 9px;margin-bottom:14px;">
                        <span style="font-size:12px;">{r['icon']}</span>
                        <span style="font-size:10px;color:{r['color']};font-weight:600;">{r['Type']}</span>
                    </div>
                    <div style="font-size:28px;font-weight:800;color:{acc};margin-bottom:2px;">₹{int(r['Net_Profit']):,}</div>
                    <div style="font-size:10px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:14px;">{tx['net_profit_lbl']} · {r['Dist_km']} {tx['away_lbl']}</div>
                    <div style="border-top:1px solid {'rgba(255,255,255,0.08)' if istop else '#f3f4f6'};padding-top:12px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;">
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['revenue_lbl']}</div>
                            <div style="font-size:11px;font-weight:600;color:{'rgba(255,255,255,0.8)' if istop else '#374151'};">₹{int(r['Revenue']):,}</div>
                        </div>
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['transport_lbl']}</div>
                            <div style="font-size:11px;font-weight:600;color:#ef4444;">₹{int(r['Transport']):,}</div>
                        </div>
                        <div>
                            <div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:2px;">{tx['risk']}</div>
                            <div style="font-size:11px;font-weight:600;color:#f59e0b;">{r['Risk_pct']}%</div>
                        </div>
                    </div>
                </div>""",unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)

        # ── EXPERT TIP ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fffbeb,#fef9c3);border-radius:12px;padding:16px 22px;margin-bottom:22px;border-left:4px solid #fbbf24;display:flex;align-items:flex-start;gap:12px;">
            <span style="font-size:22px;flex-shrink:0;">💡</span>
            <div><div style="font-size:11px;font-weight:700;color:#92400e;letter-spacing:1px;text-transform:uppercase;margin-bottom:3px;">{tx['farmer_tip']}</div>
            <div style="font-size:13px;color:#78350f;line-height:1.5;">{tx['tip_text']}</div></div>
        </div>""",unsafe_allow_html=True)

        # ── CHARTS ──
        st.markdown(f'<div style="font-size:11px;font-weight:700;color:#1a7a1a;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;"><span style="width:4px;height:18px;background:#1a7a1a;border-radius:2px;display:inline-block;"></span>Market Analysis</div>',unsafe_allow_html=True)

        cc1,cc2=st.columns([3,2])
        with cc1:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);"><div style="font-size:13px;font-weight:700;color:#1a2e1f;margin-bottom:14px;">{tx["bar_title"]}</div>',unsafe_allow_html=True)
            fig=go.Figure(go.Bar(
                y=top10["Name"],x=top10["Net_Profit"],orientation="h",
                marker=dict(color=top10["color"].tolist(),line=dict(width=0)),
                text=[f"₹{int(v):,}" for v in top10["Net_Profit"]],
                textposition="outside",textfont=dict(size=11,color="#374151",family="Poppins"),
                hovertemplate="<b>%{y}</b><br>Net Profit: ₹%{x:,.0f}<extra></extra>",
            ))
            fig.update_layout(height=360,paper_bgcolor="white",plot_bgcolor="white",
                margin=dict(l=0,r=80,t=4,b=4),font=dict(family="Poppins"),
                xaxis=dict(showgrid=True,gridcolor="#f5f3ef",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
                yaxis=dict(autorange="reversed",tickfont=dict(size=11,color="#374151")),
                hoverlabel=dict(bgcolor="#1a3a1a",bordercolor="#fbbf24",font=dict(color="white")))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        with cc2:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);"><div style="font-size:13px;font-weight:700;color:#1a2e1f;margin-bottom:14px;">{tx["pie_title"]}</div>',unsafe_allow_html=True)
            pdata=top10.groupby("Type")["Net_Profit"].sum().reset_index()
            cmap={"Mandi":"#3b82f6","Processing":"#8b5cf6","Pulp":"#f59e0b","Pickle":"#ec4899",
                  "Local Export":"#16a34a","Abroad Export":"#d97706","Cold Storage":"#0891b2","FPO":"#65a30d"}
            fig2=go.Figure(go.Pie(
                labels=pdata["Type"],values=pdata["Net_Profit"],hole=0.55,
                marker=dict(colors=[cmap.get(c,"#888") for c in pdata["Type"]],line=dict(color="white",width=2)),
                textinfo="percent+label",textfont=dict(size=10,family="Poppins"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} · %{percent}<extra></extra>",
            ))
            fig2.update_layout(height=360,paper_bgcolor="white",margin=dict(l=8,r=8,t=4,b=4),
                legend=dict(font=dict(size=10,family="Poppins"),orientation="v",x=1.0,y=0.5),
                font=dict(family="Poppins"),
                annotations=[dict(text=f"<b>{rvar}</b>",x=0.5,y=0.5,font=dict(size=12,color="#374151"),showarrow=False)],
                hoverlabel=dict(bgcolor="#1a3a1a",bordercolor="#fbbf24",font=dict(color="white")))
            st.plotly_chart(fig2,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)

        # ── REVENUE VS TRANSPORT ──
        st.markdown('<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:20px;">',unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:13px;font-weight:700;color:#1a2e1f;margin-bottom:14px;">{tx["revenue_lbl"]} vs {tx["transport_lbl"]} — Top 10</div>',unsafe_allow_html=True)
        fig3=go.Figure()
        fig3.add_trace(go.Bar(name=tx["trans"],x=top10["Name"],y=top10["Transport"],marker_color="#ef4444",opacity=0.85,hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>"))
        fig3.add_trace(go.Bar(name=tx["net"],x=top10["Name"],y=top10["Net_Profit"],marker_color="#16a34a",opacity=0.9,hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>"))
        fig3.update_layout(barmode="stack",height=260,paper_bgcolor="white",plot_bgcolor="white",
            margin=dict(l=0,r=0,t=4,b=4),font=dict(family="Poppins"),
            xaxis=dict(tickfont=dict(size=10,color="#6b7280"),tickangle=-20),
            yaxis=dict(showgrid=True,gridcolor="#f5f3ef",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
            legend=dict(orientation="h",y=1.1,font=dict(size=11)),
            hoverlabel=dict(bgcolor="#1a3a1a",bordercolor="#fbbf24",font=dict(color="white")))
        st.plotly_chart(fig3,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

        # ── TABLE (simple, no styling that breaks) ──
        st.markdown(f'<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:20px;"><div style="font-size:13px;font-weight:700;color:#1a2e1f;margin-bottom:14px;">{tx["table_title"]}</div>',unsafe_allow_html=True)
        disp=top10[["Rank","Name","Type","Dist_km","Revenue","Transport","Risk_pct","Net_Profit"]].copy()
        disp.columns=[tx["rank"],tx["dest"],tx["cat"],tx["dist_km"],tx["rev"],tx["trans"],tx["risk"],tx["net"]]
        # Format columns without .style to avoid pandas compatibility issue
        disp[tx["rev"]] = disp[tx["rev"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["trans"]] = disp[tx["trans"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["net"]] = disp[tx["net"]].apply(lambda x: f"₹{int(x):,}")
        disp[tx["dist_km"]] = disp[tx["dist_km"]].apply(lambda x: f"{x:.1f}")
        disp[tx["risk"]] = disp[tx["risk"]].apply(lambda x: f"{x:.2f}%")
        st.dataframe(disp, use_container_width=True, height=320, hide_index=True)
        st.markdown("</div>",unsafe_allow_html=True)

        # ── MAP ──
        st.markdown(f'<div style="font-size:11px;font-weight:700;color:#1a7a1a;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px;"><span style="width:4px;height:18px;background:#1a7a1a;border-radius:2px;display:inline-block;"></span>{tx["map_title"]}</div>',unsafe_allow_html=True)
        st.markdown('<div style="background:white;border-radius:14px;padding:20px;border:1px solid #e5e7eb;box-shadow:0 4px 16px rgba(0,0,0,0.06);">',unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#6b7280;margin-bottom:12px;">🏠 Your farm &nbsp;|&nbsp; ★ Best destination (gold dashed route) &nbsp;|&nbsp; Colored dots = other top markets</div>',unsafe_allow_html=True)

        br=top3.iloc[0]
        m=folium.Map(location=[vlat,vlon],zoom_start=8,tiles="CartoDB Positron")

        # Farmer marker
        folium.Marker([vlat,vlon],
            popup=folium.Popup(f"<b style='font-family:Poppins'>{fname}</b><br>📍 {rv}",max_width=200),
            tooltip=tx["your_loc"],
            icon=folium.DivIcon(html="""
            <div style="background:#1a7a1a;border:3px solid #fbbf24;border-radius:50%;
                width:38px;height:38px;display:flex;align-items:center;justify-content:center;
                font-size:18px;box-shadow:0 3px 12px rgba(0,0,0,0.4);">🏠</div>
            """,icon_size=(38,38),icon_anchor=(19,19))
        ).add_to(m)

        # Best destination star
        folium.Marker([br["Lat"],br["Lon"]],
            popup=folium.Popup(
                f"<b style='font-family:Poppins'>{br['Name']}</b><br>{br['Type']}<br>"
                f"<span style='color:#16a34a;font-weight:700;font-size:14px'>₹{int(br['Net_Profit']):,}</span>",
                max_width=220),
            tooltip=tx["best_dest"],
            icon=folium.DivIcon(html="""
            <div style="background:#fbbf24;border:3px solid white;border-radius:50%;
                width:40px;height:40px;display:flex;align-items:center;justify-content:center;
                font-size:20px;font-weight:900;color:#1a1a1a;
                box-shadow:0 4px 16px rgba(251,191,36,0.6);">★</div>
            """,icon_size=(40,40),icon_anchor=(20,20))
        ).add_to(m)

        # Gold dashed route line
        folium.PolyLine(
            [(vlat,vlon),(br["Lat"],br["Lon"])],
            color="#fbbf24",weight=4,opacity=0.95,dash_array="10 6"
        ).add_to(m)

        # Other markets
        for _,row in top10.iloc[1:].iterrows():
            folium.CircleMarker(
                [row["Lat"],row["Lon"]],radius=10,
                color=row["color"],fill=True,fill_color=row["color"],fill_opacity=0.85,weight=2,
                popup=folium.Popup(
                    f"<b>{row['Name']}</b><br>{row['Type']}<br>₹{int(row['Net_Profit']):,}",
                    max_width=200),
                tooltip=f"{row['Name']} — ₹{int(row['Net_Profit']):,}",
            ).add_to(m)

        st_folium(m,width=None,height=520,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

st.markdown("</div>",unsafe_allow_html=True)

# ── FOOTER ──
st.markdown(f"""
<div style="background:#1a3a1a;padding:24px 32px;margin-top:32px;text-align:center;">
    <div style="font-size:16px;font-weight:700;color:white;margin-bottom:4px;">🥭 {tx['title']}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.4);">© 2025 · {tx['tagline']} · Andhra Pradesh · Telangana · Karnataka</div>
</div>""",unsafe_allow_html=True)
