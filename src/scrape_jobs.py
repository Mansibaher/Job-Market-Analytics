from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_indeed(job_title, num_pages=2):
    options = Options()
    options.add_argument("--start-maximized")  # open big browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    job_title = job_title.replace(" ", "+")
    base_url = "https://www.indeed.com/jobs?q={}&start={}"

    jobs = []

    for page in range(num_pages):
        url = base_url.format(job_title, page * 10)
        print(f"🔗 Visiting: {url}")
        driver.get(url)
        time.sleep(5)  # allow content and cookies to load

        # Optional: Click "Accept Cookies" if shown
        try:
            consent = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            consent.click()
            print("✅ Accepted cookies")
            time.sleep(2)
        except:
            pass

        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.find_all("div", class_="job_seen_beacon")
        print(f"📄 Found {len(listings)} jobs on page {page + 1}")

        for listing in listings:
            title = listing.find("h2", class_="jobTitle")
            company = listing.find("span", class_="companyName")
            location = listing.find("div", class_="companyLocation")
            salary = listing.find("div", class_="salary-snippet")
            summary = listing.find("div", class_="job-snippet")

            jobs.append({
                "job_title": title.text.strip() if title else "",
                "company": company.text.strip() if company else "",
                "location": location.text.strip() if location else "",
                "salary": salary.text.strip() if salary else "",
                "description": summary.text.strip().replace("\n", " ") if summary else ""
            })

    driver.quit()
    return pd.DataFrame(jobs)

if __name__ == "__main__":
    roles = ["Data Analyst", "Machine Learning Engineer"]
    all_jobs = pd.DataFrame()

    for role in roles:
        print(f"\n🚀 Scraping: {role}")
        df = scrape_indeed(role)
        df["role"] = role
        all_jobs = pd.concat([all_jobs, df], ignore_index=True)

    all_jobs.to_csv("../data/jobs.csv", index=False)
    print("\n✅ Data saved to data/jobs.csv")
