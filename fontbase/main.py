import requests
from bs4 import BeautifulSoup
import re
import urllib3
from urllib.parse import urljoin, urlparse
import json
import os

# Disable HTTPS warnings since verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_files(url, file_extensions):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    files = []
    for link in links:
        href = link.get('href')
        if href and any(href.endswith(ext) for ext in file_extensions):
            full_url = urljoin(url, href)
            file_name = os.path.basename(urlparse(full_url).path)
            files.append({
                "file_name": file_name,
                "download_url": full_url,
                "os": detect_os(file_name)
            })
    return files

def detect_os(file_name):
    file_name = file_name.lower()
    if file_name.endswith('.exe'):
        if 'x64' in file_name or 'win64' in file_name:
            return 'Windows 64-bit'
        elif 'x86' in file_name or 'win32' in file_name:
            return 'Windows X84-bit'
        elif 'arm' in file_name:
            return 'Windows ARM64'
        return 'Windows'
    elif file_name.endswith(('.dmg', '.pkg')):
        return 'macOS'
    elif file_name.endswith(('.appimage',)):
        return 'Linux'
    elif 'linux' in file_name:
        return 'Linux'
    else:
        return 'Other'


def extract_version(file_name):
    version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', file_name)
    return version_match.group(1) if version_match else "Unknown"

def generate_combined_json(app_name, sources):
    all_files = []
    latest_version = None

    for source in sources:
        fetched = fetch_files(source['url'], source['extensions'])
        if fetched:
            all_files.extend(fetched)
            if not latest_version:
                latest_version = extract_version(fetched[0]['file_name'])

    data = {
        "name": app_name,
        "latest_version": latest_version,
        "files": all_files
    }
    with open('fontbase_info.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(json.dumps(data, indent=2))
    return data

# Define sources: Windows and macOS and Linux
sources = [
    {"url": "https://fontba.se/downloads/windows", "extensions": [".exe"]},
    {"url": "https://fontba.se/downloads/mac", "extensions": [".dmg", ".pkg"]},
    {"url": "https://fontba.se/downloads/linux", "extensions": [".deb", ".AppImage"]}
]

# Call function
generate_combined_json("FontBase", sources)
