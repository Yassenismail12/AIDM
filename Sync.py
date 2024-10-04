import requests
from PyQt5.QtCore import QTimer
from GoogleDriveAPI import download_google_sheet
def setup_auto_sync(local_file_path, sheet_url):
    timer = QTimer()
    timer.timeout.connect(lambda: sync_if_online(local_file_path, sheet_url))
    timer.start(30000)  # 30 seconds
    return timer

def sync_if_online(local_file_path, sheet_url):
    try:
        # Check for internet connection
        requests.get("https://www.google.com", timeout=5)
        # If online, download the latest version
        download_google_sheet(sheet_url, local_file_path)
    except requests.ConnectionError:
        print("No internet connection. Using local copy.")
