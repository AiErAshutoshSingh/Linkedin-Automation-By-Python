from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ✅ LinkedIn Credentials (USE YOUR LOGIN DETAILS)
LINKEDIN_EMAIL = "aritrika.chtech@gmail.com"
LINKEDIN_PASSWORD = "Meyoucount@3"

# ✅ Your LinkedIn Profile URL
PROFILE_URL = "https://www.linkedin.com/in/aritrika-chandra-487587192/"

# ✅ Your message
POST_MESSAGE = "Hello, LinkedIn!"
#This is an automated post using Selenium. 🚀

#Automation #Selenium #LinkedIn


# 🚀 Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)  # Increased wait time for reliability

def login():
    """Logs into LinkedIn and waits for manual verification if needed."""
    driver.get("https://www.linkedin.com/login")
    time.sleep(5)

    # 🔑 Enter Credentials
    username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username.send_keys(LINKEDIN_EMAIL)
    password.send_keys(LINKEDIN_PASSWORD)
    password.send_keys(Keys.RETURN)

    time.sleep(5)

    # 🔍 Check for CAPTCHA or 2FA verification
    if "checkpoint" in driver.current_url:
        print("\n🔒 LinkedIn requires manual verification (CAPTCHA or 2FA).")
        input("📌 Please complete verification manually, then press Enter to continue...")

    print("✅ Logged in successfully!")

def post_message():
    """Posts a text message on LinkedIn profile."""
    driver.get(PROFILE_URL)
    time.sleep(10)  # Allow time for the page to load fully

    # 📝 Click "Create a post" on profile using the correct span-based XPath
    try:
        print("🔍 Looking for 'Create a post' button...")
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'pvs-navigation__text') and text()='Create a post']"))
        )
        post_button.click()
    except:
        print("⚠️ Could not find 'Create a post' button. Retrying after refreshing the page.")
        driver.refresh()
        time.sleep(10)
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'pvs-navigation__text') and text()='Create a post']"))
        )
        post_button.click()

    time.sleep(5)

    # 📝 Type the post message in the correct section
    try:
        print("📝 Writing the message in the post box...")
        text_area = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ql-editor') and @role='textbox']"))
        )
        text_area.click()
        text_area.send_keys(POST_MESSAGE)
    except:
        print("❌ Failed to locate the post message box. Retrying...")
        driver.refresh()
        time.sleep(10)
        text_area = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ql-editor') and @role='textbox']"))
        )
        text_area.click()
        text_area.send_keys(POST_MESSAGE)

    time.sleep(3)

    # 🚀 Click "Post" button to submit
    print("🚀 Clicking the 'Post' button...")
    post_submit_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]/span[text()='Post']")
        )
    )
    post_submit_button.click()
    time.sleep(5)

    print("✅ LinkedIn post successfully published on your profile!")

def main():
    """Runs the LinkedIn Auto-Posting Script."""
    login()
    post_message()
    print("✅ Posting completed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
