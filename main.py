import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import requests
import os
import time

def get_driver(download_dir):
    # Chrome options settings
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [
            {"id": "Save as PDF", "origin": "local", "account": ""}
        ],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }
    prefs = {
        "printing.print_preview_sticky_settings.appState": json.dumps(settings),
        "savefile.default_directory": download_dir,
        "savefile.prompt_for_download": False,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.default_directory": download_dir,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--kiosk-printing")

    # Set up the Chrome service
    chrome_service = Service(ChromeDriverManager().install())

    # Launch browser with predefined settings
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

def download_article(url, download_dir):
    browser = get_driver(download_dir)
    browser.get(url)

    # Launch print and save as PDF
    browser.execute_script("window.print();")
    
    # Wait for the download to complete
    time.sleep(5)  # Adjust the sleep time if needed

    browser.quit()

def main():
    st.title("GeeksforGeeks Article Downloader")

    url = st.text_input("Enter the article URL:")

    if st.button("Download PDF"):
        # Get the current script directory
        download_dir = os.path.dirname(os.path.abspath(__file__))
        # Check if the URL is valid/reachable
        response = requests.get(url)
        if response.status_code == 200:
            try:
                download_article(url, download_dir)
                st.success(f"The article has been successfully downloaded as a PDF in {download_dir}.")
            except Exception as e:
                st.error(f"An error occurred while downloading the article: {e}")
        else:
            st.error("The provided URL is not valid or reachable. Please enter a valid URL.")

if __name__ == "__main__":
    main()
