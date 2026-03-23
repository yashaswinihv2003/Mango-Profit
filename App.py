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
        "view_gmaps": "View in Google Map",
        "variety_names":{"Banganapalli": "Banganapalli", "Totapuri": "Totapuri", "Neelam": "Neelam", "Rasalu": "Rasalu"},
        "cat_names":{"Mandi": "Mandi", "Processing": "Processing", "Pulp": "Pulp", "Pickle": "Pickle", "Local Export": "Local Export", "Abroad Export": "Abroad Export", "Cold Storage": "Cold Storage", "FPO": "FPO"},
        "platform_ready":"✅ PLATFORM READY",
        "platform_overview":"📊 Platform Overview",
        "live_lbl":"LIVE",
        "map_legend":"🏠 Farm &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ Best market (gold)</b> &nbsp;|&nbsp; Real road routes",
        "loading_routes":"Loading routes...",
        "mangonav_tag":"🥭 MANGONAV PLATFORM",
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
        "verify_otp":"OTP ధృవీకరించండి","otp_ph":"గణాంక OTP",
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
        "view_gmaps": "గూగుల్ మ్యాప్ లో చూడండి",
        "variety_names":{"Banganapalli": "బంగినపల్లి", "Totapuri": "తోతాపురి", "Neelam": "నీలం", "Rasalu": "రసాలు"},
        "cat_names":{"Mandi": "మండి", "Processing": "ప్రాసెసింగ్", "Pulp": "పల్పు", "Pickle": "పచ్చడి", "Local Export": "స్థానిక ఎగుమతి", "Abroad Export": "విదేశీ ఎగుమతి", "Cold Storage": "కోల్డ్ స్టోరేజ్", "FPO": "FPO"},
        "platform_ready":"✅ ప్లాట్‌ఫామ్ సిద్ధంగా ఉంది",
        "platform_overview":"📊 ప్లాట్‌ఫామ్ అవలోకనం",
        "live_lbl":"లైవ్",
        "map_legend":"🏠 పొలం &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ ఉత్తమ మార్కెట్ (బంగారు)</b> &nbsp;|&nbsp; నిజమైన రహదారి మార్గాలు",
        "loading_routes":"మార్గాలు లోడ్ అవుతున్నాయి...",
        "mangonav_tag":"🥭 మాంగోనావ్ ప్లాట్‌ఫామ్",
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
        "view_gmaps": "गूगल मैप में देखें",
        "variety_names":{"Banganapalli": "बंगनपल्ली", "Totapuri": "तोतापुरी", "Neelam": "नीलम", "Rasalu": "रसालु"},
        "cat_names":{"Mandi": "मंडी", "Processing": "प्रसंस्करण", "Pulp": "गूदा", "Pickle": "अचार", "Local Export": "स्थानीय निर्यात", "Abroad Export": "विदेश निर्यात", "Cold Storage": "शीत भंडार", "FPO": "FPO"},
        "platform_ready":"✅ प्लेटफॉर्म तैयार है",
        "platform_overview":"📊 प्लेटफॉर्म अवलोकन",
        "live_lbl":"लाइव",
        "map_legend":"🏠 खेत &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ सर्वोत्तम बाज़ार (सोना)</b> &nbsp;|&nbsp; वास्तविक सड़क मार्ग",
        "loading_routes":"मार्ग लोड हो रहे हैं...",
        "mangonav_tag":"🥭 मैंगोनाव प्लेटफॉर्म",
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
        "view_gmaps": "ಗೂಗುಲ್ ಮ್ಯಾಪ್ ನಲ್ಲಿ ನೋಡಿ",
        "variety_names":{"Banganapalli": "ಬಂಗನಪಲ್ಲಿ", "Totapuri": "ತೋತಾಪುರಿ", "Neelam": "ನೀಲಂ", "Rasalu": "ರಸಾಲು"},
        "cat_names":{"Mandi": "ಮಂಡಿ", "Processing": "ಸಂಸ್ಕರಣೆ", "Pulp": "ತಿರುಳು", "Pickle": "ಉಪ್ಪಿನಕಾಯಿ", "Local Export": "ಸ್ಥಳೀಯ ರಫ್ತು", "Abroad Export": "ವಿದೇಶಿ ರಫ್ತು", "Cold Storage": "ಶೀತಲ ಸಂಗ್ರಹ", "FPO": "FPO"},
        "platform_ready":"✅ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಸಿದ್ಧವಾಗಿದೆ",
        "platform_overview":"📊 ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಅವಲೋಕನ",
        "live_lbl":"ಲೈವ್",
        "map_legend":"🏠 ಹೊಲ &nbsp;|&nbsp; <b style='color:#FF8C00;'>★ ಉತ್ತಮ ಮಾರುಕಟ್ಟೆ (ಚಿನ್ನ)</b> &nbsp;|&nbsp; ನಿಜವಾದ ರಸ್ತೆ ಮಾರ್ಗಗಳು",
        "loading_routes":"ಮಾರ್ಗಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        "mangonav_tag":"🥭 ಮ್ಯಾಂಗೋನಾವ್ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್",
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
    background-attachment: fixed;
}
.stApp::before{
    content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(255,255,255,0.85); z-index: -1;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%) !important;
    color: white !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.9) !important; font-weight: 500 !important; }

