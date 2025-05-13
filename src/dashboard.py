import streamlit as st
import pandas as pd
import altair as alt

# Load data
df = pd.read_csv("../data/jobs_serpapi.csv")
skills_df = pd.read_csv("../data/skill_frequencies.csv")

st.set_page_config(page_title="Job Market Skill Trends", layout="wide")

st.title("📊 Real-Time Job Market Analytics Dashboard")
st.markdown("Explore the most in-demand tech skills from job descriptions across Data Analyst and ML Engineer roles.")

# Dropdown to filter by role
roles = df["role"].dropna().unique().tolist()
selected_role = st.selectbox("🎯 Select Job Role", roles)

# Filter jobs by role
filtered_df = df[df["role"] == selected_role]

# Recalculate skill frequency for the selected role
tracked_skills = skills_df["Skill"].tolist()
skill_counts = {skill: 0 for skill in tracked_skills}

for desc in filtered_df["description"].dropna():
    text = desc.lower()
    for skill in tracked_skills:
        if skill.lower() in text:
            skill_counts[skill] += 1

# Create DataFrame for chart
chart_df = pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"])
chart_df = chart_df.sort_values(by="Count", ascending=False)

# Bar chart
st.subheader("📌 Skill Mentions in Job Descriptions")
bar_chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X("Count:Q"),
    y=alt.Y("Skill:N", sort="-x"),
    tooltip=["Skill", "Count"]
).properties(width=700, height=400)

st.altair_chart(bar_chart, use_container_width=True)

# Job listings table
with st.expander("📝 View Job Listings"):
    st.dataframe(filtered_df[["job_title", "company", "location", "via", "description"]])

# CSV download
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Job Listings", data=csv_data, file_name="filtered_jobs.csv", mime="text/csv")
