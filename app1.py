# 🔥 FULL STREAMLIT APP (UPGRADED UI ONLY)

```python
import streamlit as st

st.set_page_config(layout="wide")

# ─────────────────────────────────────────────────────────────
# 🔥 INSANE LEVEL UI CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* RESET */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header {visibility:hidden;}

/* 🌾 REAL BACKGROUND */
.stApp {
    background:
        linear-gradient(rgba(6, 30, 12, 0.75), rgba(6, 30, 12, 0.75)),
        url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80");
    background-size: cover;
    background-attachment: fixed;
}

/* ✨ FLOATING LIGHT EFFECT */
.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.08), transparent 40%),
                radial-gradient(circle at 70% 60%, rgba(255,255,255,0.06), transparent 40%);
    animation: float 18s infinite linear;
}
@keyframes float {
    0% {transform: translate(0,0);}
    50% {transform: translate(-5%,-5%);}
    100% {transform: translate(0,0);}
}

/* 🧊 GLASS PANEL */
.main .block-container {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 20px;
    margin: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

/* 📦 CARDS */
.card {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}

/* 🔘 BUTTON */
.stButton > button {
    background: linear-gradient(135deg,#FF8C00,#E65100);
    color:white;
    border-radius:12px;
    font-weight:700;
}
.stButton > button:hover {
    transform: scale(1.05);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0D1B12,#132218);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 🎯 DEMO CONTENT (YOUR UI WILL APPLY HERE)
# ─────────────────────────────────────────────────────────────

st.title("🌾 MangoNav Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">💰 Profit<br><h2>₹5,49,223</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">📍 Market<br><h2>Yerravaripalem</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">📈 ROI<br><h2>96%</h2></div>', unsafe_allow_html=True)

st.button("Run Analysis")

st.write("Now your full app UI will look premium automatically.")
```
