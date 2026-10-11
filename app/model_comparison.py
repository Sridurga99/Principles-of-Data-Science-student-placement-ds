import pandas as pd
import plotly.express as px
import streamlit as st

import theme

theme.hero(
    "EVALUATION WORKSPACE",
    "Model Comparison",
    "Compare the evaluation metrics recorded during model development.",
)

metrics = pd.DataFrame([
    {
        "Model": "Logistic Regression",
        "Accuracy": 85.67,
        "Precision": 79.15,
        "Recall": 71.78,
        "F1-score": 75.29,
        "ROC-AUC": 92.03,
    },
    {
        "Model": "Decision Tree",
        "Accuracy": 100.0,
        "Precision": 100.0,
        "Recall": 100.0,
        "F1-score": 100.0,
        "ROC-AUC": 100.0,
    },
    {
        "Model": "Random Forest",
        "Accuracy": 100.0,
        "Precision": 100.0,
        "Recall": 100.0,
        "F1-score": 100.0,
        "ROC-AUC": 100.0,
    },
    {
        "Model": "XGBoost",
        "Accuracy": 100.0,
        "Precision": 100.0,
        "Recall": 100.0,
        "F1-score": 100.0,
        "ROC-AUC": 100.0,
    },
])

columns = st.columns(4)

for column, (_, row) in zip(columns, metrics.iterrows()):
    with column:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-copy">{row["Model"]}</div>
                <div style="font-size:1.8rem;font-weight:800;
                            color:#67e8f9;margin:10px 0">
                    {row["Accuracy"]:.2f}%
                </div>
                <div class="card-copy">Test accuracy</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

metric = st.selectbox(
    "Metric to compare",
    ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"],
)

fig = px.bar(
    metrics,
    x="Model",
    y=metric,
    color="Model",
    text=metrics[metric].map(lambda value: f"{value:.2f}%"),
    color_discrete_sequence=[
        "#8b5cf6", "#67e8f9", "#f0abfc", "#60a5fa"
    ],
    template="plotly_dark",
)

fig.update_layout(
    height=400,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    yaxis_title=f"{metric} (%)",
    yaxis_range=[0, 105],
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(metrics, use_container_width=True, hide_index=True)

st.markdown(
    """
    <div class="notice">
        <b>Dataset validation note:</b> Tree-based models achieved perfect
        test-set scores on this dataset. The placement classes show strong
        separation across CGPA, coding skills, and aptitude score.
        Therefore, these results should be interpreted as dataset-specific
        performance rather than evidence of perfect real-world placement
        prediction.
    </div>
    """,
    unsafe_allow_html=True,
)