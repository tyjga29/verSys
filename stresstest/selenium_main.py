from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to perform the clicking action
def click_button(driver, iteration):
    print(f"Iteration {iteration}: Clicking the button...")
    # Find the button element by its XPath, CSS selector, ID, etc.
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Search Whole Database']")))
    button.click()
    print(f"Iteration {iteration}: Button clicked successfully.")

# URL of the website to stress test
website_url = "http://127.0.0.1:8000/"

# Number of times to click the button
num_clicks = 3

# Create a list to store the WebDriver instances
drivers = []

# Loop to create WebDriver instances and perform the clicking action
for i in range(num_clicks):
    print(f"\nStarting iteration {i+1}")
    # Create a WebDriver instance (make sure you have the appropriate driver installed, e.g., chromedriver for Chrome)
    driver = webdriver.Chrome()
    drivers.append(driver)
    # Navigate to the website
    driver.get(website_url)
    # Call the function to click the button
    click_button(driver, i+1)

# Close all WebDriver sessions
for driver in drivers:
    driver.quit()
