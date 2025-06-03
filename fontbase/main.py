import requests
from bs4 import BeautifulSoup
import re
import urllib3
from urllib.parse import urljoin, urlparse
import json
import os
from fontbase.version.main import version
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

def scrape_fontbase():
    # Define sources: Windows, macOS and Linux
    sources = [
        {"url": "https://fontba.se/downloads/windows", "extensions": [".exe"]},
        {"url": "https://fontba.se/downloads/mac", "extensions": [".dmg", ".pkg"]},
        {"url": "https://fontba.se/downloads/linux", "extensions": [".deb", ".AppImage"]}
    ]
    
    all_files = []
    all_links = []
    latest_version = None
    
    try:
        print("\n=== Scraping FontBase ===")
        
        for source in sources:
            print(f"\nScraping {source['url']}...")
            fetched = fetch_files(source['url'], source['extensions'])
            
            if fetched:
                print(f"Found {len(fetched)} files")
                print("-" * 50)
                
                for file in fetched:
                    version = extract_version(file['file_name'])
                    if not latest_version:
                        latest_version = version
                    
                    print(f"File: {file['file_name']}")
                    print(f"URL: {file['download_url']}")
                    print(f"OS: {file['os']}")
                    print(f"Version: {version}")
                    print("-" * 50)
                    
                    # Store all links
                    all_links.append({
                        "product": "fontbase",
                        "version": version,
                        "text": file['file_name'],
                        "url": file['download_url'],
                        "platform": file['os']
                    })
                    
                    # Add version to file info
                    file['version'] = version
                    all_files.append(file)
        
        # Create the output structure
        output = {
            "name": "FontBase",
            "latest_version": latest_version,
            "files": all_files
        }
        
        # Save all links to a separate JSON file
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            all_links_file = os.path.join(current_dir, "fontbase_all_links.json")
            
            with open(all_links_file, "w", encoding="utf-8") as f:
                json.dump(all_links, f, indent=2, ensure_ascii=False)
            
            print(f"\nSaved {len(all_links)} total links to fontbase_all_links.json")
        except Exception as e:
            print(f"Error saving all links: {str(e)}")
        
        # Save download files to JSON
        
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    try:
        scrape_fontbase()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
