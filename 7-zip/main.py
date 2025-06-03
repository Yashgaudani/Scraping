import requests
from bs4 import BeautifulSoup
import json
import re
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://www.7-zip.org/download.html'
GITHUB_URL = 'https://github.com/ip7z/7zip/releases'

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def fetch_html(url):
    response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def fetch_files():
    soup = fetch_html(BASE_URL)
    links = soup.find_all('a')
    files = []

    for link in links:
        href = link.get('href')
        text = link.text.strip()

        if href and href.startswith('a/'):
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
    elif filename.endswith('.7z'):
        return 'Source Code'
    else:
        return 'Unknown'

def extract_version(filename):
    match = re.search(r'7z(\d{2})(\d{2})', filename)
    if match:
        major = match.group(1)
        minor = match.group(2)
        return f"{int(major)}.{int(minor)}"
    return None

def parse_version(version_text):
    # Converts "24.09" -> (24, 9) tuple for easy comparison
    parts = version_text.split('.')
    return tuple(int(p) for p in parts)

def fetch_latest_version_link():
    soup = fetch_html(GITHUB_URL)

    version_pattern = re.compile(r'^\d{1,2}\.\d{1,2}$')
    version_links = []

    for link in soup.find_all('a', href=True):
        text = link.text.strip()
        href = link['href'].strip()

        if version_pattern.match(text):
            if href.startswith('/'):
                full_url = 'https://github.com' + href
            else:
                full_url = href
            
            version_links.append({
                "text": text,
                "url": full_url,
                "parsed": parse_version(text)
            })

    if not version_links:
        return None

    # Find the max version based on parsed tuple
    latest = max(version_links, key=lambda x: x['parsed'])

    # Remove the 'parsed' key before returning
    latest_version = {
        "text": latest["text"],
        "url": latest["url"]
    }

    return latest_version

def scrape_7zip():
    all_links = []
    
    try:
        print("\n=== Scraping 7-Zip ===")
        files = fetch_files()
        version_links = fetch_latest_version_link()

        if not version_links:
            print("❌ Version links not found.")
            return

        output = {
            "name": "7-Zip",
            "latest_version": version_links['text'] or "unknown",
            "release_date": "unknown",
            "files": []
        }

        print("\nAll files found:")
        print("-" * 50)
        
        for f in files:
            filename = f['href'].split('/')[-1]
            os_name = detect_os(filename)
            download_url = BASE_URL + f['href']
            version = extract_version(filename) or version_links['text']
            
            print(f"File: {filename}")
            print(f"Text: {f['text']}")
            print(f"URL: {download_url}")
            print(f"OS: {os_name}")
            print(f"Version: {version}")
            print("-" * 50)
            
            # Store all links
            all_links.append({
                "product": "7-zip",
                "version": version,
                "text": f['text'],
                "url": download_url,
                "platform": os_name
            })
            
            output['files'].append({
                "file_name": filename,
                "text": f["text"],
                "download_url": download_url,
                "os": os_name,
                "version": version
            })

        # Save all links to a separate JSON file
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            all_links_file = os.path.join(current_dir, "7zip_all_links.json")
            
            with open(all_links_file, "w", encoding="utf-8") as f:
                json.dump(all_links, f, indent=2, ensure_ascii=False)
            
            print(f"\nSaved {len(all_links)} total links to 7zip_all_links.json")
        except Exception as e:
            print(f"Error saving all links: {str(e)}")

        # Save download files to JSON
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(current_dir, "7zip_info.json")
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print(f"\nSuccessfully saved {len(output['files'])} download files to 7zip_info.json")
            
            # Print the download files
            print("\n=== 7-Zip Download Information ===")
            print(json.dumps(output, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"Error saving JSON file: {str(e)}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    try:
        scrape_7zip()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
