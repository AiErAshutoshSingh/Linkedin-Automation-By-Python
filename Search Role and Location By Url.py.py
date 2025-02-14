from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from urllib.parse import quote

def linkedin_login(driver, wait, username, password):
    driver.get("https://www.linkedin.com/login")
    
    # Locate username and password fields
    user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    pass_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    
    # Enter credentials
    user_field.send_keys(username)
    pass_field.send_keys(password)
    pass_field.send_keys(Keys.RETURN)
    
    # Handle possible verification
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        input("Complete verification manually and press Enter to continue...")
    except:
        print("No verification detected, proceeding...")
    
    print("Logged in successfully!")

def search_people_by_location(driver, keyword, location):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(keyword)}&geoUrn=%5B%22{quote(location)}%22%5D"
    driver.get(search_url)
    time.sleep(5)  # Allow search results to load
    print("Search results loaded for", keyword, "in", location)

def send_connection_requests(driver, wait, max_requests=10, note="Hello, I would like to connect with you on LinkedIn!"):
    sent_requests = 0
    while sent_requests < max_requests:
        people = driver.find_elements(By.XPATH, "//button[contains(., 'Connect')]")
        if not people:
            print("No more connect buttons found.")
            break
        
        for button in people:
            try:
                button.click()
                time.sleep(random.uniform(2, 4))
                
                # Handle the "Add a note" popup
                try:
                    add_note_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add a note')]")))
                    add_note_button.click()
                    
                    note_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[contains(@id, 'custom-message')]")))
                    note_box.send_keys(note)
                    
                    send_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send')]")))
                    send_now_button.click()
                except:
                    print("No 'Add a note' button, sending request without note.")
                    try:
                        send_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send now')]")))
                        send_now_button.click()
                    except:
                        print("No 'Send now' button, skipping...")
                
                sent_requests += 1
                print(f"Connection request sent. Total: {sent_requests}")
                time.sleep(random.uniform(3, 6))  # Random delay to avoid detection
                
                if sent_requests >= max_requests:
                    break
            except Exception as e:
                print("Error clicking connect button:", e)
        
        # Scroll down to load more profiles
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(random.uniform(3, 5))

def main():
    # Credentials (replace with your own details)
    username = "aritrika.chtech@gmail.com"
    password = "Meyoucount@3"
    keyword = "Software Engineer"
    location = "New Zealand"
    max_requests = 10  # Set limit to avoid detection
    note = "Hello, I would like to connect with you on LinkedIn!"  # Custom note
    
    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    
    try:
        linkedin_login(driver, wait, username, password)
        search_people_by_location(driver, keyword, location)
        send_connection_requests(driver, wait, max_requests, note)
    finally:
        driver.quit()
        print("Process completed.")

if __name__ == "__main__":
    main()
