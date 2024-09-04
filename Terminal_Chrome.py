import os
import sys
import subprocess
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "requests"])
    print("Dependencies installed.")

def download_chromium_and_chromedriver():
    if not os.path.exists("chrome"):
        print("Downloading Chromium...")
        os.system("wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        os.system("ar x google-chrome-stable_current_amd64.deb")
        os.system("tar --strip-components=4 -xvf data.tar.xz ./opt/google/chrome/chrome")
        os.system("rm google-chrome-stable_current_amd64.deb")
        print("Chromium downloaded and extracted.")
    else:
        print("Chromium already downloaded.")

    if not os.path.exists("chromedriver"):
        print("Downloading ChromeDriver...")
        os.system("wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        with open("LATEST_RELEASE", "r") as file:
            version = file.read().strip()
        os.system(f"wget -q https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip")
        os.system("unzip -q chromedriver_linux64.zip")
        os.system("chmod +x chromedriver")
        os.system("rm chromedriver_linux64.zip LATEST_RELEASE")
        print("ChromeDriver downloaded and made executable.")
    else:
        print("ChromeDriver already downloaded.")

def keep_url_alive(url, refresh_time=40):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "./chrome"

    service = Service(executable_path="./chromedriver")

    try:
        print("Initializing Chrome WebDriver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully.")
    except WebDriverException as e:
        print(f"Failed to initialize WebDriver: {e}")
        return

    print(f"Starting to refresh {url} every {refresh_time} seconds...")
    while True:
        try:
            print(f"Loading {url}...")
            driver.get(url)
            print("Page loaded successfully.")
            
            # More detailed page interaction logging
            page_title = driver.title
            print(f"Page Title: {page_title}")
            
            if "not found" in page_title.lower() or driver.page_source.lower().find("error") != -1:
                print("Warning: The page might not have loaded correctly.")
            else:
                print("The page appears to be loaded correctly.")

            print(f"Current URL: {driver.current_url}")
            print(f"Page Source Length: {len(driver.page_source)} characters")
            
            # Logging the first 100 characters of the page source for inspection
            print(f"Page Source Preview: {driver.page_source[:100]}...")

        except WebDriverException as e:
            print(f"Error fetching {url}: {e}")

        time.sleep(refresh_time)

if __name__ == "__main__":
    install_dependencies()
    download_chromium_and_chromedriver()

    url = input("Enter the URL you want to keep alive (e.g., https://www.example.com): ")
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Invalid URL format. Please start with 'http://' or 'https://'.")
        sys.exit(1)

    keep_url_alive(url)
