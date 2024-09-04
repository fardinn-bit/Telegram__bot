import os
import subprocess
import sys
import time
import logging

# Configure logging
logging.basicConfig(filename='jupyter_lab_runner.log', level=logging.INFO)

# Function to install required packages
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Automatically install required packages if not already installed
required_packages = ['selenium', 'webdriver-manager']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def start_jupyter():
    # Command to start Jupyter Lab (ensure you have the path set correctly)
    os.system('jupyter lab &')
    logging.info("Jupyter Lab started.")

def open_jupyter(url):
    # Set up Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # Uncomment this line to run without a GUI
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")  # Set window size if needed

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the Jupyter Lab URL
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    return driver

def create_file(driver, file_name):
    try:
        # Click on the 'New' button and create a new file
        new_button = driver.find_element(By.XPATH, "//button[contains(text(),'New')]")
        new_button.click()
        
        # Click on 'Text File' (or the file type you want)
        time.sleep(1)  # Wait for the menu to appear
        text_file_option = driver.find_element(By.XPATH, "//div[contains(text(),'Text File')]")
        text_file_option.click()

        # Wait for the new file to load and rename it
        time.sleep(2)  # Wait for the new file to load
        file_input = driver.find_element(By.XPATH, "//input[@type='text']")  # Adjust the selector if needed
        file_input.send_keys(file_name)  # Rename the file
        file_input.send_keys("\n")  # Press Enter to create the file

        logging.info(f"New file '{file_name}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating file: {e}")

def click_file(driver, file_name):
    try:
        # Find and click the desired file in Jupyter Lab
        file_link = driver.find_element(By.XPATH, f"//a[contains(text(),'{file_name}')]")  # Update file name here
        file_link.click()
        logging.info(f"File '{file_name}' clicked successfully.")
    except Exception as e:
        logging.error(f"Error clicking file: {e}")

def main():
    # Start Jupyter Lab
    start_jupyter()
    
    # Replace with your Jupyter Lab URL
    jupyter_url = input("Enter your Jupyter Lab URL (e.g., http://localhost:8888/lab): ")
    
    # Open Jupyter Lab in the browser
    driver = open_jupyter(jupyter_url)

    try:
        while True:
            # Example file name for the new file
            new_file_name = "NewFile.txt"  # Change this to your desired file name

            # Perform desired tasks
            create_file(driver, new_file_name)
            click_file(driver, new_file_name)

            # Wait for a specified interval before the next iteration
            time.sleep(60)  # Adjust this interval as necessary
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
