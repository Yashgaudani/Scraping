import requests
from bs4 import BeautifulSoup
import json
import urllib3
import re
import os

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
    text = soup.get_text()
    match = re.search(r'FortiOS\s*([0-9]+\.[0-9]+(\.[0-9]+)?)', text)
    return match.group(1) if match else "Unknown"

def scrape_fortinet():
    # URLs
    base_url = 'https://www.fortinet.com/support/product-downloads'
    version_url = 'https://www.fortinet.com/products/fortigate/fortios'
    all_links = []
    
    try:
        print("\n=== Scraping Fortinet ===")
        files = fetch_files(base_url)
        latest_version = extract_version_from_page(version_url)
        print(f"[✔] Latest version found: {latest_version}")

        output = {
            "name": "FortiClient",
            "latest_version": latest_version,
            "files": []
        }

        print("\nAll files found:")
        print("-" * 50)
        
        for f in files:
            href = f['href']
            filename = href.split('/')[-1] if href.startswith("http") else "forticlient"
            os_name = detect_os(f['text'])
            download_url = href if href.startswith("http") else f"https://www.fortinet.com{href}"
            
            print(f"File: {filename}")
            print(f"URL: {download_url}")
            print(f"OS: {os_name}")
            print(f"Version: {latest_version}")
            print("-" * 50)
            
            # Store all links
            all_links.append({
                "product": "fortinet",
                "version": latest_version,
                "text": filename,
                "url": download_url,
                "platform": os_name
            })
            
            output['files'].append({
                "file_name": filename,
                "download_url": download_url,
                "os": os_name,
                "version": latest_version
            })

        # Save all links to a separate JSON file
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            all_links_file = os.path.join(current_dir, "fortinet_all_links.json")
            
            with open(all_links_file, "w", encoding="utf-8") as f:
                json.dump(all_links, f, indent=2, ensure_ascii=False)
            
            print(f"\nSaved {len(all_links)} total links to fortinet_all_links.json")
        except Exception as e:
            print(f"Error saving all links: {str(e)}")

        # Save download files to JSON
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(current_dir, "fortinet_info.json")
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print(f"\nSuccessfully saved {len(output['files'])} download files to fortinet_info.json")
            
            # Print the download files
            print("\n=== Fortinet Download Information ===")
            print(json.dumps(output, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"Error saving JSON file: {str(e)}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    try:
        scrape_fortinet()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
