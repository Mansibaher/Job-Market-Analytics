import pandas as pd

# Load data
df = pd.read_csv("../data/jobs_serpapi.csv")
print(f"✅ Loaded {len(df)} job listings")

# Show column names
print("\n🧠 Columns:")
print(df.columns.tolist())

# Top job titles
print("\n🔹 Top Job Titles:")
print(df['job_title'].value_counts().head(5))

# Top companies
print("\n🏢 Top Hiring Companies:")
print(df['company'].value_counts().head(5))

# Top locations
print("\n🌍 Top Locations:")
print(df['location'].value_counts().head(5))

# Platform sources
print("\n🌐 Job Platforms (via):")
print(df['via'].value_counts().head(5))
