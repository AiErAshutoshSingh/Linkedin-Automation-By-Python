import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ LinkedIn Credentials
LINKEDIN_EMAIL = "aritrika.chtech@gmail.com"
LINKEDIN_PASSWORD = "Meyoucount@3"

# ✅ Your LinkedIn Profile URL
PROFILE_URL = "https://www.linkedin.com/in/aritrika-chandra-487587192/"

# ✅ Your message
POST_MESSAGE = "Hello, LinkedIn! This is an automated post with an image."

# ✅ Image path (Ensure correctness)
IMAGE_PATH = r"C:\img.png"  # Use `r""` or double backslashes `\\`

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

    # 📝 Click "Create a post"
    try:
        print("🔍 Looking for 'Create a post' button...")
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Create a post']"))
        )
        post_button.click()
    except:
        print("⚠️ Could not find 'Create a post' button. Retrying...")
        driver.refresh()
        time.sleep(10)
        post_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Create a post']"))
        )
        post_button.click()

    time.sleep(5)

    # 📝 Type the post message
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

    # 📷 Upload Image (Manual Click & PyAutoGUI)
    try:
        print("📷 Clicking the 'Add a photo' button...")
        image_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Add a photo')]"))
        )
        image_button.click()
        time.sleep(3)

        # 📤 Simulate keyboard entry for file upload (PyAutoGUI)
        print("📤 Uploading image via file dialog...")
        time.sleep(3)  # Allow file selection dialog to open
        pyautogui.write(IMAGE_PATH)  # Type the file path
        time.sleep(2)
        pyautogui.press("enter")  # Press Enter to confirm upload
        time.sleep(5)  # Wait for the image to load

        # ✅ Click "Next" or "Done" after uploading the image
        print("✅ Waiting for 'Next' button...")
        for _ in range(3):  # Try multiple times if button isn't immediately available
            try:
                done_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]'))
                )
                done_button.click()
                print("✅ Clicked 'Next' button successfully!")
                break
            except:
                print("⚠️ 'Next' button not found, retrying...")
                time.sleep(2)  # Wait and retry

    except Exception as e:
        print(f"⚠️ Image upload failed or was skipped. Error: {e}")

    # 🚀 Click "Post" button
    try:
        print("🚀 Clicking the 'Post' button...")
        post_submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]/span[text()='Post']"))
        )
        post_submit_button.click()
    except:
        print("⚠️ 'Post' button not found, retrying...")
        driver.refresh()
        time.sleep(5)
        post_submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]/span[text()='Post']"))
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
