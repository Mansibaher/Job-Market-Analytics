import pandas as pd
import re

# Load job descriptions
df = pd.read_csv("../data/jobs_serpapi.csv")

# Define list of skills to search
skills_to_track = [
    "Python", "SQL", "Excel", "Pandas", "scikit-learn", "Tableau",
    "Power BI", "AWS", "NumPy", "Git", "Java", "R", "TensorFlow"
]

# Preprocess and scan descriptions
skill_counts = {skill: 0 for skill in skills_to_track}

for desc in df["description"].dropna():
    text = desc.lower()
    for skill in skills_to_track:
        if re.search(rf"\b{skill.lower()}\b", text):
            skill_counts[skill] += 1

# Convert to DataFrame
result = pd.DataFrame(skill_counts.items(), columns=["Skill", "Count"])
result = result.sort_values(by="Count", ascending=False)

print("📊 Skill Frequencies in Job Descriptions:\n")
print(result)

# Optionally save to CSV
result.to_csv("../data/skill_frequencies.csv", index=False)
