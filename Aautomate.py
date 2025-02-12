from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import pandas as pd
from datetime import datetime

class LinkedInConnector:
    def __init__(self, email, password):
        """Initialize LinkedIn automation with login credentials."""
        self.email = email
        self.password = password
        self.driver = None
        self.connection_stats = {
            'attempted': 0,
            'successful': 0,
            'failed': 0
        }
        
    def setup_driver(self):
        """Set up and configure Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        # Remove this line if you want to see the browser in action
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        
    def login(self):
        """Log in to LinkedIn."""
        try:
            self.driver.get('https://www.linkedin.com/login')
            
            # Wait for and enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login button
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Wait for login to complete
            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def search_people(self, search_query, max_pages=3):
        """Search for people based on search query."""
        try:
            # Encode the search query for URL
            encoded_query = search_query.replace(' ', '%20')
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}"
            self.driver.get(search_url)
            
            profiles_processed = []
            
            for page in range(max_pages):
                # Wait for profile cards to load
                time.sleep(random.uniform(3, 5))
                
                # Get all profile cards on current page
                profile_cards = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "li.reusable-search__result-container"
                )
                
                for card in profile_cards:
                    try:
                        profile_data = self.process_profile(card)
                        if profile_data:
                            profiles_processed.append(profile_data)
                    except Exception as e:
                        print(f"Error processing profile: {str(e)}")
                        continue
                
                # Try to click next page button
                try:
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        "button.artdeco-pagination__button--next"
                    )
                    if "disabled" in next_button.get_attribute("class"):
                        break
                    next_button.click()
                    time.sleep(random.uniform(3, 5))
                except NoSuchElementException:
                    break
                    
            return profiles_processed
            
        except Exception as e:
            print(f"Error during people search: {str(e)}")
            return []
    
    def process_profile(self, card):
        """Process a single profile card and send connection request."""
        try:
            # Get profile name and title
            name = card.find_element(By.CSS_SELECTOR, "span.entity-result__title-text").text.strip()
            title = card.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text.strip()
            
            # Look for the Connect button
            connect_button = None
            buttons = card.find_elements(By.CSS_SELECTOR, "button")
            
            for button in buttons:
                if "Connect" in button.text:
                    connect_button = button
                    break
            
            connection_status = "Not attempted"
            
            if connect_button:
                # Random delay before clicking
                time.sleep(random.uniform(1, 3))
                
                # Click connect button
                connect_button.click()
                self.connection_stats['attempted'] += 1
                
                # Wait for the send button in the modal
                try:
                    send_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Send now']"))
                    )
                    
                    # Optional: Add a note (uncomment if needed)
                    # add_note_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Add a note']")
                    # add_note_button.click()
                    # note_field = self.driver.find_element(By.CSS_SELECTOR, "textarea#custom-message")
                    # note_field.send_keys("Hi! I'd love to connect and share insights about our industry.")
                    
                    # Random delay before sending
                    time.sleep(random.uniform(1, 2))
                    send_button.click()
                    
                    connection_status = "Request sent"
                    self.connection_stats['successful'] += 1
                    
                except TimeoutException:
                    connection_status = "Failed to send request"
                    self.connection_stats['failed'] += 1
            else:
                connection_status = "No connect button found"
            
            return {
                "name": name,
                "title": title,
                "connection_status": connection_status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"Error processing profile: {str(e)}")
            return None
    
    def save_results(self, profiles, filename="connection_attempts.csv"):
        """Save connection attempts to CSV file."""
        df = pd.DataFrame(profiles)
        df.to_csv(filename, index=False)
        print(f"\nConnection Statistics:")
        print(f"Attempted: {self.connection_stats['attempted']}")
        print(f"Successful: {self.connection_stats['successful']}")
        print(f"Failed: {self.connection_stats['failed']}")
    
    def close(self):
        """Close the web driver."""
        if self.driver:
            self.driver.quit()

def main():
    # Initialize connector with your LinkedIn credentials
    connector = LinkedInConnector(
        email="1ashutoshsingh2022@gmail.com",
        password="7849878869As!@#"
    )
    
    try:
        # Setup and login
        connector.setup_driver()
        if connector.login():
            # Search for people and send connection requests
            search_queries = [
                "python developer",
                "data scientist", "ceo", "cto", "cfo",  
                # Add more search queries as needed
            ]
            
            all_profiles = []
            for query in search_queries:
                print(f"\nProcessing search query: {query}")
                profiles = connector.search_people(query, max_pages=2)
                all_profiles.extend(profiles)
                
                # Add a random delay between searches
                time.sleep(random.uniform(5, 10))
            
            # Save results
            connector.save_results(all_profiles)
            
    finally:
        connector.close()

if __name__ == "__main__":
    main()