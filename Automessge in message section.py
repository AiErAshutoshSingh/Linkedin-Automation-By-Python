from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🔧 LinkedIn Credentials
LINKEDIN_EMAIL = "aritrika.chtech@gmail.com"
LINKEDIN_PASSWORD = "Meyoucount@3"

# 📝 Message to send
MESSAGE_TEXT = "Hey {name}, hope you're doing well! Just wanted to connect and say hi. Looking forward to networking with you!"

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
    """Automatically sends messages to LinkedIn connections."""
    driver.get("https://www.linkedin.com/messaging/")
    time.sleep(5)

    # 🔍 Find all recent chats (avoid duplicate messaging)
    chats = driver.find_elements(By.XPATH, "//li[contains(@class, 'msg-conversation-listitem')]")
    print(f"📩 Found {len(chats)} recent chats.")

    for chat in chats:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", chat)  # Ensure visibility
            chat.click()
            time.sleep(3)

            # Extract recipient's name
            try:
                name_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'msg-entity-title')]")
                recipient_name = name_element.text.strip()
            except:
                recipient_name = "there"

            # 🎯 Type message
            message_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'msg-form__contenteditable')]"))
            )
            message_box.send_keys(MESSAGE_TEXT.format(name=recipient_name))
            time.sleep(2)

            # 📤 Click send button
            send_button = driver.find_element(By.XPATH, "//button[contains(@class, 'msg-form__send-button')]")
            driver.execute_script("arguments[0].click();", send_button)
            time.sleep(3)

            print(f"✅ Message sent to {recipient_name}!")

        except Exception as e:
            print(f"⚠️ Error sending message: {e}")

    print("✅ All messages sent!")

def main():
    """Runs the LinkedIn Messaging Bot."""
    login()
    send_messages()
    print("✅ Messaging completed.")
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()
