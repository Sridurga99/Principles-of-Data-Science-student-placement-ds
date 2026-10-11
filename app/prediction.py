from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

import theme

df = theme.load_data()
root = Path(__file__).resolve().parent.parent

model_path = root / "models" / "best_model.pkl"
encoder_path = root / "models" / "encoder.pkl"
scaler_path = root / "models" / "scaler.pkl"

theme.hero(
    "PLACEMENT READINESS",
    "Explore a student profile",
    "Enter the profile attributes and run the saved classifier. "
    "The result is a model estimate, not a placement guarantee.",
)

if not model_path.exists():
    st.error(f"Saved model not found: {model_path}")
    st.stop()

model = joblib.load(model_path)
encoder = joblib.load(encoder_path) if encoder_path.exists() else None
scaler = joblib.load(scaler_path) if scaler_path.exists() else None

with st.form("placement_profile"):
    st.markdown(
        "<div class='section-title'>Student profile</div>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        gender_options = (
            sorted(df["gender"].dropna().astype(str).unique())
            if "gender" in df else ["Female", "Male"]
        )
        gender = st.selectbox("Gender", gender_options)
        age = st.number_input("Age", 16, 60, 21)

        degree_options = (
            sorted(df["degree"].dropna().astype(str).unique())
            if "degree" in df else ["BE", "BTech", "BSc"]
        )
        degree = st.selectbox("Degree", degree_options)

    with c2:
        branch_options = (
            sorted(df["branch"].dropna().astype(str).unique())
            if "branch" in df else ["CS", "IT", "DS"]
        )
        branch = st.selectbox("Branch", branch_options)
        cgpa = st.number_input(
            "CGPA", min_value=0.0, max_value=10.0,
            value=8.0, step=0.1
        )
        backlogs = st.number_input(
            "Backlogs", min_value=0, max_value=30, value=0
        )

    with c3:
        internships = st.number_input(
            "Internships", min_value=0, max_value=20, value=1
        )
        certifications = st.number_input(
            "Certifications", min_value=0, max_value=50, value=2
        )
        projects = st.number_input(
            "Projects", min_value=0, max_value=30, value=2
        )

    st.markdown(
        "<div class='section-title'>Skill assessment</div>",
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        coding = st.slider("Coding skills", 0, 10, 7)

    with s2:
        communication = st.slider("Communication skills", 0, 10, 7)

    with s3:
        aptitude = st.slider("Aptitude score", 0, 100, 75)

    submitted = st.form_submit_button(
        "Analyse placement readiness",
        use_container_width=True,
    )

if submitted:
    raw = pd.DataFrame([{
        "gender": gender,
        "age": age,
        "degree": degree,
        "branch": branch,
        "cgpa": cgpa,
        "backlogs": backlogs,
        "internships": internships,
        "certifications": certifications,
        "coding_skills": coding,
        "communication_skills": communication,
        "aptitude_score": aptitude,
        "projects": projects,
    }])

    try:
        cat_cols = ["gender", "degree", "branch"]
        num_cols = [
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

        if encoder is None or scaler is None:
            st.error(
                "The saved encoder or scaler is missing. "
                "Prediction requires the preprocessing artifacts used "
                "during model training."
            )
            st.stop()

        cats = encoder.transform(raw[cat_cols])
        nums = scaler.transform(raw[num_cols])

        if hasattr(cats, "toarray"):
            cats = cats.toarray()

        prepared = np.hstack([cats, nums])

        expected = getattr(model, "n_features_in_", prepared.shape[1])

        if prepared.shape[1] != expected:
            st.error(
                f"Input has {prepared.shape[1]} processed features, "
                f"but the model expects {expected}. "
                "The encoder/scaler feature order must match the "
                "original training pipeline."
            )
            st.stop()

        prediction = int(model.predict(prepared)[0])

        probabilities = (
            model.predict_proba(prepared)[0]
            if hasattr(model, "predict_proba")
            else None
        )

        st.markdown(
            "<div class='section-title'>Prediction result</div>",
            unsafe_allow_html=True,
        )

        left, right = st.columns([1, 1.4])

        with left:
            if prediction == 1:
                st.success("Model classification: Placed")
            else:
                st.warning("Model classification: Not placed")

            if probabilities is not None:
                classes = list(model.classes_)

                if 1 in classes:
                    score = float(probabilities[classes.index(1)]) * 100

                    st.metric(
                        "Model-estimated placed probability",
                        f"{score:.1f}%",
                    )
                    st.progress(max(0, min(100, round(score))) / 100)
                else:
                    st.info(
                        "The model does not expose a probability "
                        "for the positive placement class."
                    )

        with right:
            st.markdown(
                "<div class='glass-card'>"
                "<div class='card-title'>Profile summary</div>"
                "<div class='card-copy'>"
                + "<br>".join(
                    f"<b>{key.replace('_', ' ').title()}:</b> {value}"
                    for key, value in raw.iloc[0].items()
                )
                + "</div></div>",
                unsafe_allow_html=True,
            )

        st.caption(
            "This is a model output, not an actual hiring decision. "
            "Probability estimates may not be calibrated."
        )

    except Exception as exc:
        st.error(
            "Prediction failed. Check the saved preprocessing pipeline "
            "and feature order against the original training code."
        )
        st.exception(exc)