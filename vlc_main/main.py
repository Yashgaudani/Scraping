import requests
from bs4 import BeautifulSoup
import json
import re
import urllib3
import os

# Disable HTTPS warnings since verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_files(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    files = []
    for link in links:
        href = link.get('href')
        if href and href != '../':
            files.append(href.strip('/'))
    return files

def get_latest_version(versions):
    version_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')
    version_list = [v for v in versions if version_pattern.match(v)]
    if not version_list:
        return None
    version_list.sort(key=lambda s: tuple(map(int, s.split('.'))))
    return version_list[-1]

def detect_os(folder_name):
    folder_name = folder_name.lower()
    if 'win32' in folder_name:
        return 'Windows 32-bit'
    elif 'win64' in folder_name:
        return 'Windows 64-bit'
    elif 'win' in folder_name:
        # fallback if just "win"
        return 'Windows (Unknown Arch)'
    elif 'mac' in folder_name:
        return 'macOS'
    elif 'linux' in folder_name:
        return 'Linux'
    else:
        return 'Other'

def scrape_vlc():
    # Base URL
    base_url = 'https://download.videolan.org/'
    all_links = []
    
    try:
        print("\n=== Scraping VLC ===")
        top_level = fetch_files(base_url)
        
        if 'vlc' in top_level:
            print("[✔] 'vlc/' folder found.")
            vlc_url = base_url + 'vlc/'
            name = 'vlc'
            versions = fetch_files(vlc_url)
            latest_version = get_latest_version(versions)

            if latest_version:
                latest_url = f"{vlc_url}{latest_version}/"
                print(f"[✔] Latest version found: {latest_version}")
                print(f"➡️ Latest VLC URL: {latest_url}")

                vlc_data = {
                    "name": name,
                    "latest_version": latest_version,
                    "files": []
                }

                subentries = fetch_files(latest_url)
                file_count = 0
                
                print("\nAll files found:")
                print("-" * 50)
                
                for entry in subentries:
                    if '.' not in entry:
                        folder_url = f"{latest_url}{entry}/"
                        os_name = detect_os(entry)
                        try:
                            subfiles = fetch_files(folder_url)
                            for file in subfiles:
                                file_url = f"{folder_url}{file}"
                                print(f"File: {file}")
                                print(f"URL: {file_url}")
                                print(f"OS: {os_name}")
                                print(f"Version: {latest_version}")
                                print("-" * 50)
                                
                                # Store all links
                                all_links.append({
                                    "product": "vlc",
                                    "version": latest_version,
                                    "text": file,
                                    "url": file_url,
                                    "platform": os_name
                                })
                                
                                vlc_data["files"].append({
                                    "file_name": file,
                                    "download_url": file_url,
                                    "os": os_name,
                                    "version": latest_version
                                })
                                file_count += 1
                        except Exception as err:
                            print(f"⚠️ Error reading folder {folder_url}: {err}")
                    else:
                        # It's a file directly under latest version folder
                        file_url = f"{latest_url}{entry}"
                        os_name = detect_os(entry)
                        
                        print(f"File: {entry}")
                        print(f"URL: {file_url}")
                        print(f"OS: {os_name}")
                        print(f"Version: {latest_version}")
                        print("-" * 50)
                        
                        # Store all links
                        all_links.append({
                            "product": "vlc",
                            "version": latest_version,
                            "text": entry,
                            "url": file_url,
                            "platform": os_name
                        })
                        
                        vlc_data["files"].append({
                            "file_name": entry,
                            "download_url": file_url,
                            "os": os_name,
                            "version": latest_version
                        })
                        file_count += 1

                # Save all links to a separate JSON file
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    all_links_file = os.path.join(current_dir, "vlc_all_links.json")
                    
                    with open(all_links_file, "w", encoding="utf-8") as f:
                        json.dump(all_links, f, indent=2, ensure_ascii=False)
                    
                    print(f"\nSaved {len(all_links)} total links to vlc_all_links.json")
                except Exception as e:
                    print(f"Error saving all links: {str(e)}")

                # Save download files to JSON
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    output_file = os.path.join(current_dir, "vlc_info.json")
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(vlc_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"\nSuccessfully saved {len(vlc_data['files'])} download files to vlc_info.json")
                    
                    # Print the download files
                    print("\n=== VLC Download Information ===")
                    print(json.dumps(vlc_data, indent=2, ensure_ascii=False))
                    
                except Exception as e:
                    print(f"Error saving JSON file: {str(e)}")

                if file_count > 0:
                    print("Successfully fetched data")
                else:
                    print("No files found to fetch.")
            else:
                print("No valid versions found.")
        else:
            print("'vlc/' folder not found.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def main():
    try:
        scrape_vlc()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
