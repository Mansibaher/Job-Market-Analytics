from serpapi import GoogleSearch
import pandas as pd

def fetch_jobs(query, location="United States", num_results=20):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": "bba9162424df02753baeea17cbc6fb50ab181b5d55fff55d40917726f242d77a",
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # 🔍 DEBUG PRINT: Show API result structure
    print(f"\n📦 Raw API results for '{query}':")
    print(results)

    job_data = []
    for job in results.get("jobs_results", []):
        job_data.append({
            "job_title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "location": job.get("location", ""),
            "via": job.get("via", ""),
            "description": job.get("description", ""),
            "extensions": job.get("detected_extensions", {}),
        })

    return pd.DataFrame(job_data)

if __name__ == "__main__":
    roles = ["Data Analyst", "Machine Learning Engineer"]
    all_jobs = pd.DataFrame()

    for role in roles:
        print(f"\n🔍 Fetching: {role}")
        df = fetch_jobs(role)
        print(f"📊 Retrieved {len(df)} job listings for: {role}")
        df["role"] = role
        all_jobs = pd.concat([all_jobs, df], ignore_index=True)

    all_jobs.to_csv("../data/jobs_serpapi.csv", index=False)
    print("\n✅ Saved to data/jobs_serpapi.csv")
