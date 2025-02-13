import openai
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# OpenAI API Key (Replace with your own key)
openai.api_key = "your_openai_api_key"

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

# Wait until login fields are available
wait = WebDriverWait(driver, 15)

# Login to LinkedIn
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
password = wait.until(EC.presence_of_element_located((By.ID, "password")))
username.send_keys("your_email")
password.send_keys("your_password")
password.send_keys(Keys.RETURN)

# Handle verification (if any)
try:
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    input("Complete the verification and press Enter...")
    submit_button.click()
except:
    print("No verification detected, proceeding...")

print("Logged in successfully!")

# Navigate to "My Network"
driver.get("https://www.linkedin.com/mynetwork/")
time.sleep(5)

# Scroll to load more connections
for _ in range(3):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(random.uniform(2, 4))

# Load existing connection requests
try:
    sent_requests_df = pd.read_csv("sent_requests.csv")
except FileNotFoundError:
    sent_requests_df = pd.DataFrame(columns=["Name", "Profile URL", "Message", "Follow-up Sent"])

# Function to generate AI-based personalized messages
def generate_ai_message(name):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a short, friendly LinkedIn connection request message."},
            {"role": "user", "content": f"Generate a LinkedIn message for {name}."}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to send connection requests with AI-generated messages
def send_connection_requests():
    connect_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Connect')]")

    print(f"Found {len(connect_buttons)} Connect buttons.")

    for button in connect_buttons:
        try:
            # Extract recipient's name
            parent_div = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'entity-result__item')]")
            name_element = parent_div.find_element(By.XPATH, ".//span[contains(@class, 'entity-result__title-text')]")
            recipient_name = name_element.text.strip() if name_element else "there"

            button.click()
            time.sleep(random.uniform(2, 4))

            # Generate AI-based personalized message
            personalized_message = generate_ai_message(recipient_name)

            # Handle "Add a Note" popup
            try:
                add_note_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add a note')]")))
                add_note_button.click()
                time.sleep(2)

                message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']")))
                message_box.send_keys(personalized_message)
                time.sleep(2)

                send_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send')]")))
                send_now_button.click()
                print(f"Sent request to {recipient_name} with message: {personalized_message}")

            except:
                print(f"No 'Add a note' option for {recipient_name}, sending request without a message.")
                try:
                    send_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send now')]")))
                    send_now_button.click()
                    print(f"Sent request to {recipient_name} without a message.")
                except:
                    print(f"Failed to send request to {recipient_name}, skipping...")

            # Save request details
            sent_requests_df.loc[len(sent_requests_df)] = [recipient_name, "", personalized_message, "No"]
            sent_requests_df.to_csv("sent_requests.csv", index=False)

            time.sleep(random.uniform(5, 10))

        except Exception as e:
            print("Error sending request:", e)

# Function to send follow-up messages
def send_follow_up_messages():
    driver.get("https://www.linkedin.com/messaging/")
    time.sleep(5)

    for index, row in sent_requests_df.iterrows():
        if row["Follow-up Sent"] == "No":
            try:
                recipient_name = row["Name"]
                follow_up_message = f"Hi {recipient_name}, thanks for connecting! Looking forward to networking with you."

                search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search messages')]")))
                search_box.send_keys(recipient_name)
                time.sleep(3)
                search_box.send_keys(Keys.RETURN)
                time.sleep(3)

                # Find the message input field
                message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Write a message')]")))
                message_box.send_keys(follow_up_message)
                time.sleep(2)

                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send')]")))
                send_button.click()
                print(f"Sent follow-up message to {recipient_name}: {follow_up_message}")

                # Update follow-up status
                sent_requests_df.at[index, "Follow-up Sent"] = "Yes"
                sent_requests_df.to_csv("sent_requests.csv", index=False)

                time.sleep(random.uniform(5, 10))
            except:
                print(f"Failed to send follow-up to {recipient_name}")

# Run the functions
send_connection_requests()
send_follow_up_messages()

# Close browser
driver.quit()
print("All connection requests and follow-ups sent successfully!")
