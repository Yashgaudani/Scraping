import requests
from bs4 import BeautifulSoup
import json
import re
import urllib3
import os

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constants
BASE_URL = 'https://www.7-zip.org/download.html'
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

# Detect OS based on filename
def detect_os(filename):
    filename = filename.lower()
    if 'x64' in filename:
        return 'Windows 64-bit'
    elif 'win32' in filename or 'x86' in filename:
        return 'Windows 32-bit'
    elif 'arm64' in filename:
        return 'Windows ARM64'
    elif filename.endswith('.7z') or filename.endswith('.zip'):
        return 'Source Code'
    else:
        return 'Unknown'

# Extract version number like 24.09 from filename
def extract_version(filename):
    match = re.search(r'7z(\d{2})(\d{2})', filename)
    if match:
        major = match.group(1)
        minor = match.group(2)
        return f"{int(major)}.{int(minor)}"
    return "unknown"

# Fetch and parse the HTML
def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

# Main scraping function
def scrape_7zip():
    print("🔍 Fetching HTML from 7-Zip...")
    soup = fetch_html(BASE_URL)
    links = soup.find_all('a')

    all_links = []

    for link in links:
        href = link.get('href')
        text = link.text.strip()

        if href and href.startswith('a/'):
            filename = href.split('/')[-1]
            download_url = f"https://www.7-zip.org/{href}"
            os_type = detect_os(filename)
            version = extract_version(filename)

            all_links.append({
                "product": "7-zip",
                "file_name": filename,
                "version": version,
                "text": text,
                "url": download_url,
                "platform": os_type
            })

    if not all_links:
        print("❌ No download links found. Site may have changed.")
        return

    # Save to JSON
    output_path = "/home/yash-gaudani/R%D/Vlc/7-zip/7zip_all_links.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure folder exists

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_links, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(all_links)} links to:\n{output_path}")

# Run the script
if __name__ == "__main__":
    try:
        scrape_7zip()
    except Exception as e:
        print(f"❌ Error: {e}")
