import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

import theme

df = theme.load_data()

theme.hero(
    "UNSUPERVISED LEARNING",
    "Student Segmentation",
    "Explore groups with similar academic and skill profiles. Clusters "
    "are descriptive groups, not placement predictions or labels of ability.",
)

features = [
    column
    for column in [
        "cgpa",
        "backlogs",
        "internships",
        "certifications",
        "coding_skills",
        "communication_skills",
        "aptitude_score",
        "projects",
        "age",
    ]
    if column in df.columns
]

if len(features) < 2:
    st.warning("At least two numeric profile features are required.")
    st.stop()

default_features = [
    column
    for column in [
        "cgpa",
        "coding_skills",
        "aptitude_score",
        "backlogs",
        "internships",
        "projects",
    ]
    if column in features
]

selected = st.multiselect(
    "Features used for clustering",
    features,
    default=default_features,
)

k = st.slider("Number of clusters", 2, 6, 2)

if len(selected) < 2:
    st.info("Select at least two features to continue.")
    st.stop()

X = df[selected].apply(pd.to_numeric, errors="coerce")
X = X.fillna(X.median()).fillna(0)

scaled = StandardScaler().fit_transform(X)

labels = KMeans(
    n_clusters=k,
    random_state=42,
    n_init=10,
).fit_predict(scaled)

result = df.copy()
result["cluster"] = labels

silhouette = (
    silhouette_score(scaled, labels)
    if len(result) > k and result["cluster"].nunique() > 1
    else float("nan")
)

a, b, c = st.columns(3)
a.metric("Clusters", k)
b.metric("Students grouped", f"{len(result):,}")
c.metric(
    "Silhouette score",
    f"{silhouette:.3f}" if pd.notna(silhouette) else "N/A",
)

st.caption(
    "A low silhouette score suggests that the clusters overlap "
    "rather than forming sharply separated groups."
)

left, right = st.columns(2)

with left:
    counts = (
        result["cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("Cluster")
        .reset_index(name="Students")
    )

    fig = px.bar(
        counts,
        x="Cluster",
        y="Students",
        color="Cluster",
        color_discrete_sequence=[
            "#8b5cf6", "#22d3ee", "#f0abfc",
            "#60a5fa", "#34d399", "#fbbf24",
        ],
        template="plotly_dark",
        text="Students",
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    rates = (
        result.groupby("cluster")
        .agg(
            Students=("placed", "size"),
            Placement_rate=("placed", "mean"),
        )
        .reset_index()
    )

    rates["Placement_rate"] *= 100

    fig = px.bar(
        rates,
        x="cluster",
        y="Placement_rate",
        color="cluster",
        color_discrete_sequence=[
            "#8b5cf6", "#22d3ee", "#f0abfc",
            "#60a5fa", "#34d399", "#fbbf24",
        ],
        text=rates["Placement_rate"].map(lambda value: f"{value:.1f}%"),
        template="plotly_dark",
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title="Cluster",
        yaxis_title="Placement rate (%)",
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<div class='section-title'>Cluster profiles</div>",
    unsafe_allow_html=True,
)

profile_columns = selected.copy()

if "placed" in result.columns and "placed" not in profile_columns:
    profile_columns.append("placed")

profile = (
    result.groupby("cluster")[profile_columns]
    .mean()
    .reset_index()
)

st.dataframe(profile, use_container_width=True, hide_index=True)

x_axis = st.selectbox("X-axis", selected, index=0)
y_options = [feature for feature in selected if feature != x_axis]
y_axis = st.selectbox("Y-axis", y_options, index=0)

sample = result.sample(min(len(result), 3000), random_state=42)

fig = px.scatter(
    sample,
    x=x_axis,
    y=y_axis,
    color=sample["cluster"].astype(str),
    color_discrete_sequence=[
        "#8b5cf6", "#22d3ee", "#f0abfc",
        "#60a5fa", "#34d399", "#fbbf24",
    ],
    opacity=0.72,
    template="plotly_dark",
    hover_data=[
        column for column in [
            "cgpa", "coding_skills", "aptitude_score", "placed"
        ]
        if column in sample.columns
    ],
)

fig.update_layout(
    height=430,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title="Cluster",
)

st.plotly_chart(fig, use_container_width=True)

st.download_button(
    "Download segmented dataset",
    result.to_csv(index=False).encode("utf-8"),
    file_name="student_segments.csv",
    mime="text/csv",
)