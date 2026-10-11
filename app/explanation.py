from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

import theme

root = Path(__file__).resolve().parent.parent
theme.load_data()

theme.hero(
    "MODEL TRANSPARENCY",
    "Understand the prediction",
    "Explore how the Logistic Regression model uses student features "
    "to estimate placement probability.",
)

model_path = root / "models" / "best_model.pkl"

if not model_path.exists():
    st.error(f"Model file not found: {model_path}")
    st.stop()

model = joblib.load(model_path)

feature_names = [
    "gender_Male",
    "degree_BE",
    "degree_BSc",
    "degree_BTech",
    "branch_CS",
    "branch_DS",
    "branch_Electrical",
    "branch_IT",
    "branch_Mechanical",
    "age",
    "cgpa",
    "backlogs",
    "internships",
    "certifications",
    "coding_skills",
    "communication_skills",
    "aptitude_score",
    "projects",
]

st.markdown(
    "<div class='section-title'>Model overview</div>",
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Model type",
    type(model).__name__,
)

c2.metric(
    "Features used",
    getattr(model, "n_features_in_", len(feature_names)),
)

c3.metric(
    "Test accuracy",
    "85.67%",
)

st.markdown(
    "<div class='section-title'>How the model makes predictions</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="glass-card">
        <div class="card-copy">
            Logistic Regression combines the student's input features
            to estimate the probability of placement. Each feature has
            a model coefficient that indicates its contribution to the
            prediction.
        </div>
        <br>
        <div class="card-copy">
            Positive coefficients increase the estimated placement
            probability, while negative coefficients decrease it.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if hasattr(model, "coef_"):
    coefficients = model.coef_[0]

    if len(coefficients) == len(feature_names):
        coefficient_df = pd.DataFrame({
            "Feature": feature_names,
            "Coefficient": coefficients,
            "Absolute Impact": abs(coefficients),
        })

        coefficient_df = coefficient_df.sort_values(
            "Absolute Impact",
            ascending=False,
        )

        st.markdown(
            "<div class='section-title'>Feature contribution</div>",
            unsafe_allow_html=True,
        )

        display_df = coefficient_df.head(12).sort_values(
            "Coefficient"
        )

        fig = px.bar(
            display_df,
            x="Coefficient",
            y="Feature",
            orientation="h",
            color="Coefficient",
            color_continuous_scale=["#ef4444", "#94a3b8", "#22c55e"],
            template="plotly_dark",
        )

        fig.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis_title="Model coefficient",
            yaxis_title="Feature",
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            coefficient_df[
                ["Feature", "Coefficient"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        positive = coefficient_df[
            coefficient_df["Coefficient"] > 0
        ].head(5)

        negative = coefficient_df[
            coefficient_df["Coefficient"] < 0
        ].sort_values(
            "Coefficient"
        ).head(5)

        st.markdown(
            "<div class='section-title'>Key model signals</div>",
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="card-copy">
                        <b>Positive model signals</b>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            for _, row in positive.iterrows():
                st.write(
                    f"• {row['Feature']}: "
                    f"{row['Coefficient']:.3f}"
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="card-copy">
                        <b>Negative model signals</b>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            for _, row in negative.iterrows():
                st.write(
                    f"• {row['Feature']}: "
                    f"{row['Coefficient']:.3f}"
                )

            st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="notice">
        <b>Interpretation note:</b> Coefficients describe how the trained
        model uses the available features. They do not prove that a feature
        directly causes placement. Model performance can also change when
        evaluated on new or different student populations.
    </div>
    """,
    unsafe_allow_html=True,
)