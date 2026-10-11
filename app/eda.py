import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency
import theme

df = theme.load_data()

theme.hero(
    "DISCOVER PATTERNS",
    "Exploratory Data Analysis",
    "Explore distributions and relationships across student attributes. "
    "Associations in the dataset do not establish causation.",
)

placed = int((df["placed"] == 1).sum())
total = len(df)

a, b, c = st.columns(3)
a.metric("Placement rate", f"{placed / total * 100:.2f}%")
b.metric("Placed", f"{placed:,}")
c.metric("Not placed", f"{total - placed:,}")

st.markdown(
    "<div class='section-title'>Placement by category</div>",
    unsafe_allow_html=True,
)

categorical_columns = [
    column for column in ["gender", "degree", "branch"]
    if column in df.columns
]

if categorical_columns:
    selected = st.selectbox("Choose a category", categorical_columns)

    rates = (
        df.groupby(selected, dropna=False)
        .agg(
            students=("placed", "size"),
            placement_rate=("placed", "mean"),
        )
        .reset_index()
    )

    rates["placement_rate"] *= 100

    fig = px.bar(
        rates,
        x=selected,
        y="placement_rate",
        color="placement_rate",
        text=rates["placement_rate"].map(lambda value: f"{value:.1f}%"),
        color_continuous_scale=["#7c3aed", "#22d3ee"],
        template="plotly_dark",
        hover_data={"students": True, "placement_rate": ":.2f"},
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_title="Placement rate (%)",
        xaxis_title=selected.title(),
    )

    st.plotly_chart(fig, use_container_width=True)

    display_rates = rates.rename(
        columns={
            selected: selected.title(),
            "students": "Students",
            "placement_rate": "Placement rate (%)",
        }
    )

    st.dataframe(
        display_rates.style.format({"Placement rate (%)": "{:.2f}%"}),
        use_container_width=True,
        hide_index=True,
    )

st.markdown(
    "<div class='section-title'>Numerical feature relationships</div>",
    unsafe_allow_html=True,
)

numeric_columns = [
    column for column in df.select_dtypes(include="number").columns
    if column != "placed"
]

if numeric_columns:
    defaults = [
        column for column in
        ["cgpa", "coding_skills", "aptitude_score", "internships"]
        if column in numeric_columns
    ]

    chosen = st.multiselect(
        "Features to compare",
        numeric_columns,
        default=defaults,
    )

    if chosen:
        columns_for_corr = chosen.copy()
        if "placed" in df.columns and "placed" not in columns_for_corr:
            columns_for_corr.append("placed")

        corr = df[columns_for_corr].corr(numeric_only=True)

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
            template="plotly_dark",
        )

        fig.update_layout(
            height=max(350, 50 * len(corr)),
            paper_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)

        if "placed" in corr.columns:
            st.caption(
                "Correlation indicates association in this dataset; "
                "it does not establish causation."
            )

            corr_table = (
                corr[["placed"]]
                .drop(index="placed", errors="ignore")
                .sort_values("placed", ascending=False)
                .rename(columns={"placed": "Correlation with placement"})
            )

            st.dataframe(corr_table, use_container_width=True)

st.markdown(
    "<div class='section-title'>Placed vs not placed profiles</div>",
    unsafe_allow_html=True,
)

compare_columns = [
    column for column in [
        "cgpa",
        "coding_skills",
        "communication_skills",
        "aptitude_score",
        "internships",
        "certifications",
        "projects",
        "backlogs",
    ]
    if column in df.columns
]

if compare_columns:
    summary = (
        df.groupby("placed")[compare_columns]
        .mean()
        .T.reset_index()
        .rename(
            columns={
                "index": "Feature",
                0: "Not placed",
                1: "Placed",
            }
        )
    )

    st.dataframe(summary, use_container_width=True, hide_index=True)

    feature = st.selectbox(
        "Visualize a feature",
        compare_columns,
        index=(
            compare_columns.index("coding_skills")
            if "coding_skills" in compare_columns else 0
        ),
    )

    fig = px.box(
        df,
        x="placed",
        y=feature,
        color="placed",
        color_discrete_map={0: "#8b5cf6", 1: "#67e8f9"},
        template="plotly_dark",
        points="outliers",
    )

    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Not placed", "Placed"],
        ),
    )

    st.plotly_chart(fig, use_container_width=True)