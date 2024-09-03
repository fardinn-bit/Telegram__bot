#!/bin/bash

# Prompt user for any URL
read -p "Enter the URL you want to keep alive: " URL

# Infinite loop to keep the session alive
while true; do
    curl -I "$URL"
    sleep 100
done
