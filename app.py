import streamlit as st
import sqlite3, bcrypt, random, requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="MangoNav",
                   page_icon="🥭", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English":{
        "title":"MangoNav","tagline":"Farmer Profit Intelligence",
        "sign_in":"Sign In","create_account":"Register",
        "phone":"Phone Number","password":"Password",
        "phone_ph":"10-digit mobile number","pass_ph":"Your password",
        "login_btn":"Sign In","forgot":"Forgot Password?",
        "otp_opt":"Login with OTP","send_otp":"Send OTP",
        "verify_otp":"Verify OTP","otp_ph":"6-digit OTP",
        "name":"Full Name","place":"Village / District","reg_btn":"Create Account",
        "select_lang":"Language","village_sel":"Select Your Village",
        "variety":"Mango Variety","quantity":"Quantity (Tonnes)",
        "analyze_btn":"Find My Best Market & Profit",
        "top3":"Top 3 Most Profitable Destinations",
        "bar_title":"Net Profit Comparison","pie_title":"Market Share",
        "map_title":"Route Map to Best Market",
        "rank":"Rank","dest":"Destination","cat":"Category",
        "dist_km":"Distance","rev":"Revenue (₹)","trans":"Transport (₹)",
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
        "tip_text":"Abroad Export gives the highest return (+7%) but needs quality grading. Local Export hubs are nearest and easiest to access for most farmers.",
        "no_results":"No markets found within 150km. Try a different village or variety.",
        "welcome":"Welcome back",
        "hero_title":"Find Your Most Profitable Mango Market",
        "hero_sub":"Select your village, variety and quantity below to discover your best market and maximum profit.",
        "fill_details":"Enter Your Farm Details",
    },
    "Telugu":{
        "title":"MangoNav","tagline":"రైతు లాభం సమాచారం",
        "sign_in":"లాగిన్","create_account":"నమోదు",
        "phone":"ఫోన్ నంబర్","password":"పాస్‌వర్డ్",
        "phone_ph":"10 అంకెల నంబర్","pass_ph":"మీ పాస్‌వర్డ్",
        "login_btn":"లాగిన్ చేయండి","forgot":"పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt":"OTP తో లాగిన్","send_otp":"OTP పంపండి",
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"6 అంకెల OTP",
        "name":"పూర్తి పేరు","place":"గ్రామం / జిల్లా","reg_btn":"ఖాతా తెరవండి",
        "select_lang":"భాష","village_sel":"మీ గ్రామం ఎంచుకోండి",
        "variety":"మామిడి రకం","quantity":"పరిమాణం (టన్నులు)",
        "analyze_btn":"ఉత్తమ మార్కెట్ & లాభం కనుగొనండి",
        "top3":"అగ్ర 3 లాభ గమ్యాలు",
        "bar_title":"నికర లాభం పోలిక","pie_title":"మార్కెట్ వాటా",
        "map_title":"ఉత్తమ మార్కెట్‌కు మార్గ మ్యాప్",
        "rank":"స్థానం","dest":"గమ్యం","cat":"వర్గం",
        "dist_km":"దూరం","rev":"ఆదాయం (₹)","trans":"రవాణా (₹)",
        "risk":"రిస్క్ (%)","net":"నికర లాభం (₹)",
        "logout":"నిష్క్రమించు","reset_pw":"పాస్‌వర్డ్ రీసెట్",
        "new_pw":"కొత్త పాస్‌వర్డ్","conf_pw":"నిర్ధారించండి","upd_pw":"అప్‌డేట్ చేయండి",
        "back":"తిరిగి","use_pw":"పాస్‌వర్డ్ ఉపయోగించండి",
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
        "welcome":"స్వాగతం",
        "hero_title":"మీ అత్యంత లాభదాయక మామిడి మార్కెట్ కనుగొనండి",
        "hero_sub":"మీ గ్రామం, రకం మరియు పరిమాణాన్ని ఎంచుకోండి.",
        "fill_details":"మీ పొలం వివరాలు నమోదు చేయండి",
    },
    "Hindi":{
        "title":"MangoNav","tagline":"किसान लाभ सूचना",
        "sign_in":"साइन इन","create_account":"पंजीकरण",
        "phone":"फ़ोन नंबर","password":"पासवर्ड",
        "phone_ph":"10 अंकों का नंबर","pass_ph":"आपका पासवर्ड",
        "login_btn":"साइन इन करें","forgot":"पासवर्ड भूल गए?",
        "otp_opt":"OTP से लॉगिन","send_otp":"OTP भेजें",
        "verify_otp":"OTP सत्यापित करें","otp_ph":"6 अंकों का OTP",
        "name":"पूरा नाम","place":"गाँव / जिला","reg_btn":"खाता बनाएं",
        "select_lang":"भाषा","village_sel":"अपना गाँव चुनें",
        "variety":"आम की किस्म","quantity":"मात्रा (टन)",
        "analyze_btn":"मेरा सर्वोत्तम बाज़ार और लाभ खोजें",
        "top3":"शीर्ष 3 लाभदायक गंतव्य",
        "bar_title":"शुद्ध लाभ तुलना","pie_title":"बाज़ार हिस्सेदारी",
        "map_title":"सर्वोत्तम बाज़ार का मार्ग",
        "rank":"रैंक","dest":"गंतव्य","cat":"श्रेणी",
        "dist_km":"दूरी","rev":"राजस्व (₹)","trans":"परिवहन (₹)",
        "risk":"जोखिम (%)","net":"शुद्ध लाभ (₹)",
        "logout":"साइन आउट","reset_pw":"पासवर्ड रीसेट",
        "new_pw":"नया पासवर्ड","conf_pw":"पुष्टि करें","upd_pw":"अपडेट करें",
        "back":"वापस","use_pw":"पासवर्ड का उपयोग करें",
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
        "welcome":"स्वागत है",
        "hero_title":"अपना सबसे लाभदायक आम बाज़ार खोजें",
        "hero_sub":"अपना गाँव, किस्म और मात्रा चुनें।",
        "fill_details":"अपने खेत की जानकारी दर्ज करें",
    },
    "Kannada":{
        "title":"MangoNav","tagline":"ರೈತ ಲಾಭ ಮಾಹಿತಿ",
        "sign_in":"ಸೈನ್ ಇನ್","create_account":"ನೋಂದಣಿ",
        "phone":"ಫೋನ್ ಸಂಖ್ಯೆ","password":"ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph":"10 ಅಂಕಿಯ ಸಂಖ್ಯೆ","pass_ph":"ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್",
        "login_btn":"ಸೈನ್ ಇನ್ ಮಾಡಿ","forgot":"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt":"OTP ಮೂಲಕ ಲಾಗಿನ್","send_otp":"OTP ಕಳುಹಿಸಿ",
        "verify_otp":"OTP ಪರಿಶೀಲಿಸಿ","otp_ph":"6 ಅಂಕಿಯ OTP",
        "name":"ಪೂರ್ಣ ಹೆಸರು","place":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ","reg_btn":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "select_lang":"ಭಾಷೆ","village_sel":"ನಿಮ್ಮ ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ",
        "variety":"ಮಾವಿನ ತಳಿ","quantity":"ಪ್ರಮಾಣ (ಟನ್)",
        "analyze_btn":"ನನ್ನ ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "top3":"ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title":"ನಿವ್ವಳ ಲಾಭ ಹೋಲಿಕೆ","pie_title":"ಮಾರುಕಟ್ಟೆ ಪಾಲು",
        "map_title":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ ಮಾರ್ಗ ನಕ್ಷೆ",
        "rank":"ಶ್ರೇಣಿ","dest":"ಗಮ್ಯ","cat":"ವರ್ಗ",
        "dist_km":"ದೂರ","rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)",
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
        "welcome":"ಸ್ವಾಗತ",
        "hero_title":"ನಿಮ್ಮ ಅತ್ಯಂತ ಲಾಭದಾಯಕ ಮಾವಿನ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "hero_sub":"ನಿಮ್ಮ ಗ್ರಾಮ, ತಳಿ ಮತ್ತು ಪ್ರಮಾಣ ಆಯ್ಕೆ ಮಾಡಿ.",
        "fill_details":"ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳು",
    },
}

