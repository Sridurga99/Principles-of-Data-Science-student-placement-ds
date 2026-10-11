import streamlit as st
import plotly.graph_objects as go
import theme

df = theme.load_data()

placed_count = int((df["placed"] == 1).sum())
not_placed_count = int((df["placed"] == 0).sum())
rate = placed_count / len(df) * 100 if len(df) else 0
avg_cgpa = df["cgpa"].mean() if "cgpa" in df else 0
avg_coding = df["coding_skills"].mean() if "coding_skills" in df else 0

theme.hero(
    "STUDENT CAREER ANALYTICS · PLACEMENT DATASET",
    "Turn student data into actionable placement insights.",
    "Explore placement trends, evaluate student profiles, understand model "
    "behaviour, and identify the skills that deserve attention.",
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Students analysed",
    f"{len(df):,}",
)

c2.metric(
    "Placed students",
    f"{placed_count:,}",
)

c3.metric(
    "Dataset placement rate",
    f"{rate:.1f}%",
)

c4.metric(
    "Average CGPA",
    f"{avg_cgpa:.2f}",
)

st.markdown(
    "<div class='section-title'>Placement Intelligence Workspace</div>",
    unsafe_allow_html=True,
)

items = [
    (
        "📊",
        "EDA & Insights",
        "Explore distributions, placement rates and feature relationships.",
    ),
    (
        "🎯",
        "Placement Prediction",
        "Evaluate a student profile using the saved classification model.",
    ),
    (
        "🧠",
        "Model Explanation",
        "Explore the features used by the trained model and understand how it makes predictions.",
    ),
    (
        "👥",
        "Student Segmentation",
        "Compare groups with similar academic and skill profiles.",
    ),
    (
        "🧩",
        "Skill Gap Analysis",
        "Compare student attributes against placed-student benchmarks.",
    ),
    (
        "🚀",
        "Recommendations",
        "Turn identified skill gaps into practical improvement steps.",
    ),
]

for start in (0, 3):
    columns = st.columns(3)

    for col, item in zip(columns, items[start:start + 3]):
        with col:
            theme.card(*item)

left, right = st.columns([1.3, 1])

with left:
    st.markdown(
        "<div class='section-title'>Placement Distribution</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Placed", "Not placed"],
                values=[placed_count, not_placed_count],
                hole=0.72,
                sort=False,
                marker=dict(
                    colors=["#67e8f9", "#8b5cf6"],
                    line=dict(
                        color="#10172b",
                        width=4,
                    ),
                ),
                textinfo="label+percent",
                textfont=dict(
                    color="#eef2ff",
                    size=13,
                ),
                hovertemplate=(
                    "%{label}<br>%{value:,} students"
                    "<br>%{percent}<extra></extra>"
                ),
            )
        ]
    )

    fig.update_layout(
        height=330,
        margin=dict(
            l=8,
            r=8,
            t=18,
            b=8,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        annotations=[
            dict(
                text=(
                    f"{rate:.1f}%<br>"
                    "<span style='font-size:11px'>placed</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=25,
                    color="#f3f5ff",
                ),
            )
        ],
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with right:
    st.markdown(
        "<div class='section-title'>Dataset Snapshot</div>",
        unsafe_allow_html=True,
    )

    snapshot = [
        (
            "Average coding skill",
            f"{avg_coding:.2f} / 10",
        ),
        (
            "Branches represented",
            str(df["branch"].nunique())
            if "branch" in df
            else "—",
        ),
        (
            "Degree categories",
            str(df["degree"].nunique())
            if "degree" in df
            else "—",
        ),
    ]

    for label, value in snapshot:
        st.markdown(
            f"""
            <div class="glass-card"
                 style="padding:16px 18px;margin-bottom:10px;
                        display:flex;justify-content:space-between;
                        align-items:center">
                <span style="color:#aab8d6">{label}</span>
                <b style="color:#eef2ff;font-size:1.05rem">{value}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="notice">
            These statistics describe this dataset. They do not guarantee
            an individual student's placement outcome.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    "<div class='section-title'>How to Use the Platform</div>",
    unsafe_allow_html=True,
)

steps = st.columns(4)

step_data = [
    (
        "01",
        "Explore",
        "Inspect the dataset and placement trends.",
    ),
    (
        "02",
        "Predict",
        "Evaluate a student profile using the trained model.",
    ),
    (
        "03",
        "Understand",
        "Review the model's influential features.",
    ),
    (
        "04",
        "Improve",
        "Use skill gaps to plan targeted next steps.",
    ),
]

for col, (number, title, description) in zip(steps, step_data):
    with col:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="eyebrow">{number} / STEP</div>
                <div class="card-title">{title}</div>
                <div class="card-copy">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )