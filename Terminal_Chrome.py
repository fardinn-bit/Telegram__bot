import requests
import time

def main():
    # Prompt user for a URL
    url = input("Enter the URL you want to keep alive (e.g., https://www.example.com): ")

    # Validate URL input
    if not (url.startswith("http://") or url.startswith("https://")):
        print("Invalid URL format. Please start with 'http://' or 'https://'.")
        return

    refresh_time = 40  # Set refresh interval to 40 seconds

    print(f"Starting to refresh {url} every {refresh_time} seconds...")

    # Infinite loop to keep the session alive
    while True:
        try:
            # Fetch the URL
            print(f"Fetching {url} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            response = requests.get(url)
            
            # Check the response status
            if response.status_code == 200:
                print("Success: Page fetched successfully.")
            else:
                print(f"Warning: Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

        # Wait for the specified time before the next request
        time.sleep(refresh_time)

if __name__ == "__main__":
    main()