# ══════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════
def init_db():
    conn=sqlite3.connect("farmers.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT,place TEXT,phone TEXT PRIMARY KEY,password TEXT)")
    conn.commit();conn.close()
def reg(n,p,ph,pw):
    conn=sqlite3.connect("farmers.db");h=bcrypt.hashpw(pw.encode(),bcrypt.gensalt())
    try: conn.execute("INSERT INTO users VALUES(?,?,?,?)",(n,p,ph,h));conn.commit();return True
    except: return False
    finally: conn.close()
def login(ph,pw):
    conn=sqlite3.connect("farmers.db");c=conn.cursor()
    c.execute("SELECT * FROM users WHERE phone=?",(ph,));u=c.fetchone();conn.close()
    if u and bcrypt.checkpw(pw.encode(),u[3]): return u
    return None
def get_u(ph):
    conn=sqlite3.connect("farmers.db");c=conn.cursor()
    c.execute("SELECT * FROM users WHERE phone=?",(ph,));u=c.fetchone();conn.close();return u
def upd_pw(ph,pw):
    conn=sqlite3.connect("farmers.db");h=bcrypt.hashpw(pw.encode(),bcrypt.gensalt())
    conn.execute("UPDATE users SET password=? WHERE phone=?",(h,ph));conn.commit();conn.close()
init_db()

for k,v in {"logged_in":False,"auth_mode":"login","otp_mode":False,"otp_sent":False,
            "otp_code":None,"otp_phone":None,"forgot":False,"f_otp_sent":False,
            "f_otp_ok":False,"f_code":None,"lang":"English","run":False,
            "last_village":None,"last_variety":"Banganapalli","last_tonnes":10.0}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════
# BASE CSS — Poppins font, green buttons
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
*{box-sizing:border-box;}
#MainMenu,footer,header,[data-testid="stDecoration"]{visibility:hidden;display:none!important;}
.stApp{font-family:'Poppins',sans-serif;}
.main .block-container{padding:0!important;max-width:100%!important;}
.stTextInput>label{display:none!important;}

/* GREEN PRIMARY BUTTON */
.stButton>button{
    font-family:'Poppins',sans-serif!important;font-size:14px!important;
    font-weight:700!important;border-radius:8px!important;
    padding:13px 24px!important;transition:all 0.18s!important;cursor:pointer!important;
    width:100%!important;
}
.stButton>button:not([kind="secondary"]){
    background:#16a34a!important;color:white!important;border:none!important;
    box-shadow:0 4px 18px rgba(22,163,74,0.45)!important;
}
.stButton>button:not([kind="secondary"]):hover{
    background:#15803d!important;transform:translateY(-1px)!important;
    box-shadow:0 6px 24px rgba(22,163,74,0.55)!important;
}
.stButton>button[kind="secondary"]{
    background:rgba(255,255,255,0.12)!important;color:rgba(255,255,255,0.8)!important;
    border:1.5px solid rgba(255,255,255,0.25)!important;
    font-size:12px!important;padding:10px!important;
}
.stButton>button[kind="secondary"]:hover{
    background:rgba(255,255,255,0.18)!important;color:white!important;
}

