import requests
from bs4 import BeautifulSoup
import json
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def fetch_files(url):
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    files = []
    for link in links:
        href = link.get('href')
        text = link.get_text(strip=True)
        if href and any(keyword in href.lower() for keyword in ['forticlient', 'fabricagent', 'play.google', 'apple.com', '/support/product-downloads/linux']):
            files.append({
                "href": href,
                "text": text
            })
    return files

def detect_os(text):
    text = text.lower()
    if 'windows' in text and 'arm' in text:
        return 'Windows ARM64'
    elif 'windows' in text and ('64' in text or 'x64' in text):
        return 'Windows 64-bit'
    elif 'windows' in text:
        return 'Windows'
    elif 'mac' in text or 'macos' in text:
        return 'MacOS'
    elif 'android' in text:
        return 'Android'
    elif 'ios' in text:
        return 'iOS'
    elif 'linux' in text:
        return 'Linux'
    else:
        return 'Unknown'

def extract_version_from_page(url):
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    match = re.search(r'FortiOS\s*([0-9]+\.[0-9]+(\.[0-9]+)?)', text)
    return match.group(1) if match else "Unknown"

# URLs
base_url = 'https://www.fortinet.com/support/product-downloads'
version_url = 'https://www.fortinet.com/products/fortigate/fortios'

try:
    files = fetch_files(base_url)
    latest_version = extract_version_from_page(version_url)
    print(f"Latest version found: {latest_version}")

    output = {
        "name": "FortiClient",
        "latest_version": latest_version,
        "files": []
    }

    for f in files:
        href = f['href']
        filename = href.split('/')[-1] if href.startswith("http") else "forticlient"
        os_name = detect_os(f['text'])
        download_url = href if href.startswith("http") else f"https://www.fortinet.com{href}"

        output['files'].append({
            "file_name": filename,
            "download_url": download_url,
            "os": os_name
        })

    with open('forticlient_info.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("Saved to forticlient_info.json")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
