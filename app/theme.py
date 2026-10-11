
from pathlib import Path

import streamlit as st


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080d1c;
        --panel: #121b32;
        --line: rgba(167,139,250,.22);
        --muted: #a8b4d0;
        --purple: #a78bfa;
        --cyan: #67e8f9;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 10% 10%, rgba(124,58,237,.20), transparent 38%),
            radial-gradient(ellipse at 90% 30%, rgba(6,182,212,.14), transparent 35%),
            linear-gradient(135deg, #080d1c, #0d1428 55%, #080d1c);
        background-attachment: fixed;
        color: #eef2ff;
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1225, #10152b);
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] * {
        color: #eef2ff;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 5rem;
    min-height: auto;
}
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #f5f3ff !important;
    }

    p, label {
        color: #cbd5e1;
    }

    /* Animated ambient glow */

    .stApp::before,
    .stApp::after {
        content: "";
        position: fixed;
        pointer-events: none;
        z-index: 0;
        border-radius: 50%;
        filter: blur(90px);
        opacity: .25;
        animation: ambientDrift 18s ease-in-out infinite alternate;
    }

    .stApp::before {
        width: 340px;
        height: 340px;
        background: #7048ff;
        left: -130px;
        top: 12%;
    }

    .stApp::after {
        width: 300px;
        height: 300px;
        background: #00c9ee;
        right: -100px;
        top: 50%;
        animation-delay: -8s;
    }

    @keyframes ambientDrift {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(45px, -35px) scale(1.1); }
        100% { transform: translate(-20px, 40px) scale(.95); }
    }

    /* Floating emoji background */

    .floating-elements {
        position: fixed;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    
.float-item {
    position: absolute;
    bottom: -70px;
    opacity: 0;
    animation: floatUp linear infinite;
    user-select: none;
}

.shape-circle {
    width: 12px;
    height: 12px;
    border: 1px solid rgba(103,232,249,.7);
    border-radius: 50%;
}

.shape-diamond {
    width: 10px;
    height: 10px;
    border: 1px solid rgba(167,139,250,.8);
    transform: rotate(45deg);
}

.shape-ring {
    width: 24px;
    height: 24px;
    border: 1px solid rgba(96,165,250,.55);
    border-radius: 50%;
}

.shape-square {
    width: 9px;
    height: 9px;
    border: 1px solid rgba(240,171,252,.7);
}

.float-item:nth-child(1) {
    left: 7%;
    animation-duration: 19s;
    animation-delay: -5s;
}

.float-item:nth-child(2) {
    left: 20%;
    animation-duration: 24s;
    animation-delay: -12s;
}

.float-item:nth-child(3) {
    left: 36%;
    animation-duration: 21s;
    animation-delay: -8s;
}

.float-item:nth-child(4) {
    left: 52%;
    animation-duration: 25s;
    animation-delay: -17s;
}

.float-item:nth-child(5) {
    left: 67%;
    animation-duration: 20s;
    animation-delay: -10s;
}

.float-item:nth-child(6) {
    left: 81%;
    animation-duration: 23s;
    animation-delay: -7s;
}

.float-item:nth-child(7) {
    left: 92%;
    animation-duration: 22s;
    animation-delay: -15s;
}

    @keyframes floatUp {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 0;
        }
        15% {
            opacity: .35;
        }
        50% {
            transform: translateY(-50vh) rotate(12deg);
            opacity: .25;
        }
        100% {
            transform: translateY(-115vh) rotate(-15deg);
            opacity: 0;
        }
    }

    /* Twinkling particles */

    .particle-field {
        position: fixed;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #8be9ff;
        box-shadow: 0 0 14px #67e8f9;
        animation: twinkle 4s ease-in-out infinite alternate;
    }

    .particle:nth-child(1) { top: 17%; left: 14%; }
    .particle:nth-child(2) { top: 31%; left: 29%; animation-delay: -1s; }
    .particle:nth-child(3) { top: 66%; left: 12%; animation-delay: -2s; }
    .particle:nth-child(4) { top: 74%; left: 37%; animation-delay: -3s; }
    .particle:nth-child(5) { top: 22%; left: 72%; animation-delay: -1.5s; }
    .particle:nth-child(6) { top: 48%; left: 88%; animation-delay: -.5s; }
    .particle:nth-child(7) { top: 83%; left: 77%; animation-delay: -2.5s; }
    .particle:nth-child(8) { top: 39%; left: 57%; animation-delay: -3.5s; }

    @keyframes twinkle {
        from { opacity: .12; transform: scale(.7); }
        to { opacity: .75; transform: scale(1.5); }
    }

    /* Keep page content above decorative background */

    [data-testid="stMain"],
    [data-testid="stSidebar"],
    [data-testid="stHeader"] {
        position: relative;
        z-index: 1;
    }

    /* Metrics */

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #17213d, #10182c);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px;
        transition: transform .2s ease, border-color .2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #a78bfa;
    }

    [data-testid="stMetricLabel"] {
        color: #a8b4d0 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Buttons */

    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(100deg, #7c3aed, #2563eb);
        color: white !important;
        border: 1px solid rgba(167,139,250,.45);
        border-radius: 10px;
        font-weight: 700;
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(87,76,211,.3);
        border-color: #67e8f9;
    }

    /* Inputs */

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    [data-baseweb="select"] {
        background: #10182c !important;
        color: white !important;
        border-color: var(--line) !important;
        border-radius: 10px !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stPlotlyChart"] {
        background: rgba(18,27,50,.65);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 8px;
    }

    hr {
        border-color: var(--line) !important;
    }
    

    /* Hero banner */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 34px;
        margin: 4px 0 25px;
        border: 1px solid rgba(167,139,250,.3);
        border-radius: 22px;
        background: linear-gradient(115deg, #1b2144, #10243c 65%, #102e3b);
        box-shadow: 0 18px 45px rgba(0,0,0,.18);
    }

    .hero::before {
        content: "";
        position: absolute;
        right: -55px;
        top: -120px;
        width: 260px;
        height: 260px;
        border: 1px solid rgba(103,232,249,.3);
        border-radius: 50%;
        box-shadow:
            0 0 0 22px rgba(103,232,249,.04),
            0 0 0 48px rgba(167,139,250,.04);
        animation: orbit 18s linear infinite;
        pointer-events: none;
    }

    .hero::after {
        content: "✦";
        position: absolute;
        right: 12%;
        top: 20%;
        color: rgba(103,232,249,.45);
        font-size: 52px;
        animation: heroFloat 4s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes orbit {
        to { transform: rotate(360deg); }
    }

    @keyframes heroFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-12px) rotate(12deg); }
    }

    .eyebrow {
        position: relative;
        z-index: 1;
        color: #a5b4fc;
        font-size: .76rem;
        letter-spacing: .16em;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero h1 {
        position: relative;
        z-index: 1;
        font-size: clamp(2rem, 4vw, 3.2rem);
        line-height: 1.12;
        margin: 0 0 14px;
        background: linear-gradient(90deg, #ffffff, #c4b5fd, #67e8f9);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        position: relative;
        z-index: 1;
        max-width: 780px;
        line-height: 1.7;
        color: #cbd5e1;
        margin: 0;
    }

    /* Reusable feature cards */

    .glass-card {
        height: 100%;
        padding: 20px;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: linear-gradient(145deg, #17213d, #10182c);
        transition: transform .2s ease, border-color .2s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: #67e8f9;
    }

    .card-icon {
        font-size: 1.6rem;
        margin-bottom: 12px;
    }

    .card-title {
        color: #f5f3ff;
        font-weight: 800;
        font-size: 1.05rem;
        margin-bottom: 8px;
    }

    .card-copy {
        color: #a8b4d0;
        font-size: .9rem;
        line-height: 1.6;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #f5f3ff;
        margin: 22px 0 12px;
    }

    .pill {
        display: inline-block;
        padding: 5px 10px;
        margin: 3px;
        border-radius: 999px;
        color: #a5f3fc;
        background: rgba(103,232,249,.08);
        border: 1px solid rgba(103,232,249,.2);
        font-size: .76rem;
    }

    .notice {
        padding: 14px 16px;
        border-radius: 12px;
        background: rgba(96,165,250,.09);
        border: 1px solid rgba(96,165,250,.25);
        color: #dbeafe;
        line-height: 1.6;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #8b5cf6, #22d3ee);
    }

    @media (max-width: 700px) {
        .hero {
            padding: 24px;
        }

        .hero h1 {
            font-size: 2rem;
        }

        .block-container {
            padding-top: 1.2rem;
        }

        .float-item {
            font-size: 17px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



st.markdown(
    """
    <div class="floating-elements">
        <span class="float-item shape-circle"></span>
        <span class="float-item shape-diamond"></span>
        <span class="float-item shape-ring"></span>
        <span class="float-item shape-square"></span>
        <span class="float-item shape-circle"></span>
        <span class="float-item shape-diamond"></span>
        <span class="float-item shape-ring"></span>
    </div>

    <div class="particle-field">
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
        <span class="particle"></span>
    </div>
    """,
    unsafe_allow_html=True,
)

def hero(eyebrow, title, description):
    st.markdown(
        f"""
        <section class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{description}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def card(icon, title, description):
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data():
    import pandas as pd

    project_root = Path(__file__).resolve().parent.parent
    path = project_root / "data" / "processed" / "student_placement_cleaned.csv"

    if not path.exists():
        st.error(f"Dataset not found: {path}")
        st.info(
            "Ensure the cleaned dataset exists at "
            "data/processed/student_placement_cleaned.csv."
        )
        st.stop()

    data = pd.read_csv(path)

    if data.empty:
        st.error("The cleaned dataset contains no rows.")
        st.stop()

    return data