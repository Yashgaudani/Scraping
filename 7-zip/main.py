import requests
from bs4 import BeautifulSoup
import json
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_files(url):
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
        text = link.text.strip()
        if href and href.startswith('a/') and href.endswith('.exe'):
            files.append({
                "href": href,
                "text": text
            })
    return files

def detect_os(filename):
    filename = filename.lower()
    if 'x64' in filename:
        return 'Windows 64-bit'
    elif 'win32' in filename or 'x86' in filename:
        return 'Windows 32-bit'
    elif 'arm64' in filename:
        return 'Windows ARM64'
    else:
        return 'Windows 32-bit'

def extract_version(filename):
    # Example: '7z2409-x64.exe' -> version '24.09' (7z2409)
    match = re.search(r'7z(\d{2})(\d{2})', filename)
    if match:
        major = match.group(1)
        minor = match.group(2)
        return f"{int(major)}.{int(minor)}"
    return None

base_url = 'https://www.7-zip.org/'

try:
    files = fetch_files(base_url)

    # Use the first file's version as latest (7-zip site has one version at a time)
    latest_version = None
    if files:
        latest_version = extract_version(files[0]['href'])

    output = {
        "name": "7-zip",
        "latest_version": latest_version if latest_version else "unknown",
        "files": []
    }

    for f in files:
        filename = f['href'].split('/')[-1]
        os_name = detect_os(filename)
        output['files'].append({
            "file_name": filename,
            "download_url": base_url + f['href'],
            "os": os_name
        })

    with open('7zip_info.json', 'w') as f:
        json.dump(output, f, indent=2)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
