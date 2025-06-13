import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
import os

BASE_URL = "https://download.documentfoundation.org/"
OUTPUT_PATH = "/home/yash-gaudani/R%D/Vlc/LibreOffice/libreoffice_downloads.json"

# Filenames to match
TARGET_FILES = {
    "LibreOffice_25.2.4_Win_x86-64.msi": "Windows",
    "LibreOffice_25.2.4_Win_x86.msi": "Windows",
    "LibreOffice_25.2.4_Win_aarch64.msi": "Windows",
    "LibreOffice_25.2.4_MacOS_x86-64.dmg": "macOS",
    "LibreOffice_25.2.4_MacOS_aarch64.dmg": "macOS",
    "LibreOffice_25.2.4_Linux_x86-64_deb.tar.gz": "Linux"
}

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [urljoin(url, a['href']) for a in soup.find_all("a", href=True)]

def get_latest_version(version_urls):
    version_dirs = []
    for url in version_urls:
        name = url.rstrip('/').split('/')[-1]
        if re.match(r'^\d+\.\d+\.\d+$', name):
            version_dirs.append(name)
    version_dirs.sort(key=lambda s: list(map(int, s.split('.'))), reverse=True)
    return version_dirs[0] + '/'

# Step 1-3: Navigate to latest version
libreoffice_url = next(link for link in get_links(BASE_URL) if "libreoffice/" in link)
stable_url = next(link for link in get_links(libreoffice_url) if "stable/" in link)
version_links = get_links(stable_url)
latest_version = get_latest_version(version_links)
version_url = urljoin(stable_url, latest_version)
version_clean = latest_version.rstrip('/')

# Step 4-5: Traverse and filter
os_folders = [link for link in get_links(version_url) if link.rstrip('/').split('/')[-1] in ['win', 'mac', 'deb']]
results = []

for os_url in os_folders:
    arch_links = [link for link in get_links(os_url) if link.endswith('/')]
    for arch_url in arch_links:
        file_links = [link for link in get_links(arch_url) if not link.endswith('/')]
        for file_link in file_links:
            filename = file_link.split('/')[-1]
            if filename in TARGET_FILES:
                results.append({
                    "product": "LibreOffice",
                    "version": version_clean,
                    "text": filename,
                    "url": file_link,
                    "platform": TARGET_FILES[filename]
                })

# Step 6: Save to file
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ Saved {len(results)} entries to {OUTPUT_PATH}")
