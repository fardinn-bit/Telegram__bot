#!/bin/bash

# Download and extract Chromium without sudo
cd ~
if [ ! -f chrome ]; then
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    ar x google-chrome-stable_current_amd64.deb
    tar --strip-components=4 -xvf data.tar.xz ./opt/google/chrome/chrome
    rm google-chrome-stable_current_amd64.deb
fi

# Download and install ChromeDriver
if [ ! -f chromedriver ]; then
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
    chromedriver_version=$(cat LATEST_RELEASE)
    wget https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    rm chromedriver_linux64.zip
    chmod +x chromedriver
fi

# Install Python dependencies
pip install selenium
