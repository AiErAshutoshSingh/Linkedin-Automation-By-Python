from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random  # Import random module for delay

# 🔧 LinkedIn Credentials
LINKEDIN_EMAIL = "aritrika.chtech@gmail.com"
LINKEDIN_PASSWORD = "Meyoucount@3"

# 📝 List of Recipients & Message
RECIPIENT_NAMES = ["Manish Rawat"]  # Add more names as needed
MESSAGE_TEXT = "Hey {name}, hope you're doing well! Looking forward to networking with you!"

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

def send_messages():
    """Searches for multiple recipients in LinkedIn messages, waits 3-5 minutes, then sends messages."""
    driver.get("https://www.linkedin.com/messaging/")
    time.sleep(5)

    for recipient in RECIPIENT_NAMES:
        try:
            # 🔍 Search for the recipient in messages
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search-conversations"))
            )
            search_box.clear()
            search_box.send_keys(recipient)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)

            print(f"🔍 Searching for {recipient} in messages...")

            # Click on the first search result
            chat = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'msg-conversation-listitem')]"))
            )
            driver.execute_script("arguments[0].click();", chat)
            time.sleep(3)

            # 🕒 Random wait time (3-5 minutes) before sending the message
            wait_time = random.randint(180, 300)  # 180s to 300s (3-5 min)
            print(f"⏳ Waiting {wait_time // 60} minutes before messaging {recipient}...")
            time.sleep(wait_time)

            # 🎯 Type the message
            message_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'msg-form__contenteditable')]"))
            )
            message_box.send_keys(MESSAGE_TEXT.format(name=recipient))
            time.sleep(2)

            # 📤 Click send button
            send_button = driver.find_element(By.XPATH, "//button[contains(@class, 'msg-form__send-button')]")
            driver.execute_script("arguments[0].click();", send_button)
            time.sleep(3)

            print(f"✅ Message sent to {recipient}!")

        except Exception as e:
            print(f"❌ Error sending message to {recipient}: {e}")

    print("✅ All messages sent!")

def main():
    """Runs the LinkedIn Messaging Bot for multiple recipients with a random delay."""
    login()
    send_messages()
    print("✅ Messaging completed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
