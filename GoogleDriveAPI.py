import requests
import pandas as pd
import os


def download_google_sheet(sheet_url, local_file_path):
    # This will download the Google Sheet as an .xlsx file
    sheet_id = sheet_url.split('/')[5]
    download_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    try:
        response = requests.get(download_url)
        response.raise_for_status()  # Check for request errors

        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded Google Sheet to {local_file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        # You can add offline handling here