/* ── BUTTONS ── */
.stButton>button {
    width: 100%; border-radius: 12px !important; border: none !important;
    padding: 14px 24px !important; font-weight: 700 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(90deg, #FF8C00, #FFA500) !important; color: white !important;
    box-shadow: 0 4px 15px rgba(255,140,0,0.3) !important;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important; }

/* ── CARDS ── */
.glass-card {
    background: white; border-radius: 20px; padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.kpi-card { text-align: center; padding: 20px; border-radius: 16px; background: #F8FBF8; border-bottom: 4px solid #2E7D32; }
.kpi-val { font-size: 28px; font-weight: 800; color: #1B5E20; display: block; margin-bottom: 4px; }
.kpi-lbl { font-size: 13px; font-weight: 600; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── VOICE BUTTON ── */
.voice-btn {
    background: #007AFF; color: white; padding: 10px 20px; border-radius: 50px;
    font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ANALYTICS ENGINE
# ══════════════════════════════════════════════════════════════
VILLAGES = {
    "Punganur": [13.3650, 78.5800, "Chittoor"], "Madanapalle": [13.5500, 78.5000, "Chittoor"],
    "Chittoor": [13.2000, 79.1000, "Chittoor"], "Tirupati": [13.6285, 79.4192, "Tirupati"],
    "Renigunta": [13.6300, 79.5100, "Tirupati"], "Rayachoti": [14.0500, 78.7500, "Annamayya"],
    "Rajampet": [14.1800, 79.1500, "Annamayya"], "B.Kothakota": [13.6500, 78.3000, "Annamayya"]
}
MARKETS = [
    {"Name": "Chittoor Central Mandi", "Type": "Mandi", "Lat": 13.2100, "Lon": 79.0900, "Price": 42000, "Handling": 1500, "Risk": 8},
    {"Name": "Bangalore Export Hub", "Type": "Abroad Export", "Lat": 12.9716, "Lon": 77.5946, "Price": 68000, "Handling": 4500, "Risk": 15},
    {"Name": "Tirupati Processing Unit", "Type": "Processing", "Lat": 13.6500, "Lon": 79.4000, "Price": 38000, "Handling": 500, "Risk": 3},
    {"Name": "Chennai Marine Exports", "Type": "Abroad Export", "Lat": 13.0827, "Lon": 80.2707, "Price": 72000, "Handling": 6000, "Risk": 20},
    {"Name": "Anantapur Pulp Factory", "Type": "Pulp", "Lat": 14.6819, "Lon": 77.6006, "Price": 35000, "Handling": 800, "Risk": 5},
    {"Name": "Kolar Mango FPO", "Type": "FPO", "Lat": 13.1367, "Lon": 78.1292, "Price": 46000, "Handling": 1200, "Risk": 6},
    {"Name": "Palamaner Pickle Ind.", "Type": "Pickle", "Lat": 13.2000, "Lon": 78.7500, "Price": 39500, "Handling": 900, "Risk": 4},
    {"Name": "Madanapalle Mega Cold Storage", "Type": "Cold Storage", "Lat": 13.5600, "Lon": 78.5100, "Price": 44000, "Handling": 2500, "Risk": 2}
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = np.radians(lat2-lat1), np.radians(lon2-lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1-a))

def osm_route(lat1, lon1, lat2, lon2):
    try:
        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson", timeout=3)
        if r.status_code == 200: return [[p[1], p[0]] for p in r.json()['routes'][0]['geometry']['coordinates']]
    except: pass
    return [[lat1, lon1], [lat2, lon2]]

def run_analysis(vname, variety, qty):
    vlat, vlon, _ = VILLAGES[vname]
    res = []
    for m in MARKETS:
        dist = haversine(vlat, vlon, m["Lat"], m["Lon"])
        if dist > 150: continue
        trans_cost = dist * 12 * qty
        gross = m["Price"] * qty
        net = gross - trans_cost - (m["Handling"] * qty)
        res.append({**m, "Dist": dist, "Net_Profit": net, "Revenue": gross, "Transport": trans_cost})
    return pd.DataFrame(res).sort_values("Net_Profit", ascending=False).head(3)

# ══════════════════════════════════════════════════════════════
# AUTHENTICATION UI
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    cols = st.columns([1, 4, 1])
    with cols[1]:
        st.markdown(f"<div style='text-align:center;margin:60px 0 30px;'><h1 style='color:#1B5E20;font-size:48px;margin:0;'>{T['English']['title']}</h1><p style='color:#666;font-size:18px;'>{T['English']['tagline']}</p></div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            mode = st.tabs([T["English"]["sign_in"], T["English"]["register"]])
            
            with mode[0]:
                ph = st.text_input(T["English"]["phone"], placeholder=T["English"]["phone_ph"], key="login_ph")
                pw = st.text_input(T["English"]["password"], type="password", placeholder=T["English"]["pass_ph"], key="login_pw")
                if st.button(T["English"]["login_btn"], type="primary"):
                    u = login(ph, pw)
                    if u:
                        st.session_state.logged_in = True
                        st.session_state.user = u
                        st.session_state.just_logged_in = True
                        st.rerun()
                    else: st.error("Invalid credentials")
            
            with mode[1]:
                n = st.text_input(T["English"]["name"])
                p = st.text_input(T["English"]["place"])
                reg_ph = st.text_input(T["English"]["phone"], key="reg_ph")
                reg_pw = st.text_input(T["English"]["password"], type="password", key="reg_pw")
                if st.button(T["English"]["reg_btn"]):
                    if reg(n,p,reg_ph,reg_pw): st.success("Account created! Please sign in."); st.balloons()
                    else: st.error("Registration failed")
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # ══════════════════════════════════════════════════════════════
    # MAIN APP
    # ══════════════════════════════════════════════════════════════
    lang = st.sidebar.selectbox("Language", ["English", "Telugu", "Hindi", "Kannada"], index=["English", "Telugu", "Hindi", "Kannada"].index(st.session_state.lang))
    st.session_state.lang = lang
    lt = T[lang]

    st.sidebar.markdown(f"### {lt['farmer_profile']}")
    st.sidebar.info(f"👤 **{st.session_state.user[0]}**\n📍 {st.session_state.user[1]}")
    
    st.sidebar.markdown(f"### {lt['crop_data']}")
    v_options = list(VILLAGES.keys())
    sel_v = st.sidebar.selectbox(lt["village_sel"], v_options, index=v_options.index(st.session_state.last_village) if st.session_state.last_village in v_options else 0)
    var_options = ["Banganapalli", "Totapuri", "Neelam", "Rasalu"]
    sel_var = st.sidebar.selectbox(lt["variety_lbl"], var_options, index=var_options.index(st.session_state.last_variety))
    sel_qty = st.sidebar.number_input(lt["qty_lbl"], 1.0, 100.0, st.session_state.last_tonnes)
    
    if st.sidebar.button(lt["analyze_btn"], type="primary"):
        st.session_state.run = True
        st.session_state.last_village = sel_v
        st.session_state.last_variety = sel_var
        st.session_state.last_tonnes = sel_qty

    if st.sidebar.button(lt["logout"]):
        st.session_state.logged_in = False
        st.rerun()

    # ── HEADER ──
    st.markdown(f"""
    <div style="background:linear-gradient(90deg, #1B5E20, #2E7D32); padding: 20px 40px; color:white; display:flex; justify-content:space-between; align-items:center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div>
            <h2 style="margin:0; font-size:28px;">{lt['title']}</h2>
            <p style="margin:0; opacity:0.8;">{lt['tagline']}</p>
        </div>
        <div style="text-align:right;">
            <span style="background:rgba(255,255,255,0.2); padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700;">{lt['platform_ready']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.run:
        st.markdown(f"""
        <div style="text-align:center; padding:100px 20px;">
            <h1 style="color:#1B5E20; font-size:42px; margin-bottom:15px;">{lt['hero_title']}</h1>
            <p style="color:#666; font-size:20px; max-width:700px; margin:0 auto;">{lt['hero_sub']}</p>
            <div style="margin-top:40px; display:flex; justify-content:center; gap:40px;">
                <div style="text-align:center;"><span style="font-size:32px;">📈</span><p style="font-weight:600;">{lt['varieties_lbl']}</p></div>
                <div style="text-align:center;"><span style="font-size:32px;">🏢</span><p style="font-weight:600;">{lt['markets_lbl']}</p></div>
                <div style="text-align:center;"><span style="font-size:32px;">📍</span><p style="font-weight:600;">{lt['districts_lbl']}</p></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        df = run_analysis(sel_v, sel_var, sel_qty)
        if df.empty:
            st.warning(lt["no_results"])
        else:
            best = df.iloc[0]
            vlat, vlon, _ = VILLAGES[sel_v]

            # ── KPI ROW ──
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(f'<div class="kpi-card"><span class="kpi-val">₹{int(best["Net_Profit"]):,}</span><span class="kpi-lbl">{lt["kpi_profit"]}</span></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="kpi-card"><span class="kpi-val">{best["Name"]}</span><span class="kpi-lbl">{lt["kpi_market"]}</span></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="kpi-card"><span class="kpi-val">{int((best["Net_Profit"]/best["Revenue"])*100)}%</span><span class="kpi-lbl">{lt["kpi_roi"]}</span></div>', unsafe_allow_html=True)
            with c4: st.markdown(f'<div class="kpi-card"><span class="kpi-val">8</span><span class="kpi-lbl">{lt["kpi_markets"]}</span></div>', unsafe_allow_html=True)

            # ── MAIN CONTENT ──
            col_main, col_side = st.columns([2, 1])

            with col_main:
                st.markdown(f'<div class="glass-card"><h3>🗺️ {lt["map_title"]}</h3>', unsafe_allow_html=True)
                m = folium.Map(location=[vlat, vlon], zoom_start=9, tiles="cartodbpositron")
                folium.Marker([vlat, vlon], tooltip=lt["your_loc"], icon=folium.Icon(color='green', icon='home')).add_to(m)
                
                for i, row in df.iterrows():
                    rcol, wt, op, dash = ("#FF8C00", 6, 0.9, None) if i==0 else (["#2E7D32","#1565C0"][i-1], 4, 0.7, "8 4")
                    coords = osm_route(vlat, vlon, row["Lat"], row["Lon"])
                    folium.PolyLine(coords, color=rcol, weight=wt, opacity=op, dash_array=dash).add_to(m)
                    
                    if i==0:
                        folium.Marker([row["Lat"], row["Lon"]],
                            popup=folium.Popup(f"<b>{row['Name']}</b><br>{row['Type']}<br><span style='color:#2E7D32;font-weight:700;font-size:14px'>₹{int(row['Net_Profit']):,}</span>", max_width=220),
                            tooltip=f"BEST: {row['Name']}",
                            icon=folium.DivIcon(html='<div style="background:#FF8C00;border:3px solid white;border-radius:50%;width:46px;height:46px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;color:white;box-shadow:0 0 0 4px rgba(255,140,0,0.35),0 4px 18px rgba(255,140,0,0.6);">★</div>', icon_size=(46,46), icon_anchor=(23,23))
                        ).add_to(m)
                    else:
                        folium.CircleMarker([row["Lat"], row["Lon"]], radius=8, color=rcol, fill=True, fill_opacity=0.9).add_to(m)
                
                st_folium(m, width="100%", height=450)
                st.markdown(f"<p style='color:#666;font-size:13px;margin-top:10px;'>{lt['map_legend']}</p></div>", unsafe_allow_html=True)
                
                # Dynamic localized button for Google Maps navigation
                gmap_url = f"https://www.google.com/maps/dir/?api=1&origin={vlat},{vlon}&destination={best['Lat']},{best['Lon']}&travelmode=driving"
                btn_html = f"""
                <div style="margin-top:15px;">
                    <button onclick="window.open('{gmap_url}', '_blank')" style="
                        width:100%; padding:15px; background:#4285F4; color:white; border:none; border-radius:10px; 
                        font-weight:bold; font-family:sans-serif; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:10px;">
                        <img src="https://www.gstatic.com/images/branding/product/1x/maps_64dp.png" width="24px">
                        {lt['view_gmaps']}
                    </button>
                </div>
                """
                components.html(btn_html, height=70)

            with col_side:
                st.markdown(f'<div class="glass-card"><h3>🏆 {lt["top3"]}</h3>', unsafe_allow_html=True)
                for i, row in df.iterrows():
                    color = "#FF8C00" if i==0 else "#666"
                    rank_lbl = [lt["highest_profit"], lt["second_best"], lt["third_best"]][i]
                    st.markdown(f"""
                    <div style="padding:15px; border-radius:12px; background:#F8F9FA; margin-bottom:12px; border-left:5px solid {color};">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <span style="font-size:11px; font-weight:800; color:{color}; text-transform:uppercase;">{rank_lbl}</span>
                            <span style="font-size:11px; color:#999;">{int(row['Dist'])}{lt['away_lbl']}</span>
                        </div>
                        <div style="font-weight:700; font-size:16px; margin:4px 0;">{row['Name']}</div>
                        <div style="display:flex; justify-content:space-between; font-size:14px;">
                            <span style="color:#666;">{row['Type']}</span>
                            <span style="color:#2E7D32; font-weight:700;">₹{int(row['Net_Profit']):,}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="glass-card" style="background:#FFF9E6; border:none;">
                    <h4 style="color:#856404; margin-top:0;">💡 {lt['farmer_tip']}</h4>
                    <p style="color:#856404; font-size:14px; margin-bottom:0;">{lt['tip_text']}</p>
                </div>
                """, unsafe_allow_html=True)

            # ── CHARTS ──
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'<div class="glass-card"><h4>{lt["bar_title"]}</h4>', unsafe_allow_html=True)
                fig = go.Figure(go.Bar(x=df['Name'], y=df['Net_Profit'], marker_color=['#FF8C00', '#2E7D32', '#1565C0'], text=[f"₹{int(v):,}" for v in df['Net_Profit']], textposition='auto'))
                fig.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="glass-card"><h4>{lt["pie_title"]}</h4>', unsafe_allow_html=True)
                fig = go.Figure(go.Pie(labels=df['Type'], values=df['Revenue'], hole=.4, marker_colors=['#FF8C00', '#2E7D32', '#1565C0']))
                fig.update_layout(margin=dict(l=20,r=20,t=20,b=20), height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='text-align:center;color:#999;font-size:12px;padding-bottom:30px;'>{lt['mangonav_tag']} • v2.1 (Stability Fix)</p>", unsafe_allow_html=True)
