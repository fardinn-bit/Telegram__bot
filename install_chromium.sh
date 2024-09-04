import os
import subprocess
import sys
import time

def install_requirements():
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"Installing packages from {requirements_file}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    else:
        print(f"{requirements_file} not found. Skipping package installation.")

def install_dependencies():
    # Run the bash script to install Chromium and dependencies
    bash_script = "./install_chromium.sh"
    if os.path.exists(bash_script):
        subprocess.call(['bash', bash_script])
    else:
        print(f"Error: {bash_script} not found!")

def main():
    # Install required Python packages
    install_requirements()

    # Install Chromium and its dependencies
    install_dependencies()

    url = input("Enter the URL you want to keep alive (e.g., https://www.example.com): ")

    if not (url.startswith("http://") or url.startswith("https://")):
        print("Invalid URL format. Please start with 'http://' or 'https://'.")
        return

    refresh_time = 40  # Set refresh interval to 40 seconds

    print(f"Starting to refresh {url} every {refresh_time} seconds...")

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the path to the ChromeDriver executable
    service = Service(executable_path="./chromedriver")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    while True:
        try:
            print(f"Fetching {url} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            driver.get(url)
            print("Success: Page loaded successfully.")
        except Exception as e:
            print(f"Error loading {url}: {e}")

        # Wait for the specified time before the next request
        time.sleep(refresh_time)

if __name__ == "__main__":
    main()
