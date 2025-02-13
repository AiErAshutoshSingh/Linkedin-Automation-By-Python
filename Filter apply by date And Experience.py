from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🔧 LinkedIn Credentials
LINKEDIN_EMAIL = "aritrika.chtech@gmail.com"
LINKEDIN_PASSWORD = "Meyoucount@3"

# 🎯 Job Search Filters
SEARCH_QUERY = "Software Engineer"
LOCATION_GEOID = "103644278"  # United States
EXPERIENCE_LEVEL = "2"  # Entry Level (2), Associate (3), Mid-Senior (4), Director (5), Executive (6)
DATE_POSTED = "r86400"  # Past 24 Hours (r86400), Past Week (r604800)
JOB_TYPE = "F"  # Full-Time (F), Part-Time (P), Contract (C), Internship (I)
REMOTE_TYPE = "3"  # On-Site (1), Hybrid (2), Remote (3)

# 🚀 Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

def login():
    """Logs into LinkedIn and waits for manual verification if needed."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    # 🔑 Enter Credentials
    username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username.send_keys(LINKEDIN_EMAIL)
    password.send_keys(LINKEDIN_PASSWORD)
    password.send_keys(Keys.RETURN)

    time.sleep(3)

    # 🔍 Check for CAPTCHA
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'captcha')]"))
        )
        print("\n🔒 CAPTCHA detected! Please solve it manually in the browser.")
        input("📌 Press Enter here once you have completed the CAPTCHA...")
    except:
        print("✅ No CAPTCHA detected. Proceeding...")

    # 🚦 Check for additional verification
    if "checkpoint" in driver.current_url:
        print("\n🔒 LinkedIn requires verification (2FA or CAPTCHA).")
        input("📌 Please complete verification manually, then press Enter to continue...")

    print("✅ Logged in successfully!")

def search_jobs():
    """Navigates to LinkedIn Jobs using direct URL filtering."""
    
    # Construct the LinkedIn job search URL with multiple filters
    job_search_url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={SEARCH_QUERY.replace(' ', '%20')}"
        f"&geoId={LOCATION_GEOID}"
        f"&f_E={EXPERIENCE_LEVEL}"  # Experience Level Filter
        f"&f_TPR={DATE_POSTED}"  # Date Posted Filter
        f"&f_JT={JOB_TYPE}"  # Job Type Filter
        f"&f_WT={REMOTE_TYPE}"  # Remote Work Type
        f"&origin=JOB_SEARCH_PAGE_JOB_FILTER"
        f"&refresh=true"
    )
    
    print(f"🔍 Navigating to job search URL:\n{job_search_url}")
    
    driver.get(job_search_url)
    time.sleep(5)  # Allow the page to load

    print("✅ Job search results loaded with filters applied!")

def main():
    """Runs the LinkedIn Job Search Automation."""
    login()
    search_jobs()
    print("✅ Job search completed with filters applied.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
