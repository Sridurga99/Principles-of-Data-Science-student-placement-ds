import streamlit as st
from datetime import date, timedelta

import theme

df = theme.load_data()

theme.hero(
    "YOUR NEXT STEPS",
    "Placement Readiness Plan",
    "Get personalized recommendations based on your current skill gaps.",
)

placed = df[df["placed"] == 1]

columns = [
    "cgpa",
    "coding_skills",
    "aptitude_score",
    "communication_skills",
    "internships",
    "certifications",
    "projects",
]

labels = {
    "cgpa": "CGPA",
    "coding_skills": "Coding skills",
    "aptitude_score": "Aptitude score",
    "communication_skills": "Communication skills",
    "internships": "Internships",
    "certifications": "Certifications",
    "projects": "Projects",
}

benchmarks = {
    column: float(placed[column].median())
    for column in columns
    if column in placed.columns
}

profile = st.session_state.get("student_profile")

tasks = {
    "coding_skills": [
        "Solve 2 array problems and 2 string problems.",
        "Practice one searching or sorting problem without looking at the solution.",
        "Solve one basic data-structure problem using stacks, queues or linked lists.",
        "Review your incorrect solutions and rewrite at least one problem correctly.",
    ],

    "aptitude_score": [
        "Solve 10 quantitative aptitude questions covering percentages, ratios and averages.",
        "Solve 10 logical reasoning questions under a time limit.",
        "Take one 20-question timed aptitude test.",
        "Review every wrong answer and write down the topic behind each mistake.",
    ],

    "cgpa": [
        "Identify the two subjects where you currently need the most improvement.",
        "Create a 7-day revision schedule for those subjects.",
        "Complete one focused revision session for each difficult subject.",
        "Review your previous mistakes and prepare questions for the next class or study session.",
    ],

    "communication_skills": [
        "Prepare and practice a 60-second self-introduction.",
        "Explain one technical concept aloud without reading from notes.",
        "Explain one of your projects in under 2 minutes.",
        "Practice answering 5 common HR interview questions.",
    ],

    "internships": [
        "Find 5 internship opportunities related to your target role.",
        "Update your resume with your strongest project and technical skills.",
        "Apply to at least 2 suitable internship opportunities.",
        "Create a short list of skills you want to gain from your next internship.",
    ],

    "certifications": [
        "Choose one certification that matches your target career role.",
        "Complete one module or learning section from the certification.",
        "Practice the skill learned in that module using a small exercise.",
        "Record the completed learning outcome so it can be added to your resume later.",
    ],

    "projects": [
        "Choose one useful feature to add to your existing project.",
        "Implement and test that feature.",
        "Update the project README with the new functionality.",
        "Prepare a 2-minute explanation of the project's problem, solution and technologies.",
    ],
}

if profile:
    rows = []

    maximums = {
        "cgpa": 10,
        "coding_skills": 10,
        "aptitude_score": 100,
        "communication_skills": 10,
        "internships": 10,
        "certifications": 10,
        "projects": 10,
    }

    for column in columns:
        if column in profile and column in benchmarks:
            current = float(profile[column])
            target = benchmarks[column]

            gap = max(0, target - current)
            gap_percentage = (gap / maximums[column]) * 100

            rows.append({
                "column": column,
                "current": current,
                "target": target,
                "gap_percentage": gap_percentage,
            })

    rows.sort(
        key=lambda item: item["gap_percentage"],
        reverse=True,
    )

    if rows:
        top = rows[0]
        focus = top["column"]

        st.markdown(
            "<div class='section-title'>Your highest priority</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-title">{labels[focus]}</div>
                <div class="card-copy">
                    Current: <b>{top["current"]:.2f}</b>
                    &nbsp; | &nbsp;
                    Placed-student median: <b>{top["target"]:.2f}</b>
                    &nbsp; | &nbsp;
                    Gap: <b>{top["gap_percentage"]:.1f}%</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='section-title'>4 things to do this week</div>",
            unsafe_allow_html=True,
        )

        for index, task in enumerate(tasks[focus], 1):
            st.markdown(
                f"""
                <div class="glass-card" style="margin-bottom:10px;
                     display:flex;gap:16px;align-items:center">
                    <div style="font-size:1.2rem;font-weight:800;
                                color:#a78bfa;min-width:30px">
                        {index}
                    </div>
                    <div class="card-copy">{task}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='section-title'>Your skill-gap priorities</div>",
            unsafe_allow_html=True,
        )

        for index, item in enumerate(rows, 1):
            st.markdown(
                f"""
                <div class="glass-card" style="margin-bottom:10px;
                     display:flex;gap:16px;align-items:center">
                    <div style="font-size:1.2rem;font-weight:800;
                                color:#a78bfa;min-width:30px">
                        {index:02d}
                    </div>
                    <div>
                        <div class="card-title">
                            {labels[item["column"]]}
                        </div>
                        <div class="card-copy">
                            Current: {item["current"]:.2f}
                            &nbsp; | &nbsp;
                            Median: {item["target"]:.2f}
                            &nbsp; | &nbsp;
                            Gap: {item["gap_percentage"]:.1f}%
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='section-title'>Build your weekly action plan</div>",
            unsafe_allow_html=True,
        )

        with st.form("weekly_plan"):
            hours = st.slider(
                "Hours available this week",
                1,
                20,
                5,
            )

            review_date = st.date_input(
                "Review date",
                value=date.today() + timedelta(days=7),
            )

            submitted = st.form_submit_button(
                "Create my plan",
                use_container_width=True,
            )

        if submitted:
            st.success(
                f"Weekly plan created for {labels[focus]}. "
                f"Allocate {hours} hour(s) before "
                f"{review_date.strftime('%d %b %Y')}."
            )

else:
    st.markdown(
        """
        <div class="notice">
            <b>No student profile found.</b><br>
            Go to Skill Gap Analysis, enter your current profile and click
            <b>Analyse my skill gaps</b>. Then return here to receive
            personalized recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "Recommendations are general guidance informed by the dataset, "
    "not guarantees of hiring outcomes."
)