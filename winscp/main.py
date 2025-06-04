import requests
import xml.etree.ElementTree as ET
import re
import json
import os

url = "https://sourceforge.net/p/winscp/activity/feed.rss"
response = requests.get(url)
response.raise_for_status()

root = ET.fromstring(response.text)

data = []

for item in root.findall(".//item"):
    title = item.find("title").text or ""
    pub_date = item.find("pubDate").text
    link = item.find("link").text

    # Extract version from title or link
    version_match = re.search(r'(\d+\.\d+(\.\d+)?)', title + " " + link)
    version = version_match.group(0) if version_match else "N/A"

    entry = {
        "product": "WinSCP",
        "version": version,
        "published_date": pub_date,
        "download_link": link,
        "os": "Windows"
    }
    data.append(entry)

# Define file path
file_path = "/home/yash/R & D/product_scrap/Vlc/winscp/winscp_patch_data.json"

# Ensure the directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Write JSON data to file
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"JSON saved to: {file_path}")
