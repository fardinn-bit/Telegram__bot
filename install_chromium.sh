#!/bin/bash

# Check if requirements.txt exists and install Python packages
if [ -f "requirements.txt" ]; then
    echo "Installing Python packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping Python package installation."
fi

# Download and extract Chromium without sudo if not already installed
if [ ! -f "chrome" ]; then
    echo "Downloading and extracting Chromium..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    ar x google-chrome-stable_current_amd64.deb
    tar --strip-components=4 -xvf data.tar.xz ./opt/google/chrome/chrome
    rm google-chrome-stable_current_amd64.deb
else
    echo "Chromium is already downloaded."
fi

# Download and install ChromeDriver if not already installed
if [ ! -f "chromedriver" ]; then
    echo "Downloading ChromeDriver..."
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
    chromedriver_version=$(cat LATEST_RELEASE)
    wget https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    rm chromedriver_linux64.zip
    chmod +x chromedriver
else
    echo "ChromeDriver is already installed."
fi

# Run the Python script
echo "Running the Python script..."
python3 your_script.py
