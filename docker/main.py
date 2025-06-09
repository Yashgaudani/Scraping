import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import re

# URLs
download_page_url = 'https://www.docker.com/products/docker-desktop/'
release_notes_url = 'https://docs.docker.com/desktop/release-notes/'

# Step 1: Scrape latest version from release notes
rel_response = requests.get(release_notes_url)
rel_response.raise_for_status()
rel_soup = BeautifulSoup(rel_response.content, 'html.parser')

# Try to find version number like '4.42.0' in headers (h2, h3, or strong)
version_pattern = re.compile(r'^(\d+\.\d+\.\d+)$')
latest_version = None

# Search h2 or h3 tags for version number text
for tag in rel_soup.find_all(['h2', 'h3']):
    text = tag.get_text(strip=True)
    if version_pattern.match(text):
        latest_version = text
        break

if not latest_version:
    latest_version = "latest"

print(f"🔍 Latest Docker Desktop version: {latest_version}")

# Step 2: Scrape download page for installer links matching keywords
response = requests.get(download_page_url)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

keywords = {
    "Download for Mac – Apple Silicon": "mac/main/arm64/Docker.dmg",
    "Download for Mac – Intel Chip": "mac/main/amd64/Docker.dmg",
    "Download for Windows – AMD64": "win/main/amd64/Docker%20Desktop%20Installer.exe",
    "Download for Windows – ARM64": "win/main/arm64/Docker%20Desktop%20Installer.exe"
}

downloads = []

for a in soup.find_all('a', href=True):
    href = a['href']
    for text, pattern in keywords.items():
        if pattern in href:
            full_url = urljoin(download_page_url, href)
            platform = "macOS" if "mac" in pattern else "Windows"
            downloads.append({
                "product": "docker-desktop",
                "version": latest_version,
                "text": text,
                "url": full_url,
                "platform": platform
            })

# Save output
output_path = "/home/yash-gaudani/R%D/Vlc/docker"
os.makedirs(output_path, exist_ok=True)
output_file = os.path.join(output_path, "docker_desktop_downloads.json")

with open(output_file, "w") as f:
    json.dump(downloads, f, indent=2)

print(f"✅ JSON file saved to: {output_file}")
