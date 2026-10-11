import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import theme

df = theme.load_data()

theme.hero(
    "SKILL DEVELOPMENT",
    "Skill Gap Analysis",
    "Compare a profile with the median values observed among placed "
    "students, then use the gaps to guide improvement priorities.",
)

metrics = [
    ("cgpa", "CGPA", 10),
    ("coding_skills", "Coding skills", 10),
    ("aptitude_score", "Aptitude score", 100),
    ("communication_skills", "Communication skills", 10),
    ("internships", "Internships", 10),
    ("certifications", "Certifications", 10),
    ("projects", "Projects", 10),
]

placed = df[df["placed"] == 1]

if placed.empty:
    st.warning("No placed-student records were found.")
    st.stop()

benchmarks = {
    column: float(placed[column].median())
    for column, _, _ in metrics
    if column in placed.columns
}

with st.form("skill_gap_form"):
    st.markdown(
        "<div class='section-title'>Your current profile</div>",
        unsafe_allow_html=True,
    )

    values = {}
    columns = st.columns(3)

    for index, (column, label, maximum) in enumerate(metrics):
        if column not in df.columns:
            continue

        default = float(df[column].median())
        default = min(float(maximum), max(0.0, default))

        with columns[index % 3]:
            values[column] = st.number_input(
                label,
                min_value=0.0,
                max_value=float(maximum),
                value=default,
                step=0.1 if column == "cgpa" else 1.0,
            )

    submitted = st.form_submit_button(
        "Analyse my skill gaps",
        use_container_width=True,
    )

if submitted:
    st.session_state["student_profile"] = values.copy()
    rows = []

    for column, label, maximum in metrics:
        if column not in values or column not in benchmarks:
            continue

        current = float(values[column])
        target = benchmarks[column]
        gap = max(0.0, target - current)
        normalized_gap = gap / maximum * 100

        rows.append({
            "Skill": label,
            "Your value": current,
            "Placed-student median": target,
            "Gap": gap,
            "Gap percentage": normalized_gap,
        })

    gaps = pd.DataFrame(rows).sort_values(
        "Gap percentage",
        ascending=False,
    )

    left, right = st.columns(2)

    with left:
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                name="Your profile",
                y=gaps["Skill"],
                x=gaps["Your value"],
                orientation="h",
                marker_color="#8b5cf6",
            )
        )

        fig.add_trace(
            go.Bar(
                name="Placed-student median",
                y=gaps["Skill"],
                x=gaps["Placed-student median"],
                orientation="h",
                marker_color="#67e8f9",
            )
        )

        fig.update_layout(
            barmode="group",
            height=430,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Value",
            legend_orientation="h",
            margin=dict(l=10, r=10, t=30, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        sorted_gaps = gaps.sort_values("Gap percentage")

        fig = px.bar(
            sorted_gaps,
            x="Gap percentage",
            y="Skill",
            orientation="h",
            color="Gap percentage",
            color_continuous_scale=["#22d3ee", "#8b5cf6"],
            template="plotly_dark",
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis_title="Normalized gap (%)",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "<div class='section-title'>Priority list</div>",
        unsafe_allow_html=True,
    )

    st.dataframe(gaps, use_container_width=True, hide_index=True)

    if not gaps.empty:
        top = gaps.iloc[0]

        st.markdown(
            f"""
            <div class="notice">
                <b>Suggested starting point:</b> {top["Skill"]} has
                the largest normalized gap compared with the
                placed-student median in this profile.
                Consider it alongside your interests and career goals.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.download_button(
        "Download skill-gap report",
        gaps.to_csv(index=False).encode("utf-8"),
        file_name="skill_gap_report.csv",
        mime="text/csv",
    )

else:
    st.markdown(
        "<div class='section-title'>Placed-student reference benchmarks</div>",
        unsafe_allow_html=True,
    )

    cards = st.columns(3)

    for index, (column, label, _) in enumerate(metrics):
        if column in benchmarks:
            with cards[index % 3]:
                st.metric(
                    f"Median {label}",
                    f"{benchmarks[column]:.2f}",
                )

st.caption(
    "These are descriptive dataset benchmarks, not universal hiring "
    "cut-offs or evidence of causal effects."
)