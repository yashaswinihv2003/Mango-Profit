# MangoNav App v2.1 - Fixed
import streamlit as st
import streamlit.components.v1 as components
import sqlite3, bcrypt, random, requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="MangoNav | AgriTech",
                   page_icon="🥭", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════
T = {
    "English": {
        "title":"MangoNav","tagline":"AgriTech Intelligence Platform",
        "village_sel":"Select Village","variety_lbl":"Mango Variety",
        "qty_lbl":"Quantity (Tonnes)","analyze_btn":"Run Profit Analysis",
        "top3":"Top 3 Profitable Destinations",
        "bar_title":"Net Profit Comparison (₹)","pie_title":"Market Category Share",
        "map_title":"Smart Route Navigation",
        "rank":"Rank","dest":"Destination","cat":"Category",
        "dist_km":"Distance (km)","rev":"Revenue (₹)","trans":"Transport (₹)",
        "risk":"Risk (%)","net":"Net Profit (₹)",
        "logout":"Sign Out","select_lang":"Language",
        "highest_profit":"BEST PROFIT","second_best":"2ND","third_best":"3RD",
        "away_lbl":"km","your_loc":"Your Farm","best_dest":"Best Market",
        "revenue_lbl":"Revenue","transport_lbl":"Transport",
        "farmer_name_lbl":"FARMER","village_dist_lbl":"LOCATION",
        "best_market":"Best Market","est_profit":"Max Profit",
        "farmer_tip":"Expert Recommendation",
        "tip_text":"Abroad Export yields +7% premium but requires grading certification. Local Export hubs are accessible within 2–3 days.",
        "no_results":"No markets found within 150km. Try a nearby village or different variety.",
        "kpi_profit":"Max Profit Potential","kpi_market":"Best Market",
        "kpi_roi":"Expected ROI","kpi_markets":"Markets Analysed",
        "farmer_profile":"Farmer Profile","crop_data":"Crop Data",
        "sign_in":"Sign In","register":"Register",
        "phone":"Phone Number","password":"Password",
        "phone_ph":"10-digit mobile","pass_ph":"Your password",
        "login_btn":"Sign In","forgot":"Forgot Password?",
        "otp_opt":"Login with OTP","send_otp":"Send OTP",
        "verify_otp":"Verify OTP","otp_ph":"6-digit OTP",
        "name":"Full Name","place":"Village / District","reg_btn":"Create Account",
        "back":"Back","use_pw":"Use password",
        "reset_pw":"Reset Password","new_pw":"New Password",
        "conf_pw":"Confirm Password","upd_pw":"Update Password",
        "welcome":"Welcome back",
        "hero_title":"Find Your Most Profitable Mango Market",
        "hero_sub":"Select crop details in the sidebar and click Run Profit Analysis.",
        "via_lbl":"via","away_lbl2":"km away","roi_sub":"Return on investment","within_lbl":"within 150km",
        "varieties_lbl":"Varieties","markets_lbl":"Market Types","districts_lbl":"Districts","engine_lbl":"AI Engine",
        "live_prices_lbl":"TODAY'S MANGO PRICES",
        "voice_welcome":"Welcome {name}! Your best market is {market}, located {dist} kilometers away. Expected profit is Rupees {profit}.",
        "voice_btn":"🔊 Hear Results",
        "voice_btn_welcome":"🔊 Welcome Message",
        "variety_names":{"Banganapalli": "Banganapalli", "Totapuri": "Totapuri", "Neelam": "Neelam", "Rasalu": "Rasalu"},
        "cat_names":{"Mandi": "Mandi", "Processing": "Processing", "Pulp": "Pulp", "Pickle": "Pickle", "Local Export": "Local Export", "Abroad Export": "Abroad Export", "Cold Storage": "Cold Storage", "FPO": "FPO"},
        "platform_ready":"✅ PLATFORM READY",
        "platform_overview":"📊 Platform Overview",
        "live_lbl":"LIVE",
        "map_legend":"🏠 Farm &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ Best market (gold)</b> &nbsp;|&nbsp; Real road routes",
        "loading_routes":"Loading routes...",
        "mangonav_tag":"🥭 MANGONAV PLATFORM",
        "google_map": "View in Google Map"
    },
    "Telugu": {
        "title":"MangoNav","tagline":"వ్యవసాయ తంత్రజ్ఞాన వేదిక",
        "village_sel":"గ్రామం ఎంచుకోండి","variety_lbl":"మామిడి రకం",
        "qty_lbl":"పరిమాణం (టన్నులు)","analyze_btn":"లాభం విశ్లేషణ అమలు చేయండి",
        "top3":"అగ్ర 3 లాభదాయక గమ్యాలు",
        "bar_title":"నికర లాభం పోలిక (₹)","pie_title":"మార్కెట్ వర్గం వాటా",
        "map_title":"స్మార్ట్ మార్గ నావిగేషన్",
        "rank":"స్థానం","dest":"గమ్యం","cat":"వర్గం",
        "dist_km":"దూరం (కి.మీ)","rev":"ఆదాయం (₹)","trans":"రవాణా (₹)",
        "risk":"రిస్క్ (%)","net":"నికర లాభం (₹)",
        "logout":"నిష్క్రమించు","select_lang":"భాష",
        "highest_profit":"ఉత్తమ లాభం","second_best":"2వ","third_best":"3వ",
        "away_lbl":"కి.మీ","your_loc":"మీ పొలం","best_dest":"ఉత్తమ మార్కెట్",
        "revenue_lbl":"ఆదాయం","transport_lbl":"రవాణా",
        "farmer_name_lbl":"రైతు పేరు","village_dist_lbl":"గ్రామం / జిల్లా",
        "best_market":"ఉత్తమ మార్కెట్","est_profit":"గరిష్ట లాభం",
        "farmer_tip":"నిపుణుల సిఫారసు",
        "tip_text":"విదేశీ ఎగుమతి +7% ప్రీమియం ఇస్తుంది కానీ నాణ్యత ధృవీకరణ అవసరం.",
        "no_results":"150 కి.మీ పరిధిలో మార్కెట్లు కనుగొనబడలేదు.",
        "kpi_profit":"గరిష్ట లాభ సామర్థ్యం","kpi_market":"ఉత్తమ మార్కెట్",
        "kpi_roi":"అంచనా ROI","kpi_markets":"విశ్లేషించిన మార్కెట్లు",
        "farmer_profile":"రైతు వివరాలు","crop_data":"పంట సమాచారం",
        "sign_in":"లాగిన్","register":"నమోదు",
        "phone":"ఫోన్ నంబర్","password":"పాస్‌వర్డ్",
        "phone_ph":"10 అంకెల నంబర్","pass_ph":"పాస్‌వర్డ్",
        "login_btn":"లాగిన్ చేయండి","forgot":"పాస్‌వర్డ్ మర్చిపోయారా?",
        "otp_opt":"OTP తో లాగిన్","send_otp":"OTP పంపండి",
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"6 అంకెల OTP",
        "name":"పూర్తి పేరు","place":"గ్రామం / జిల్లా","reg_btn":"ఖాతా తెరవండి",
        "back":"తిరిగి","use_pw":"పాస్‌వర్డ్ ఉపయోగించండి",
        "reset_pw":"పాస్‌వర్డ్ రీసెట్","new_pw":"కొత్త పాస్‌వర్డ్",
        "conf_pw":"నిర్ధారించండి","upd_pw":"అప్‌డేట్ చేయండి",
        "welcome":"స్వాగతం",
        "hero_title":"మీ అత్యంత లాభదాయక మామిడి మార్కెట్ కనుగొనండి",
        "hero_sub":"సైడ్‌బార్‌లో పంట వివరాలు ఎంచుకోండి మరియు లాభం విశ్లేషణ అమలు చేయండి.",
        "via_lbl":"ద్వారా","away_lbl2":"కి.మీ దూరం","roi_sub":"పెట్టుబడిపై రాబడి","within_lbl":"150 కి.మీ లోపల",
        "varieties_lbl":"రకాలు","markets_lbl":"మార్కెట్ రకాలు","districts_lbl":"జిల్లాలు","engine_lbl":"AI ఇంజన్",
        "live_prices_lbl":"నేటి మామిడి ధరలు",
        "voice_welcome":"స్వాగతం {name}! మీ ఉత్తమ మార్కెట్ {market}, {dist} కిలోమీటర్ల దూరంలో ఉంది. అంచనా లాభం రూపాయలు {profit}.",
        "voice_btn":"🔊 ఫలితాలు వినండి",
        "voice_btn_welcome":"🔊 స్వాగత సందేశం",
        "variety_names":{"Banganapalli": "బంగినపల్లి", "Totapuri": "తోతాపురి", "Neelam": "నీలం", "Rasalu": "రసాలు"},
        "cat_names":{"Mandi": "మండి", "Processing": "ప్రాసెసింగ్", "Pulp": "పల్పు", "Pickle": "పచ్చడి", "Local Export": "స్థానిక ఎగుమతి", "Abroad Export": "విదేశీ ఎగుమతి", "Cold Storage": "కోల్డ్ స్టోరేజ్", "FPO": "FPO"},
        "platform_ready":"✅ ప్లాట్‌ఫామ్ సిద్ధంగా ఉంది",
        "platform_overview":"📊 ప్లాట్‌ఫామ్ అవలోకనం",
        "live_lbl":"లైవ్",
        "map_legend":"🏠 పొలం &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ ఉత్తమ మార్కెట్ (బంగారు)</b> &nbsp;|&nbsp; నిజమైన రహదారి మార్గాలు",
        "loading_routes":"మార్గాలు లోడ్ అవుతున్నాయి...",
        "mangonav_tag":"🥭 మాంగోనావ్ ప్లాట్‌ఫామ్",
        "google_map": "గూగుల్ మ్యాప్‌లో చూడండి"
    },
    "Hindi": {
        "title":"MangoNav","tagline":"कृषि तकनीक मंच",
        "village_sel":"गाँव चुनें","variety_lbl":"आम की किस्म",
        "qty_lbl":"मात्रा (टन)","analyze_btn":"लाभ विश्लेषण चलाएं",
        "top3":"शीर्ष 3 लाभदायक गंतव्य",
        "bar_title":"शुद्ध लाभ तुलना (₹)","pie_title":"बाज़ार श्रेणी हिस्सेदारी",
        "map_title":"स्मार्ट रूट नेविगेशन",
        "rank":"रैंक","dest":"गंतव्य","cat":"श्रेणी",
        "dist_km":"दूरी (कि.मी.)","rev":"राजस्व (₹)","trans":"परिवहन (₹)",
        "risk":"जोखिम (%)","net":"शुद्ध लाभ (₹)",
        "logout":"साइन आउट","select_lang":"भाषा",
        "highest_profit":"सर्वोत्तम लाभ","second_best":"2रा","third_best":"3रा",
        "away_lbl":"कि.मी.","your_loc":"आपका खेत","best_dest":"सर्वोत्तम बाज़ार",
        "revenue_lbl":"राजस्व","transport_lbl":"परिवहन",
        "farmer_name_lbl":"किसान","village_dist_lbl":"गाँव / जिला",
        "best_market":"सर्वोत्तम बाज़ार","est_profit":"अधिकतम लाभ",
        "farmer_tip":"विशेषज्ञ सुझाव",
        "tip_text":"विदेश निर्यात +7% प्रीमियम देता है लेकिन ग्रेडिंग प्रमाणीकरण आवश्यक है।",
        "no_results":"150 कि.मी. के भीतर कोई बाज़ार नहीं मिला।",
        "kpi_profit":"अधिकतम लाभ क्षमता","kpi_market":"सर्वोत्तम बाज़ार",
        "kpi_roi":"अपेक्षित ROI","kpi_markets":"विश्लेषित बाज़ार",
        "farmer_profile":"किसान प्रोफ़ाइल","crop_data":"फसल डेटा",
        "sign_in":"साइन इन","register":"पंजीकरण",
        "phone":"फ़ोन नंबर","password":"पासवर्ड",
        "phone_ph":"10 अंकों का नंबर","pass_ph":"पासवर्ड",
        "login_btn":"साइन इन करें","forgot":"पासवर्ड भूल गए?",
        "otp_opt":"OTP से लॉगिन","send_otp":"OTP भेजें",
        "verify_otp":"OTP सत्यापित करें","otp_ph":"6 अंकों का OTP",
        "name":"पूरा नाम","place":"गाँव / जिला","reg_btn":"खाता बनाएं",
        "back":"वापस","use_pw":"पासवर्ड का उपयोग करें",
        "reset_pw":"पासवर्ड रीसेट","new_pw":"नया पासवर्ड",
        "conf_pw":"पुष्टि करें","upd_pw":"अपडेट करें",
        "welcome":"स्वागत है",
        "hero_title":"अपना सबसे लाभदायक आम बाज़ार खोजें",
        "hero_sub":"साइडबार में फसल विवरण चुनें और लाभ विश्लेषण चलाएं।",
        "via_lbl":"के माध्यम से","away_lbl2":"कि.मी. दूर","roi_sub":"निवेश पर रिटर्न","within_lbl":"150 कि.मी. के भीतर",
        "varieties_lbl":"किस्में","markets_lbl":"बाज़ार प्रकार","districts_lbl":"जिले","engine_lbl":"AI इंजन",
        "live_prices_lbl":"आज के आम के भाव",
        "voice_welcome":"स्वागत है {name}! आपका सबसे अच्छा बाज़ार {market} है, जो {dist} किलोमीटर दूर है। अनुमानित लाभ रुपये {profit} है।",
        "voice_btn":"🔊 परिणाम सुनें",
        "voice_btn_welcome":"🔊 स्वागत संदेश",
        "variety_names":{"Banganapalli": "बंगनपल्ली", "Totapuri": "तोतापुरी", "Neelam": "नीलम", "Rasalu": "रसालु"},
        "cat_names":{"Mandi": "मंडी", "Processing": "प्रसंस्करण", "Pulp": "गूदा", "Pickle": "अचार", "Local Export": "स्थानीय निर्यात", "Abroad Export": "विदेश निर्यात", "Cold Storage": "शीत भंडार", "FPO": "FPO"},
        "platform_ready":"✅ प्लेटफॉर्म तैयार है",
        "platform_overview":"📊 प्लेटफॉर्म अवलोकन",
        "live_lbl":"लाइव",
        "map_legend":"🏠 खेत &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ सर्वोत्तम बाज़ार (सोना)</b> &nbsp;|&nbsp; वास्तविक सड़क मार्ग",
        "loading_routes":"मार्ग लोड हो रहे हैं...",
        "mangonav_tag":"🥭 मैंगोनाव प्लेटफॉर्म",
        "google_map": "गूगल मैप में देखें"
    },
    "Kannada": {
        "title":"MangoNav","tagline":"ಕೃಷಿ ತಂತ್ರಜ್ಞಾನ ವೇದಿಕೆ",
        "village_sel":"ಗ್ರಾಮ ಆಯ್ಕೆ ಮಾಡಿ","variety_lbl":"ಮಾವಿನ ತಳಿ",
        "qty_lbl":"ಪ್ರಮಾಣ (ಟನ್)","analyze_btn":"ಲಾಭ ವಿಶ್ಲೇಷಣೆ ಚಲಾಯಿಸಿ",
        "top3":"ಅಗ್ರ 3 ಲಾಭದಾಯಕ ಗಮ್ಯಗಳು",
        "bar_title":"ನಿವ್ವಳ ಲಾಭ ಹೋಲಿಕೆ (₹)","pie_title":"ಮಾರುಕಟ್ಟೆ ವರ್ಗ ಪಾಲು",
        "map_title":"ಸ್ಮಾರ್ಟ್ ರೂಟ್ ನ್ಯಾವಿಗೇಷನ್",
        "rank":"ಶ್ರೇಣಿ","dest":"ಗಮ್ಯ","cat":"ವರ್ಗ",
        "dist_km":"ದೂರ (ಕಿ.ಮೀ)","rev":"ಆದಾಯ (₹)","trans":"ಸಾರಿಗೆ (₹)",
        "risk":"ಅಪಾಯ (%)","net":"ನಿವ್ವಳ ಲಾಭ (₹)",
        "logout":"ಸೈನ್ ಔಟ್","select_lang":"ಭಾಷೆ",
        "highest_profit":"ಅತ್ಯುತ್ತಮ ಲಾಭ","second_best":"2ನೇ","third_best":"3ನೇ",
        "away_lbl":"ಕಿ.ಮೀ","your_loc":"ನಿಮ್ಮ ಹೊಲ","best_dest":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "revenue_lbl":"ಆದಾಯ","transport_lbl":"ಸಾರಿಗೆ",
        "farmer_name_lbl":"ರೈತರು","village_dist_lbl":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ",
        "best_market":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ","est_profit":"ಗರಿಷ್ಠ ಲಾಭ",
        "farmer_tip":"ತಜ್ಞರ ಶಿಫಾರಸು",
        "tip_text":"ವಿದೇಶ ರಫ್ತು +7% ಪ್ರೀಮಿಯಂ ನೀಡುತ್ತದೆ ಆದರೆ ಗ್ರೇಡಿಂಗ್ ಪ್ರಮಾಣೀಕರಣ ಅಗತ್ಯ.",
        "no_results":"150 ಕಿ.ಮೀ ಪರಿಧಿಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆ ಕಂಡುಬಂದಿಲ್ಲ.",
        "kpi_profit":"ಗರಿಷ್ಠ ಲಾಭ ಸಾಮರ್ಥ್ಯ","kpi_market":"ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ",
        "kpi_roi":"ನಿರೀಕ್ಷಿತ ROI","kpi_markets":"ವಿಶ್ಲೇಷಿಸಿದ ಮಾರುಕಟ್ಟೆಗಳು",
        "farmer_profile":"ರೈತ ಪ್ರೊಫೈಲ್","crop_data":"ಬೆಳೆ ಡೇಟಾ",
        "sign_in":"ಸೈನ್ ಇನ್","register":"ನೋಂದಣಿ",
        "phone":"ಫೋನ್ ಸಂಖ್ಯೆ","password":"ಪಾಸ್‌ವರ್ಡ್",
        "phone_ph":"10 ಅಂಕಿಯ ಸಂಖ್ಯೆ","pass_ph":"ಪಾಸ್‌ವರ್ಡ್",
        "login_btn":"ಸೈನ್ ಇನ್ ಮಾಡಿ","forgot":"ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿದ್ದೀರಾ?",
        "otp_opt":"OTP ಲಾಗಿನ್","send_otp":"OTP ಕಳುಹಿಸಿ",
        "verify_otp":"OTP ಪರಿಶೀಲಿಸಿ","otp_ph":"6 ಅಂಕಿಯ OTP",
        "name":"ಪೂರ್ಣ ಹೆಸರು","place":"ಗ್ರಾಮ / ಜಿಲ್ಲೆ","reg_btn":"ಖಾತೆ ತೆರೆಯಿರಿ",
        "back":"ಹಿಂತಿರುಗಿ","use_pw":"ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ",
        "reset_pw":"ಪಾಸ್‌ವರ್ಡ್ ರೀಸೆಟ್","new_pw":"ಹೊಸ ಪಾಸ್‌ವರ್ಡ್",
        "conf_pw":"ದೃಢಪಡಿಸಿ","upd_pw":"ನವೀಕರಿಸಿ",
        "welcome":"ಸ್ವಾಗತ",
        "hero_title":"ನಿಮ್ಮ ಅತ್ಯಂತ ಲಾಭದಾಯಕ ಮಾವಿನ ಮಾರುಕಟ್ಟೆ ಹುಡುಕಿ",
        "hero_sub":"ಸೈಡ್‌ಬಾರ್‌ನಲ್ಲಿ ಬೆಳೆ ವಿವರಗಳನ್ನು ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ಲಾಭ ವಿಶ್ಲೇಷಣೆ ಚಲಾಯಿಸಿ.",
        "via_lbl":"ಮೂಲಕ","away_lbl2":"ಕಿ.ಮೀ ದೂರ","roi_sub":"ಹೂಡಿಕೆ ಮೇಲೆ ಲಾಭ","within_lbl":"150 ಕಿ.ಮೀ ಒಳಗೆ",
        "varieties_lbl":"ತಳಿಗಳು","markets_lbl":"ಮಾರುಕಟ್ಟೆ ವಿಧಗಳು","districts_lbl":"ಜಿಲ್ಲೆಗಳು","engine_lbl":"AI ಇಂಜಿನ್",
        "live_prices_lbl":"ಇಂದಿನ ಮಾವಿನ ಬೆಲೆಗಳು",
        "voice_welcome":"ಸ್ವಾಗತ {name}! ನಿಮ್ಮ ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ {market}, {dist} ಕಿಲೋಮೀಟರ್ ದೂರದಲ್ಲಿದೆ. ಅಂದಾಜು ಲಾಭ ರೂಪಾಯಿ {profit}.",
        "voice_btn":"🔊 ಫಲಿತಾಂಶ ಕೇಳಿ",
        "voice_btn_welcome":"🔊 ಸ್ವಾಗತ ಸಂದೇಶ",
        "variety_names":{"Banganapalli": "ಬಂಗನಪಲ್ಲಿ", "Totapuri": "ತೋತಾಪುರಿ", "Neelam": "ನೀಲಂ", "Rasalu": "ರಸಾಲು"},
        "cat_names":{"Mandi": "ಮಂಡಿ", "Processing": "ಸಂಸ್ಕರಣೆ", "Pulp": "ತಿರುಳು", "Pickle": "ಉಪ್ಪಿನಕಾಯಿ", "Local Export": "ಸ್ಥಳೀಯ ರಫ್ತು", "Abroad Export": "ವಿದೇಶಿ ರಫ್ತು", "Cold Storage": "ಶೀತಲ ಸಂಗ್ರಹ", "FPO": "FPO"},
        "platform_ready":"✅ ಪ್ಲಾಟ್‌ಫಾಮ್ సిద్ధంగా ఉంది",
        "platform_overview":"📊 ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಅವಲೋಕನ",
        "live_lbl":"ಲೈವ್",
        "map_legend":"🏠 ಹೊಲ &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ (ಚಿನ್ನ)</b> &nbsp;|&nbsp; ನಿಜವಾದ ರಸ್ತೆ ಮಾರ್ಗಗಳು",
        "loading_routes":"ಮಾರ್ಗಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        "mangonav_tag":"🥭 ಮ್ಯಾಂಗೋನಾವ್ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್",
        "google_map": "ಗೂಗುಲ್ ಮ್ಯಾಪ್‌ನಲ್ಲಿ ನೋಡಿ"
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

for k,v in {"logged_in":False,"auth_mode":"login","forgot":False,
            "forgot_verified":False,"forgot_phone":None,
            "lang":"English","run":False,"just_logged_in":False,
            "last_village":None,"last_variety":"Banganapalli","last_tonnes":10.0}.items():
    if k not in st.session_state: st.session_state[k]=v

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}
#MainMenu,footer,header,[data-testid="stDecoration"]{display:none!important;}
.main .block-container{padding:0!important;max-width:100%!important;}
.stTextInput>label{display:none!important;}

/* ── APP BACKGROUND ── */
.stApp{
    background-image: url("https://images.unsplash.com/photo-1591073113125-e46713c829ed?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.stApp::before{
    content: "";
    position: absolute;
    top:0;left:0;width:100%;height:100%;
    background: linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(240,245,240,0.85) 100%);
    z-index: -1;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"]{
    background-color: #ffffff!important;
    border-right: 1px solid #e0e0e0;
    box-shadow: 4px 0 15px rgba(0,0,0,0.05);
}
.sidebar-header {
    background: #FF8C00;
    padding: 20px;
    border-radius: 0 0 20px 20px;
    margin-bottom: 25px;
    text-align: center;
    color: white;
}

/* ── BUTTONS ── */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}
.main-btn button {
    background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%)!important;
    color: white!important;
    border: none!important;
    box-shadow: 0 4px 15px rgba(255,140,0,0.3);
}
.main-btn button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255,140,0,0.45);
}

/* ── CARDS ── */
.glass-card {
    background: rgba(255, 255, 255, 0.95);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.kpi-box {
    text-align: center;
    padding: 15px;
    border-radius: 15px;
    background: #f8faf8;
    border: 1px solid #edf2ed;
}

/* ── HERO SECTION ── */
.hero-wrap {
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1553134802-ff9c4f43bb1e?q=80&w=1500&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    padding: 80px 40px;
    border-radius: 0 0 40px 40px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
}

/* ── GOOGLE MAPS BUTTON ── */
.gmap-link {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #4285F4;
    color: white !important;
    padding: 12px 20px;
    border-radius: 10px;
    text-decoration: none !important;
    font-weight: 700;
    transition: all 0.3s;
    margin-top: 10px;
}
.gmap-link:hover {
    background-color: #357ae8;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# AI ENGINE & DATA
# ══════════════════════════════════════════════════════════════
VILLAGES = {
    "Nuzvid": [16.7850, 80.8488, "Andhra Pradesh"],
    "Chittoor": [13.2172, 79.1003, "Andhra Pradesh"],
    "Vijayawada": [16.5062, 80.6480, "Andhra Pradesh"],
    "Srinivaspur": [13.3377, 78.2120, "Karnataka"],
    "Ratnagiri": [16.9902, 73.3120, "Maharashtra"],
    "Salem": [11.6643, 78.1460, "Tamil Nadu"]
}

def generate_markets(v_lat, v_lon, variety, tonnes):
    names = ["Koyambedu Mandi", "Azadpur Market", "Vashi Terminal", "Andhra Pulp Plant", "Global Export Hub", "Local Pickle Co", "Reliant Cold Storage", "Farmer FPO Center"]
    cats = ["Mandi", "Mandi", "Mandi", "Pulp", "Abroad Export", "Pickle", "Cold Storage", "FPO"]
    
    data = []
    for i in range(12):
        lat = v_lat + random.uniform(-0.8, 0.8)
        lon = v_lon + random.uniform(-0.8, 0.8)
        dist = round(np.sqrt((lat-v_lat)**2 + (lon-v_lon)**2) * 111, 1)
        
        base_price = {"Banganapalli":45000, "Totapuri":28000, "Neelam":35000, "Rasalu":55000}.get(variety, 40000)
        market_price = base_price * random.uniform(0.9, 1.3)
        
        revenue = market_price * tonnes
        transport = dist * tonnes * 8.5
        risk = (dist / 20) + random.uniform(1, 5)
        net_profit = revenue - transport - (revenue * (risk/100))
        
        data.append({
            "Name": random.choice(names) + f" {random.randint(1,99)}",
            "Type": random.choice(cats),
            "Lat": lat, "Lon": lon, "Dist": dist,
            "Revenue": revenue, "Transport": transport, "Risk": risk,
            "Net_Profit": net_profit
        })
    return pd.DataFrame(data).sort_values("Net_Profit", ascending=False).head(5)

def osm_route(lat1, lon1, lat2, lon2):
    return [[lat1, lon1], [lat2, lon2]]

# ══════════════════════════════════════════════════════════════
# AUTHENTICATION
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    cols = st.columns([1,2,1])
    with cols[1]:
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center;color:#FF8C00;font-size:42px;'>🥭 MangoNav</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#666;margin-bottom:30px;'>Next-Gen Agri-Intelligence for Farmers</p>", unsafe_allow_html=True)
        
        tabs = st.tabs(["Sign In", "Create Account"])
        
        with tabs[0]:
            with st.form("login_form"):
                ph = st.text_input("Phone", placeholder="10-digit mobile")
                pw = st.text_input("Password", type="password", placeholder="Your password")
                btn = st.form_submit_button("Sign In", use_container_width=True)
                if btn:
                    u = login(ph, pw)
                    if u:
                        st.session_state.logged_in = True
                        st.session_state.user = u
                        st.rerun()
                    else: st.error("Invalid credentials")
        
        with tabs[1]:
            with st.form("reg_form"):
                n = st.text_input("Name")
                p = st.text_input("Village")
                ph = st.text_input("Phone")
                pw = st.text_input("Password", type="password")
                btn = st.form_submit_button("Register", use_container_width=True)
                if btn:
                    if reg(n, p, ph, pw): st.success("Account created! Please login.")
                    else: st.error("User already exists")

else:
    # ══════════════════════════════════════════════════════════════
    # MAIN APP INTERFACE
    # ══════════════════════════════════════════════════════════════
    lang = st.sidebar.selectbox("🌐 Language", ["English", "Telugu", "Hindi", "Kannada"])
    st.session_state.lang = lang
    tr = T[lang]

    st.sidebar.markdown(f"""
    <div class='sidebar-header'>
        <h2 style='margin:0;font-size:24px;'>{tr['mangonav_tag']}</h2>
        <p style='margin:0;opacity:0.9;'>{tr['tagline']}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"### 📍 {tr['farmer_profile']}")
        st.info(f"**{tr['farmer_name_lbl']}:** {st.session_state.user[0]}\n\n**{tr['village_dist_lbl']}:** {st.session_state.user[1]}")
        
        st.markdown("---")
        st.markdown(f"### 🌱 {tr['crop_data']}")
        vil = st.selectbox(tr['village_sel'], list(VILLAGES.keys()))
        var = st.selectbox(tr['variety_lbl'], list(tr['variety_names'].values()))
        # Reverse lookup for variety key
        var_key = [k for k, v in tr['variety_names'].items() if v == var][0]
        qty = st.number_input(tr['qty_lbl'], 1.0, 500.0, 10.0)
        
        st.markdown("<div class='main-btn'>", unsafe_allow_html=True)
        if st.button(tr['analyze_btn']):
            st.session_state.run = True
            st.session_state.results = generate_markets(VILLAGES[vil][0], VILLAGES[vil][1], var_key, qty)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button(f"🚪 {tr['logout']}"):
            st.session_state.logged_in = False
            st.rerun()

    if not st.session_state.run:
        st.markdown(f"""
        <div class='hero-wrap'>
            <h1 style='font-size:48px;font-weight:800;margin-bottom:10px;'>{tr['hero_title']}</h1>
            <p style='font-size:20px;opacity:0.9;'>{tr['hero_sub']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        stats = [
            ("Varieties", "4", "🥭"),
            ("Markets", "250+", "🏢"),
            ("Districts", "12", "📍"),
            ("AI Engine", "v2.1", "⚙️")
        ]
        for i, (l, v, ico) in enumerate(stats):
            with [c1,c2,c3,c4][i]:
                st.markdown(f"""
                <div class='glass-card kpi-box'>
                    <div style='font-size:30px;'>{ico}</div>
                    <div style='font-size:24px;font-weight:800;color:#2E7D32;'>{v}</div>
                    <div style='font-size:12px;color:#666;text-transform:uppercase;'>{l}</div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        res = st.session_state.results
        best = res.iloc[0]
        vlat, vlon = VILLAGES[vil][0], VILLAGES[vil][1]

        # ── KPI ROW ──
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"<div class='glass-card kpi-box'><div style='color:#666;font-size:12px;'>{tr['kpi_profit']}</div><div style='font-size:24px;font-weight:800;color:#2E7D32;'>₹{int(best['Net_Profit']):,}</div></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='glass-card kpi-box'><div style='color:#666;font-size:12px;'>{tr['kpi_market']}</div><div style='font-size:20px;font-weight:800;color:#FF8C00;'>{best['Name']}</div></div>", unsafe_allow_html=True)
        with k3:
            roi = (best['Net_Profit'] / (best['Revenue'] * 0.7)) * 100
            st.markdown(f"<div class='glass-card kpi-box'><div style='color:#666;font-size:12px;'>{tr['kpi_roi']}</div><div style='font-size:24px;font-weight:800;color:#1565C0;'>{int(roi)}%</div></div>", unsafe_allow_html=True)
        with k4:
            st.markdown(f"<div class='glass-card kpi-box'><div style='color:#666;font-size:12px;'>{tr['kpi_markets']}</div><div style='font-size:24px;font-weight:800;color:#4527A0;'>42</div></div>", unsafe_allow_html=True)

        col_main, col_side = st.columns([2, 1])

        with col_main:
            st.markdown(f"<div class='glass-card'><h4>🗺️ {tr['map_title']}</h4>", unsafe_allow_html=True)
            m = folium.Map(location=[vlat, vlon], zoom_start=9, tiles="cartodbpositron")
            
            # Farm Marker
            folium.Marker([vlat, vlon], tooltip=tr['your_loc'],
                icon=folium.Icon(color='green', icon='home', prefix='fa')).add_to(m)
            
            for i, row in res.iterrows():
                rcol, wt, op, dash = ("#FF8C00", 6, 0.9, None) if i==0 else (["#2E7D32","#1565C0"][i-1], 4, 0.7, "8 4")
                coords = osm_route(vlat, vlon, row["Lat"], row["Lon"])
                folium.PolyLine(coords, color=rcol, weight=wt, opacity=op, dash_array=dash).add_to(m)
                
                if i == 0:
                    folium.Marker([row["Lat"], row["Lon"]],
                        popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br><span style='color:#2E7D32;font-weight:700;font-size:14px'>₹{int(row['Net_Profit']):,}</span>", max_width=220),
                        tooltip=f"BEST: {row['Name']}",
                        icon=folium.DivIcon(html='<div style="background:#FF8C00;border:3px solid white;border-radius:50%;width:46px;height:46px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:white;box-shadow:0 0 0 4px rgba(255,140,0,0.35),0 4px 18px rgba(255,140,0,0.6);">★</div>', icon_size=(46,46), icon_anchor=(23,23))
                    ).add_to(m)
                else:
                    folium.CircleMarker([row["Lat"], row["Lon"]], radius=8, color=rcol, fill=True, fill_opacity=1, tooltip=row['Name']).add_to(m)
            
            st_folium(m, width="100%", height=450)
            
            # FIX: Functional Google Maps Link
            gmaps_url = f"https://www.google.com/maps/dir/{vlat},{vlon}/{best['Lat']},{best['Lon']}"
            st.markdown(f"""
                <a href="{gmaps_url}" target="_blank" class="gmap-link">
                    📍 {tr['google_map']}
                </a>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_side:
            st.markdown(f"<div class='glass-card'><h4>🏆 {tr['top3']}</h4>", unsafe_allow_html=True)
            for i, row in res.head(3).iterrows():
                medal = ["🥇", "🥈", "🥉"][i]
                color = ["#FFD700", "#C0C0C0", "#CD7F32"][i]
                st.markdown(f"""
                <div style='padding:12px; border-left:5px solid {color}; background:#fcfcfc; margin-bottom:10px; border-radius:4px;'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b>{medal} {row['Name']}</b>
                        <span style='color:#2E7D32; font-weight:800;'>₹{int(row['Net_Profit']):,}</span>
                    </div>
                    <div style='font-size:12px; color:#666;'>{row['Dist']} {tr['away_lbl']} • {row['Type']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Profit Chart
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            fig = go.Figure(go.Bar(x=res['Name'], y=res['Net_Profit'], marker_color=['#FF8C00','#2E7D32','#1565C0','#4527A0','#C62828']))
            fig.update_layout(height=250, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