/* LOGIN inputs */
.stTextInput>div>div>input{
    background:rgba(255,255,255,0.12)!important;
    border:1.5px solid rgba(255,255,255,0.25)!important;
    border-radius:8px!important;color:white!important;
    font-family:'Poppins',sans-serif!important;font-size:14px!important;padding:13px 16px!important;
}
.stTextInput>div>div>input:focus{border-color:#4ade80!important;outline:none!important;}
.stTextInput>div>div>input::placeholder{color:rgba(255,255,255,0.4)!important;}

/* SIDEBAR */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#052e16,#14532d)!important;border-right:none!important;}
[data-testid="stSidebar"] label{color:#86efac!important;font-size:10px!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(134,239,172,0.2)!important;color:#dcfce7!important;border-radius:8px!important;}

/* DASHBOARD form selects */
.dash-select .stSelectbox>label{font-size:11px!important;font-weight:700!important;color:#1f2937!important;letter-spacing:0.3px!important;text-transform:uppercase!important;}
.dash-select .stSelectbox>div>div{background:white!important;border:2px solid #d1d5db!important;border-radius:8px!important;color:#111827!important;font-family:'Poppins',sans-serif!important;font-size:14px!important;}
.dash-select .stNumberInput>label{font-size:11px!important;font-weight:700!important;color:#1f2937!important;letter-spacing:0.3px!important;text-transform:uppercase!important;}
.dash-select .stNumberInput>div>div>input{background:white!important;border:2px solid #d1d5db!important;border-radius:8px!important;color:#111827!important;font-family:'Poppins',sans-serif!important;font-size:14px!important;padding:10px 14px!important;}

/* DASHBOARD run button — force green on white bg */
.run-area .stButton>button{
    background:linear-gradient(135deg,#16a34a,#15803d)!important;
    color:white!important;border:none!important;font-size:15px!important;
    padding:16px 24px!important;border-radius:10px!important;
    box-shadow:0 6px 24px rgba(22,163,74,0.45)!important;
    font-weight:700!important;
}
.run-area .stButton>button:hover{
    background:linear-gradient(135deg,#15803d,#166534)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 10px 30px rgba(22,163,74,0.55)!important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    lang=st.session_state.lang; tx=T[lang]

    # Full-page agricultural field background (green paddy/crop field)
    st.markdown("""
    <style>
    [data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important;}
    .stApp{
        background-image:
            linear-gradient(to right, rgba(5,46,22,0.92) 0%, rgba(5,46,22,0.75) 50%, rgba(5,46,22,0.55) 100%),
            url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=90&fit=crop&crop=center')!important;
        background-size:cover!important;background-position:center!important;
        background-repeat:no-repeat!important;min-height:100vh!important;
    }
    .stSelectbox>div>div{background:rgba(255,255,255,0.12)!important;border:1.5px solid rgba(255,255,255,0.25)!important;color:white!important;border-radius:8px!important;}
    .stSelectbox>label{color:rgba(255,255,255,0.6)!important;font-size:10px!important;letter-spacing:1px!important;}
    .main .block-container{padding-top:0!important;}
    </style>""", unsafe_allow_html=True)

    # ── TOP GREEN NAV BAR ──
    st.markdown(f"""
    <div style="background:rgba(5,46,22,0.7);backdrop-filter:blur(12px);
        padding:14px 40px;display:flex;align-items:center;justify-content:space-between;
        border-bottom:1px solid rgba(74,222,128,0.15);">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:44px;height:44px;background:linear-gradient(135deg,#16a34a,#4ade80);
                border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;
                box-shadow:0 4px 16px rgba(22,163,74,0.4);">🥭</div>
            <div>
                <div style="font-family:'Poppins',sans-serif;font-size:24px;font-weight:800;color:white;line-height:1;">{tx['title']}</div>
                <div style="font-size:10px;color:rgba(74,222,128,0.7);letter-spacing:3px;text-transform:uppercase;margin-top:2px;">{tx['tagline']}</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:32px;">
            <div style="font-size:13px;color:rgba(255,255,255,0.6);font-weight:500;">Home</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.6);font-weight:500;">About</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.6);font-weight:500;">Contact</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── MAIN LAYOUT: LEFT HERO + RIGHT FORM ──
    left_col, right_col = st.columns([1.2, 0.9])

    with left_col:
        # Language picker at top of left column
        lc1, lc2 = st.columns([3, 1])
        with lc2:
            c = st.selectbox(tx["select_lang"], ["English","Telugu","Hindi","Kannada"],
                index=["English","Telugu","Hindi","Kannada"].index(lang),
                key="lang_sel", label_visibility="collapsed")
            if c != lang: st.session_state.lang=c; st.rerun()

        st.markdown(f"""
        <div style="padding:50px 40px 40px 48px;">
            <h1 style="font-family:'Poppins',sans-serif;font-size:52px;color:white;
                font-weight:800;line-height:1.1;margin-bottom:20px;
                text-shadow:0 4px 20px rgba(0,0,0,0.3);">
                {tx['hero_title']}
            </h1>
            <p style="font-size:16px;color:rgba(255,255,255,0.75);line-height:1.8;
                max-width:420px;margin-bottom:36px;">
                {tx['hero_sub']}
            </p>
            <div style="display:flex;gap:16px;flex-wrap:wrap;">
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                    border-radius:50px;padding:8px 20px;font-size:13px;color:white;font-weight:600;">
                    ✅ Real Market Data
                </div>
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                    border-radius:50px;padding:8px 20px;font-size:13px;color:white;font-weight:600;">
                    📍 Route Maps
                </div>
                <div style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                    border-radius:50px;padding:8px 20px;font-size:13px;color:white;font-weight:600;">
                    🌐 4 Languages
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div style="height:30px"></div>', unsafe_allow_html=True)
        # LOGIN CARD
        st.markdown("""
        <div style="background:rgba(5,30,12,0.88);backdrop-filter:blur(30px);
            border:1px solid rgba(74,222,128,0.2);border-radius:20px;
            padding:36px 32px 28px;margin:0 32px 0 0;
            box-shadow:0 30px 80px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)

        tb1, tb2 = st.columns(2)
        with tb1:
            if st.button(tx["sign_in"], key="tab_si", use_container_width=True,
                type="primary" if st.session_state.auth_mode=="login" else "secondary"):
                st.session_state.auth_mode="login"; st.session_state.otp_mode=False
                st.session_state.forgot=False; st.rerun()
        with tb2:
            if st.button(tx["create_account"], key="tab_ca", use_container_width=True,
                type="primary" if st.session_state.auth_mode=="register" else "secondary"):
                st.session_state.auth_mode="register"; st.session_state.otp_mode=False
                st.session_state.forgot=False; st.rerun()

        st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)

        def lbl(t):
            st.markdown(f'<div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(74,222,128,0.75);margin-bottom:7px;font-weight:600;">{t}</div>', unsafe_allow_html=True)

        # FORGOT
        if st.session_state.forgot:
            lbl(tx["reset_pw"])
            fph = st.text_input("_fph", placeholder=tx["phone_ph"], key="fp_ph", label_visibility="collapsed")
            if not st.session_state.f_otp_sent:
                if st.button(tx["send_otp"], key="fp_send", use_container_width=True):
                    if fph and len(fph)==10 and fph.isdigit():
                        u=get_u(fph)
                        if u:
                            code=str(random.randint(100000,999999))
                            st.session_state.f_code=code; st.session_state.f_otp_sent=True; st.session_state.otp_phone=fph
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            elif not st.session_state.f_otp_ok:
                lbl(tx["otp_ph"])
                eo = st.text_input("_fov", placeholder=tx["otp_ph"], key="fp_ov", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="fp_ver", use_container_width=True):
                    if eo==st.session_state.f_code: st.session_state.f_otp_ok=True; st.rerun()
                    else: st.error("Incorrect OTP.")
            else:
                lbl(tx["new_pw"]); np_=st.text_input("_npw", placeholder=tx["new_pw"], type="password", key="fp_np", label_visibility="collapsed")
                lbl(tx["conf_pw"]); cp_=st.text_input("_cpw", placeholder=tx["conf_pw"], type="password", key="fp_cp", label_visibility="collapsed")
                if st.button(tx["upd_pw"], key="fp_upd", use_container_width=True):
                    if np_ and np_==cp_: upd_pw(st.session_state.otp_phone,np_); st.success("Updated."); st.session_state.forgot=False; st.session_state.f_otp_sent=False; st.session_state.f_otp_ok=False; st.session_state.f_code=None; st.rerun()
                    else: st.error("Passwords do not match.")
            if st.button(tx["back"], key="fp_back", use_container_width=True, type="secondary"): st.session_state.forgot=False; st.rerun()

        # OTP LOGIN
        elif st.session_state.auth_mode=="login" and st.session_state.otp_mode:
            lbl(tx["phone"]); op=st.text_input("_op", placeholder=tx["phone_ph"], key="otp_ph_in", label_visibility="collapsed")
            if not st.session_state.otp_sent:
                if st.button(tx["send_otp"], key="s_otp", use_container_width=True):
                    if op and len(op)==10 and op.isdigit():
                        u=get_u(op)
                        if u:
                            code=str(random.randint(100000,999999)); st.session_state.otp_code=code; st.session_state.otp_sent=True; st.session_state.otp_phone=op
                            st.info(f"Demo OTP: **{code}**"); st.rerun()
                        else: st.error("No account found.")
                    else: st.warning("Enter valid 10-digit number.")
            else:
                lbl(tx["otp_ph"]); eo=st.text_input("_eov", placeholder=tx["otp_ph"], key="otp_v", label_visibility="collapsed")
                if st.button(tx["verify_otp"], key="v_otp", use_container_width=True):
                    if eo==st.session_state.otp_code: u=get_u(st.session_state.otp_phone); st.session_state.logged_in=True; st.session_state.user=u; st.session_state.otp_sent=False; st.rerun()
                    else: st.error("Incorrect OTP.")
            if st.button(tx["use_pw"], key="use_pw_btn", use_container_width=True, type="secondary"): st.session_state.otp_mode=False; st.rerun()

        # PASSWORD LOGIN
        elif st.session_state.auth_mode=="login":
            lbl(tx["phone"]); ph=st.text_input("_lph", placeholder=tx["phone_ph"], key="l_ph", label_visibility="collapsed")
            lbl(tx["password"]); pw=st.text_input("_lpw", placeholder=tx["pass_ph"], type="password", key="l_pw", label_visibility="collapsed")
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
            if st.button(tx["login_btn"], key="do_login", use_container_width=True):
                if ph and pw:
                    u=login(ph,pw)
                    if u: st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
                    else: st.error("Incorrect phone or password.")
                else: st.warning("Please fill all fields.")
            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
            fa, oa = st.columns(2)
            with fa:
                if st.button(tx["forgot"], key="frg", use_container_width=True, type="secondary"): st.session_state.forgot=True; st.rerun()
            with oa:
                if st.button(tx["otp_opt"], key="otp_sw", use_container_width=True, type="secondary"): st.session_state.otp_mode=True; st.rerun()

        # REGISTER
        else:
            for label,key_,ph_,is_pw in [(tx["name"],"r_nm","Your full name",False),(tx["place"],"r_pl","Village, District",False),(tx["phone"],"r_ph",tx["phone_ph"],False),(tx["password"],"r_pw",tx["pass_ph"],True)]:
                lbl(label)
                if is_pw: st.text_input(f"_{key_}",placeholder=ph_,key=key_,type="password",label_visibility="collapsed")
                else: st.text_input(f"_{key_}",placeholder=ph_,key=key_,label_visibility="collapsed")
            if st.button(tx["reg_btn"], key="do_reg", use_container_width=True):
                n=st.session_state.get("r_nm",""); p=st.session_state.get("r_pl",""); ph=st.session_state.get("r_ph",""); pw=st.session_state.get("r_pw","")
                if n and p and ph and pw:
                    if reg(n,p,ph,pw): st.success("Account created! Please sign in."); st.session_state.auth_mode="login"; st.rerun()
                    else: st.error("Phone already registered.")
                else: st.warning("All fields required.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:12px;font-size:10px;color:rgba(255,255,255,0.2);letter-spacing:2px;">SECURE · ENCRYPTED · YOUR DATA IS SAFE</div>', unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_all():
    def s(p):
        try: df=pd.read_csv(p);df.columns=df.columns.str.strip().str.lower();return df
        except: return pd.DataFrame()
    return (s("Village data.csv"),s("cleaned_price_data.csv"),s("cleaned_mandi_location.csv"),
            s("cleaned_processing_facilities.csv"),s("Pulp_units_merged_lat_long.csv"),
            s("cleaned_pickle_units.csv"),s("cleaned_local_export.csv"),s("cleaned_abroad_export.csv"),
            s("cleaned_cold_storage.csv"),s("cleaned_fpo.csv"))

villages,prices,geo,processing,pulp,pickle_u,local_exp,abroad_exp,cold,fpo=load_all()

def hav(la1,lo1,la2,lo2):
    R=6371;la1,lo1,la2,lo2=map(np.radians,[la1,lo1,la2,lo2])
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

def vlist():
    nc,_,_=dcols(villages)
    if nc and nc in villages.columns: return sorted(villages[nc].dropna().unique().tolist())
    return ["Default Village"]

def vcoords(vn):
    nc,lc,loc=dcols(villages)
    if nc and lc and loc:
        r=villages[villages[nc]==vn]
        if not r.empty: return float(r.iloc[0][lc]),float(r.iloc[0][loc])
    return 15.9129,79.7400

def base_price(vlat,vlon):
    try:
        m=prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices.copy()
        lc=next((c for c in m.columns if "lat" in c.lower()),None); loc=next((c for c in m.columns if "lon" in c.lower()),None); pc=next((c for c in m.columns if "price" in c.lower()),None)
        if lc and loc and pc:
            m=m.dropna(subset=[lc,loc,pc]); m["d"]=m.apply(lambda r:hav(vlat,vlon,r[lc],r[loc]),axis=1)
            return float(m.loc[m["d"].idxmin()][pc])
    except: pass
    return 25.0

def osm_route(lat1,lon1,lat2,lon2):
    try:
        r=requests.get(f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson",timeout=8).json()
        if "routes" in r and r["routes"]:
            return [(c[1],c[0]) for c in r["routes"][0]["geometry"]["coordinates"]],round(r["routes"][0]["distance"]/1000,2)
    except: pass
    return [(lat1,lon1),(lat2,lon2)],round(hav(lat1,lon1,lat2,lon2),2)

def road_dist(vlat,vlon,rlat,rlon):
    try:
        r=requests.get(f"http://router.project-osrm.org/route/v1/driving/{vlon},{vlat};{rlon},{rlat}?overview=false",timeout=5).json()
        if "routes" in r and r["routes"]: return round(r["routes"][0]["distance"]/1000,2)
    except: pass
    return round(hav(vlat,vlon,rlat,rlon),2)

def analyse(vlat,vlon,variety,tonnes):
    VACC={"Mandi":["Banganapalli","Totapuri","Neelam","Rasalu"],"Processing":["Totapuri","Neelam"],
          "Pulp":["Totapuri"],"Pickle":["Totapuri","Rasalu"],"Local Export":["Banganapalli"],
          "Abroad Export":["Banganapalli"],"Cold Storage":["Banganapalli","Totapuri","Neelam","Rasalu"],
          "FPO":["Banganapalli","Totapuri","Neelam","Rasalu"]}
    mdf=prices.merge(geo,on="market",how="left") if ("market" in prices.columns and "market" in geo.columns and not geo.empty) else prices
    CATS={"Mandi":{"mg":0.00,"col":"#3b82f6","ic":"🏪","df":mdf},
          "Processing":{"mg":0.03,"col":"#7c3aed","ic":"🏭","df":processing},
          "Pulp":{"mg":0.04,"col":"#d97706","ic":"🧃","df":pulp},
          "Pickle":{"mg":0.025,"col":"#db2777","ic":"🫙","df":pickle_u},
          "Local Export":{"mg":0.05,"col":"#16a34a","ic":"🚛","df":local_exp},
          "Abroad Export":{"mg":0.07,"col":"#b45309","ic":"✈️","df":abroad_exp},
          "Cold Storage":{"mg":0.01,"col":"#0891b2","ic":"🧊","df":cold},
          "FPO":{"mg":0.02,"col":"#65a30d","ic":"👥","df":fpo}}
    HND={"Mandi":0,"Processing":300,"Pulp":400,"Pickle":250,"Local Export":500,"Abroad Export":700,"Cold Storage":200,"FPO":150}
    DLY={"Mandi":0,"Processing":7,"Pulp":10,"Pickle":5,"Local Export":14,"Abroad Export":30,"Cold Storage":3,"FPO":2}
    bp=base_price(vlat,vlon); rows=[]
    for cat,cfg in CATS.items():
        if variety not in VACC.get(cat,[]): continue
        df_=cfg["df"]
        if df_ is None or df_.empty: continue
        nc,lc,loc=dcols(df_)
        if not lc or not loc: continue
        for _,row in df_.iterrows():
            try:
                rlat=float(row[lc]);rlon=float(row[loc])
                if hav(vlat,vlon,rlat,rlon)>150: continue
                dist=road_dist(vlat,vlon,rlat,rlon)
                nm=str(row[nc]) if nc and nc in row.index else cat
                adj=bp*(1+cfg["mg"]);rev=adj*1000*tonnes
                tra=5000+dist*200*tonnes+300*tonnes
                fin=rev*(DLY.get(cat,0)/365)*0.12
                rr=(0.004*(dist/10))+0.002;rc=rev*rr
                net=rev-tra-HND.get(cat,0)*tonnes-fin-rc
                rows.append({"Type":cat,"Name":nm,"Dist_km":dist,"Revenue":round(rev),"Transport":round(tra),"Risk_pct":round(rr*100,2),"Net_Profit":round(net),"Lat":rlat,"Lon":rlon,"color":cfg["col"],"icon":cfg["ic"]})
            except: continue
    if not rows: return pd.DataFrame()
    df=pd.DataFrame(rows).drop_duplicates(subset=["Type","Name"]).sort_values("Net_Profit",ascending=False).reset_index(drop=True)
    df["Rank"]=df.index+1; return df

# ══════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════
lang=st.session_state.get("lang","English"); tx=T[lang]
fname=st.session_state.user[0]; fplace=st.session_state.user[1]

st.markdown("<style>.stApp{background:#f3f4f6!important;}</style>", unsafe_allow_html=True)

# ── GREEN NAV ──
st.markdown(f"""
<div style="background:linear-gradient(135deg,#052e16,#15803d);padding:0 32px;height:68px;
    display:flex;align-items:center;justify-content:space-between;
    box-shadow:0 4px 28px rgba(0,0,0,0.25);position:sticky;top:0;z-index:999;">
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:44px;height:44px;background:linear-gradient(135deg,#16a34a,#4ade80);
            border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;">🥭</div>
        <div>
            <div style="font-family:'Poppins',sans-serif;font-size:22px;font-weight:800;color:white;">{tx['title']}</div>
            <div style="font-size:9px;color:rgba(74,222,128,0.65);letter-spacing:3px;text-transform:uppercase;">{tx['tagline']}</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:40px;height:40px;background:rgba(255,255,255,0.12);border:2px solid rgba(255,255,255,0.2);
            border-radius:50%;display:flex;align-items:center;justify-content:center;
            font-size:15px;font-weight:800;color:white;">{fname[0].upper()}</div>
        <div>
            <div style="font-size:14px;color:white;font-weight:700;">{fname}</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.5);">📍 {fplace}</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""<div style="padding:16px 4px 10px;"><div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#86efac;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid rgba(134,239,172,0.1);">Settings</div></div>""", unsafe_allow_html=True)
    sl=st.selectbox(tx["select_lang"],["English","Telugu","Hindi","Kannada"],index=["English","Telugu","Hindi","Kannada"].index(lang))
    if sl!=lang: st.session_state.lang=sl; st.rerun()
    st.markdown(f'<div style="margin-top:16px;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#86efac;margin-bottom:10px;">{tx["live_prices"]}</div>', unsafe_allow_html=True)
    for v,(p,tr,cl) in {"Banganapalli":(28,"↑ +2.1%","#4ade80"),"Totapuri":(18,"↓ -0.8%","#f87171"),"Neelam":(22,"↑ +1.4%","#4ade80"),"Rasalu":(30,"↑ +3.2%","#4ade80")}.items():
        st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 10px;margin-bottom:5px;background:rgba(255,255,255,0.05);border-radius:8px;"><div><div style="font-size:12px;color:#dcfce7;font-weight:600;">{v}</div><div style="font-size:10px;color:#86efac;">₹{p}/kg</div></div><div style="font-size:12px;font-weight:800;color:{cl};">{tr}</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    if st.button(tx["logout"], use_container_width=True, type="secondary"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

villages_list = vlist()

# ── HERO WITH MANGO TREE IMAGE ──
st.markdown(f"""
<div style="
    background-image:
        linear-gradient(to right, rgba(5,46,22,0.85) 0%, rgba(5,46,22,0.60) 60%, rgba(5,46,22,0.40) 100%),
        url('https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=1400&q=90&fit=crop&crop=right');
    background-size:cover;background-position:center right;
    padding:56px 48px 52px;">
    <div style="max-width:580px;">
        <h1 style="font-family:'Poppins',sans-serif;font-size:44px;color:white;font-weight:800;
            line-height:1.15;margin-bottom:14px;text-shadow:0 3px 16px rgba(0,0,0,0.4);">
            {tx['hero_title']}
        </h1>
        <p style="font-size:16px;color:rgba(255,255,255,0.78);line-height:1.75;margin-bottom:0;">
            {tx['hero_sub']}
        </p>
    </div>
</div>""", unsafe_allow_html=True)

# ── PRICE TICKER ──
st.markdown(f"""
<div style="background:#052e16;padding:12px 48px;border-bottom:1px solid rgba(74,222,128,0.12);">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
        <span style="font-size:11px;font-weight:700;color:#4ade80;letter-spacing:2px;text-transform:uppercase;margin-right:10px;">{tx['live_prices']}</span>
        <span style="font-size:13px;color:white;font-weight:500;">Banganapalli <b style="color:#4ade80;">₹28</b> ↑+2.1%</span>
        <span style="color:rgba(74,222,128,0.25);margin:0 14px;">|</span>
        <span style="font-size:13px;color:white;font-weight:500;">Totapuri <b style="color:#f87171;">₹18</b> ↓-0.8%</span>
        <span style="color:rgba(74,222,128,0.25);margin:0 14px;">|</span>
        <span style="font-size:13px;color:white;font-weight:500;">Neelam <b style="color:#4ade80;">₹22</b> ↑+1.4%</span>
        <span style="color:rgba(74,222,128,0.25);margin:0 14px;">|</span>
        <span style="font-size:13px;color:white;font-weight:500;">Rasalu <b style="color:#4ade80;">₹30</b> ↑+3.2%</span>
    </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FORM CARD + RUN BUTTON
# ══════════════════════════════════════════════════════════════
st.markdown('<div style="padding:0 32px 36px;background:#f3f4f6;">', unsafe_allow_html=True)

# White card wrapping entire form including button
st.markdown(f"""
<div style="background:white;border-radius:16px;padding:28px 32px 28px;
    box-shadow:0 8px 40px rgba(0,0,0,0.10);border:1px solid #e5e7eb;margin-bottom:24px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:22px;padding-bottom:16px;border-bottom:2px solid #f3f4f6;">
        <div style="width:38px;height:38px;background:#052e16;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:20px;">🌾</div>
        <div>
            <div style="font-size:17px;font-weight:800;color:#052e16;">{tx['fill_details']}</div>
            <div style="font-size:12px;color:#9ca3af;margin-top:1px;">All fields required to calculate your profit</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# Dropdowns row
st.markdown('<div class="dash-select">', unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns([2.2, 1.8, 1.0])
with fc1:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">📍 {tx["village_sel"]}</p>', unsafe_allow_html=True)
    sel_village = st.selectbox("__v", villages_list, key="sel_v", label_visibility="collapsed")
with fc2:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">🥭 {tx["variety"]}</p>', unsafe_allow_html=True)
    sel_variety = st.selectbox("__var", ["Banganapalli","Totapuri","Neelam","Rasalu"], key="sel_var", label_visibility="collapsed")
with fc3:
    st.markdown(f'<p style="font-size:11px;font-weight:700;color:#374151;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">⚖️ {tx["quantity"]}</p>', unsafe_allow_html=True)
    sel_tonnes = st.number_input("__t", min_value=0.5, value=10.0, step=0.5, key="sel_t", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# RUN BUTTON — full width, clearly visible green
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
st.markdown('<div class="run-area">', unsafe_allow_html=True)
run_clicked = st.button(f"🔍   {tx['analyze_btn']}", key="run_btn", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if run_clicked:
    st.session_state.run = True
    st.session_state.last_village = sel_village
    st.session_state.last_variety = sel_variety
    st.session_state.last_tonnes  = sel_tonnes

# ══════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════
if st.session_state.get("run", False):
    rv   = st.session_state.get("last_village", sel_village)
    rvar = st.session_state.get("last_variety",  sel_variety)
    rt   = st.session_state.get("last_tonnes",   sel_tonnes)

    with st.spinner("Analysing nearby markets..."):
        vlat, vlon = vcoords(rv)
        df_res = analyse(vlat, vlon, rvar, rt)

    if df_res.empty:
        st.warning(tx["no_results"])
    else:
        top3 = df_res.head(3)
        bn=int(top3.iloc[0]["Net_Profit"]); bd=top3.iloc[0]["Name"]; bc=top3.iloc[0]["Type"]

        # SUMMARY
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#052e16,#15803d);border-radius:16px;
            padding:26px 36px;margin-bottom:24px;border:1px solid rgba(74,222,128,0.2);
            position:relative;overflow:hidden;">
            <div style="position:absolute;right:32px;top:50%;transform:translateY(-50%);font-size:90px;opacity:0.07;">🏆</div>
            <div style="font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#4ade80;margin-bottom:12px;font-weight:700;">{tx['profit_summary']}</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
                <div><div style="font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:4px;">{tx['variety_lbl']}</div><div style="font-size:22px;font-weight:800;color:white;">{rvar}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:4px;">{tx['qty_lbl']}</div><div style="font-size:22px;font-weight:800;color:white;">{rt} T</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:4px;">{tx['best_market']}</div><div style="font-size:18px;font-weight:800;color:#4ade80;line-height:1.2;">{bd}</div><div style="font-size:11px;color:rgba(255,255,255,0.4);">{bc}</div></div>
                <div><div style="font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:4px;">{tx['est_profit']}</div><div style="font-size:34px;font-weight:900;color:#4ade80;">₹{bn:,}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # TOP 3 CARDS
        st.markdown(f'<div style="font-size:12px;font-weight:800;color:#052e16;letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:10px;"><span style="display:inline-block;width:5px;height:22px;background:#16a34a;border-radius:3px;"></span>{tx["top3"]}</div>', unsafe_allow_html=True)

        medals=[("#f59e0b",tx["highest_profit"],True,"🥇","linear-gradient(145deg,#052e16,#14532d)"),
                ("#6b7280",tx["second_best"],False,"🥈","white"),
                ("#92400e",tx["third_best"],False,"🥉","white")]
        c3=st.columns(3)
        for i,(col,(acc,lbl_,istop,med,bg)) in enumerate(zip(c3,medals)):
            if i>=len(top3): break
            r=top3.iloc[i]
            with col:
                st.markdown(f"""
                <div style="background:{bg};border-radius:16px;padding:24px;height:100%;
                    border:{'2px solid rgba(245,158,11,0.5)' if istop else '1px solid #e5e7eb'};
                    box-shadow:{'0 16px 48px rgba(5,46,22,0.25)' if istop else '0 4px 20px rgba(0,0,0,0.07)'};
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:14px;right:16px;font-size:28px;opacity:0.14;">{med}</div>
                    <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:{acc};margin-bottom:10px;font-weight:800;">{lbl_}</div>
                    <div style="font-size:17px;font-weight:800;color:{'#f0fdf4' if istop else '#052e16'};margin-bottom:5px;line-height:1.3;">{r['Name']}</div>
                    <div style="display:inline-flex;align-items:center;gap:5px;background:{'rgba(255,255,255,0.08)' if istop else '#f0fdf4'};border-radius:6px;padding:4px 10px;margin-bottom:16px;">
                        <span style="font-size:14px;">{r['icon']}</span>
                        <span style="font-size:11px;color:{r['color']};font-weight:700;">{r['Type']}</span>
                    </div>
                    <div style="font-size:32px;font-weight:900;color:{acc};margin-bottom:2px;">₹{int(r['Net_Profit']):,}</div>
                    <div style="font-size:11px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:18px;">{r['Dist_km']} {tx['away_lbl']}</div>
                    <div style="border-top:1px solid {'rgba(255,255,255,0.08)' if istop else '#f3f4f6'};padding-top:14px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;">
                        <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:3px;">{tx['revenue_lbl']}</div><div style="font-size:13px;font-weight:800;color:{'rgba(255,255,255,0.9)' if istop else '#16a34a'};">₹{int(r['Revenue']):,}</div></div>
                        <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:3px;">{tx['transport_lbl']}</div><div style="font-size:13px;font-weight:800;color:#ef4444;">₹{int(r['Transport']):,}</div></div>
                        <div><div style="font-size:9px;color:{'rgba(255,255,255,0.4)' if istop else '#9ca3af'};margin-bottom:3px;">{tx['risk']}</div><div style="font-size:13px;font-weight:800;color:#f59e0b;">{r['Risk_pct']}%</div></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

        # TIP
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:12px;padding:16px 22px;margin-bottom:24px;border-left:5px solid #f59e0b;display:flex;align-items:flex-start;gap:14px;">
            <span style="font-size:22px;flex-shrink:0;">💡</span>
            <div><div style="font-size:12px;font-weight:800;color:#92400e;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">{tx['farmer_tip']}</div>
            <div style="font-size:14px;color:#78350f;line-height:1.6;">{tx['tip_text']}</div></div>
        </div>""", unsafe_allow_html=True)

        # CHARTS
        cc1,cc2=st.columns([3,2])
        with cc1:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:22px;border:1px solid #e5e7eb;box-shadow:0 4px 18px rgba(0,0,0,0.06);"><div style="font-size:14px;font-weight:800;color:#052e16;margin-bottom:14px;">{tx["bar_title"]}</div>', unsafe_allow_html=True)
            fig=go.Figure(go.Bar(y=top3["Name"],x=top3["Net_Profit"],orientation="h",
                marker=dict(color=["#f59e0b","#6b7280","#b45309"],line=dict(width=0)),
                text=[f"₹{int(v):,}" for v in top3["Net_Profit"]],textposition="outside",
                textfont=dict(size=13,color="#374151",family="Poppins"),
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>"))
            fig.update_layout(height=220,paper_bgcolor="white",plot_bgcolor="white",margin=dict(l=0,r=90,t=4,b=4),font=dict(family="Poppins"),
                xaxis=dict(showgrid=True,gridcolor="#f3f4f6",zeroline=False,tickfont=dict(size=10,color="#9ca3af"),tickprefix="₹"),
                yaxis=dict(autorange="reversed",tickfont=dict(size=13,color="#052e16")),
                hoverlabel=dict(bgcolor="#052e16",bordercolor="#4ade80",font=dict(color="white")))
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with cc2:
            st.markdown(f'<div style="background:white;border-radius:14px;padding:22px;border:1px solid #e5e7eb;box-shadow:0 4px 18px rgba(0,0,0,0.06);"><div style="font-size:14px;font-weight:800;color:#052e16;margin-bottom:14px;">{tx["pie_title"]}</div>', unsafe_allow_html=True)
            pdata=top3.groupby("Type")["Net_Profit"].sum().reset_index()
            cmap={"Mandi":"#3b82f6","Processing":"#7c3aed","Pulp":"#d97706","Pickle":"#db2777","Local Export":"#16a34a","Abroad Export":"#b45309","Cold Storage":"#0891b2","FPO":"#65a30d"}
            fig2=go.Figure(go.Pie(labels=pdata["Type"],values=pdata["Net_Profit"],hole=0.56,
                marker=dict(colors=[cmap.get(c,"#888") for c in pdata["Type"]],line=dict(color="white",width=3)),
                textinfo="percent+label",textfont=dict(size=12,family="Poppins"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} · %{percent}<extra></extra>"))
            fig2.update_layout(height=220,paper_bgcolor="white",margin=dict(l=8,r=8,t=4,b=4),
                legend=dict(font=dict(size=11,family="Poppins"),orientation="v",x=1.0,y=0.5),font=dict(family="Poppins"),
                annotations=[dict(text=f"<b>{rvar}</b>",x=0.5,y=0.5,font=dict(size=13,color="#052e16"),showarrow=False)],
                hoverlabel=dict(bgcolor="#052e16",bordercolor="#4ade80",font=dict(color="white")))
            st.plotly_chart(fig2,use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        # TABLE
        st.markdown(f'<div style="background:white;border-radius:14px;padding:22px;border:1px solid #e5e7eb;box-shadow:0 4px 18px rgba(0,0,0,0.06);margin-bottom:22px;"><div style="font-size:14px;font-weight:800;color:#052e16;margin-bottom:14px;">📋 {tx["top3"]} — Detailed Breakdown</div>', unsafe_allow_html=True)
        disp=top3[["Rank","Name","Type","Dist_km","Revenue","Transport","Risk_pct","Net_Profit"]].copy()
        disp.columns=[tx["rank"],tx["dest"],tx["cat"],tx["dist_km"],tx["rev"],tx["trans"],tx["risk"],tx["net"]]
        disp[tx["rev"]]=disp[tx["rev"]].apply(lambda x:f"₹{int(x):,}")
        disp[tx["trans"]]=disp[tx["trans"]].apply(lambda x:f"₹{int(x):,}")
        disp[tx["net"]]=disp[tx["net"]].apply(lambda x:f"₹{int(x):,}")
        disp[tx["dist_km"]]=disp[tx["dist_km"]].apply(lambda x:f"{x:.1f} km")
        disp[tx["risk"]]=disp[tx["risk"]].apply(lambda x:f"{x:.2f}%")
        st.dataframe(disp,use_container_width=True,height=176,hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # MAP
        st.markdown(f'<div style="font-size:12px;font-weight:800;color:#052e16;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:10px;"><span style="display:inline-block;width:5px;height:22px;background:#16a34a;border-radius:3px;"></span>{tx["map_title"]}</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:white;border-radius:16px;padding:22px;border:1px solid #e5e7eb;box-shadow:0 4px 20px rgba(0,0,0,0.08);">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#6b7280;margin-bottom:14px;">🏠 Your farm &nbsp;&nbsp;★ Best market (gold solid route) &nbsp;&nbsp;Dots = other markets</div>', unsafe_allow_html=True)

        br=top3.iloc[0]
        m=folium.Map(location=[vlat,vlon],zoom_start=9,tiles="CartoDB Positron")
        folium.Marker([vlat,vlon],
            popup=folium.Popup(f"<b>{fname}</b><br>📍 {rv}",max_width=200),tooltip=tx["your_loc"],
            icon=folium.DivIcon(html='<div style="background:#052e16;border:3px solid #4ade80;border-radius:50%;width:42px;height:42px;display:flex;align-items:center;justify-content:center;font-size:19px;box-shadow:0 3px 14px rgba(0,0,0,0.5);">🏠</div>',icon_size=(42,42),icon_anchor=(21,21))
        ).add_to(m)

        rcols=["#f59e0b","#6b7280","#92400e"]
        for i,(_,row) in enumerate(top3.iterrows()):
            coords,_ = osm_route(vlat,vlon,row["Lat"],row["Lon"])
            folium.PolyLine(coords,color=rcols[i],weight=5 if i==0 else 3,opacity=0.95 if i==0 else 0.5,dash_array=None if i==0 else "8 5").add_to(m)
            if i==0:
                folium.Marker([row["Lat"],row["Lon"]],
                    popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br><span style='color:#16a34a;font-weight:700;font-size:14px'>₹{int(row['Net_Profit']):,}</span>",max_width=220),
                    tooltip=f"★ {row['Name']}",
                    icon=folium.DivIcon(html='<div style="background:#f59e0b;border:3px solid white;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:#1a1a1a;box-shadow:0 4px 18px rgba(245,158,11,0.7);">★</div>',icon_size=(44,44),icon_anchor=(22,22))
                ).add_to(m)
            else:
                folium.CircleMarker([row["Lat"],row["Lon"]],radius=12,color=rcols[i],fill=True,fill_color=rcols[i],fill_opacity=0.9,weight=3,
                    popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br>₹{int(row['Net_Profit']):,}",max_width=200),
                    tooltip=f"#{i+1} — {row['Name']}").add_to(m)

        st_folium(m,width=None,height=540,use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown(f"""
<div style="background:linear-gradient(135deg,#052e16,#15803d);padding:22px 32px;margin-top:28px;text-align:center;">
    <div style="font-size:16px;font-weight:800;color:white;margin-bottom:4px;">🥭 {tx['title']}</div>
    <div style="font-size:11px;color:rgba(74,222,128,0.4);letter-spacing:1px;">© 2025 · {tx['tagline']} · AP · Telangana · Karnataka</div>
</div>""", unsafe_allow_html=True)
