import streamlit as st
import plotly.express as px
import theme

df = theme.load_data()

theme.hero(
    "DATA WORKSPACE",
    "Dataset Explorer",
    "Inspect the cleaned dataset, filter student profiles, and export "
    "a subset for further analysis.",
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Columns", str(df.shape[1]))
c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
c4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

with st.expander("Filter the dataset", expanded=True):
    x1, x2, x3 = st.columns(3)

    status = x1.selectbox(
        "Placement status",
        ["All", "Placed", "Not placed"],
    )

    branch_options = (
        ["All"] + sorted(df["branch"].dropna().astype(str).unique().tolist())
        if "branch" in df else ["All"]
    )
    degree_options = (
        ["All"] + sorted(df["degree"].dropna().astype(str).unique().tolist())
        if "degree" in df else ["All"]
    )

    branch = x2.selectbox("Branch", branch_options)
    degree = x3.selectbox("Degree", degree_options)

    search = st.text_input(
        "Search within available values",
        placeholder="Type a branch, degree or category",
    )

filtered = df.copy()

if status == "Placed":
    filtered = filtered[filtered["placed"] == 1]
elif status == "Not placed":
    filtered = filtered[filtered["placed"] == 0]

if branch != "All" and "branch" in filtered:
    filtered = filtered[filtered["branch"].astype(str) == branch]

if degree != "All" and "degree" in filtered:
    filtered = filtered[filtered["degree"].astype(str) == degree]

if search.strip():
    mask = filtered.astype(str).apply(
        lambda column: column.str.contains(
            search.strip(), case=False, na=False
        )
    ).any(axis=1)
    filtered = filtered[mask]

st.caption(f"Showing {len(filtered):,} of {len(df):,} rows")

st.dataframe(
    filtered,
    use_container_width=True,
    height=390,
    hide_index=True,
)

st.download_button(
    "Download filtered CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="student_placement_filtered.csv",
    mime="text/csv",
)

st.markdown(
    "<div class='section-title'>Feature distribution</div>",
    unsafe_allow_html=True,
)

numeric_columns = filtered.select_dtypes(include="number").columns.tolist()

if numeric_columns:
    default_index = (
        numeric_columns.index("cgpa") if "cgpa" in numeric_columns else 0
    )

    chosen = st.selectbox(
        "Choose a numeric feature",
        numeric_columns,
        index=default_index,
    )

    fig = px.histogram(
        filtered,
        x=chosen,
        color="placed" if "placed" in filtered else None,
        barmode="overlay",
        opacity=0.78,
        nbins=30,
        color_discrete_map={0: "#8b5cf6", 1: "#67e8f9"},
        template="plotly_dark",
    )

    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Placed",
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No numeric columns are available in the current filtered data.")