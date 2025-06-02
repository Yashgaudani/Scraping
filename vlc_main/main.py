import requests
from bs4 import BeautifulSoup
import json
import re
import urllib3

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

# Base URL
base_url = 'https://download.videolan.org/'

try:
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
            for entry in subentries:
                if '.' not in entry:
                    folder_url = f"{latest_url}{entry}/"
                    os_name = detect_os(entry)
                    try:
                        subfiles = fetch_files(folder_url)
                        for file in subfiles:
                            vlc_data["files"].append({
                                "file_name": file,
                                "download_url": f"{folder_url}{file}",
                                "os": os_name
                            })
                            file_count += 1
                    except Exception as err:
                        print(f"⚠️ Error reading folder {folder_url}: {err}")
                else:
                    # It's a file directly under latest version folder
                    vlc_data["files"].append({
                        "file_name": entry,
                        "download_url": f"{latest_url}{entry}",
                        "os": detect_os(entry)
                    })
                    file_count += 1

            with open('vlc_info.json', 'w') as json_file:
                json.dump(vlc_data, json_file, indent=2)

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
