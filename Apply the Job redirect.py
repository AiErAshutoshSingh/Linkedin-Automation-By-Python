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



def easy_apply():
    """Finds and applies to jobs with 'Easy Apply' and redirects to external applications."""
    applied_count = 0

    try:
        job_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'job-card-container')]")
        print(f"🔍 Found {len(job_cards)} jobs.")

        for job in job_cards:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", job)  # Ensure visibility
                job.click()
                time.sleep(3)  # Wait for job details to load

                # 🎯 Check for "Easy Apply"
                try:
                    easy_apply_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Easy Apply')]"))
                    )
                    driver.execute_script("arguments[0].click();", easy_apply_button)
                    time.sleep(3)
                    print("✅ Clicked 'Easy Apply'")

                    # Click "Submit Application" if available
                    try:
                        submit_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit application')]"))
                        )
                        driver.execute_script("arguments[0].click();", submit_button)
                        applied_count += 1
                        print(f"🎯 Applied to job {applied_count}")
                        time.sleep(3)
                    except:
                        print("⚠️ No 'Submit Application' button found. Skipping...")
                        continue

                except:
                    # 🔗 Check for "Apply on Company Website" button
                    try:
                        external_apply_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Apply to') and contains(@aria-label, 'on company website')]"))
                        )
                        print("🔗 Redirecting to the company website...")

                        # Open the link in a new tab
                        driver.execute_script("arguments[0].click();", external_apply_button)
                        time.sleep(5)

                        # Switch to the new tab
                        driver.switch_to.window(driver.window_handles[-1])
                        print("🌍 Redirected to external job application site.")
                        time.sleep(5)  # Give time to review

                        # Close the tab and switch back to LinkedIn
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        print("🔄 Back to LinkedIn job search.")

                    except:
                        print("❌ No apply button found. Skipping this job.")

                time.sleep(2)  # Short wait before moving to the next job

            except Exception as e:
                print(f"⚠️ Error applying to a job: {e}")

        print(f"✅ Applied to {applied_count} jobs successfully!")

    except Exception as e:
        print(f"❌ Error during Easy Apply process: {e}")

                








           





    

def main():
    """Runs the LinkedIn Job Search & Easy Apply Automation."""
    login()
    search_jobs()
    easy_apply()
    print("✅ Job search and applications completed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
