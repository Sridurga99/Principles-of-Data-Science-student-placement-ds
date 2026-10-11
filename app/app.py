import importlib
import sys
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="PlacementIQ | Student Analytics",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

if "theme" in sys.modules:
    theme = importlib.reload(sys.modules["theme"])
else:
    import theme

pages = [
    st.Page(str(APP_DIR / "home.py"), title="Overview", default=True),
    st.Page(str(APP_DIR / "dataset_explorer.py"), title="Dataset Explorer"),
    st.Page(str(APP_DIR / "eda.py"), title="EDA & Insights"),
    st.Page(str(APP_DIR / "prediction.py"), title="Placement Prediction"),
    st.Page(str(APP_DIR / "explanation.py"), title="Model Explanation"),
    st.Page(str(APP_DIR / "segmentation.py"), title="Student Segmentation"),
    st.Page(str(APP_DIR / "skill_gap.py"), title="Skill Gap Analysis"),
    st.Page(str(APP_DIR / "model_comparison.py"), title="Model Comparison"),
    st.Page(str(APP_DIR / "recommendations.py"), title="Recommendations"),
]

st.sidebar.markdown(
    """
    <div style="padding:12px 8px 22px">
        <div style="font-size:2rem;color:#67e8f9">◈</div>
        <div style="font-size:1.35rem;font-weight:800;color:#f5f7ff">
            PLACEMENT<span style="color:#a78bfa">IQ</span>
        </div>
        <div style="font-size:.72rem;color:#8fa0c4;letter-spacing:.15em">
            STUDENT ANALYTICS
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    "<div style='font-size:.72rem;color:#8fa0c4;"
    "letter-spacing:.15em;padding:0 8px 8px'>WORKSPACE</div>",
    unsafe_allow_html=True,
)

navigation = st.navigation(pages, position="sidebar")

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="padding:4px 8px;color:#8798bb;font-size:.78rem;line-height:1.8">
        Data-driven insights for placement readiness.
        <br>
        <span style="color:#67e8f9">●</span> Analytics workspace
    </div>
    """,
    unsafe_allow_html=True,
)

navigation.run()