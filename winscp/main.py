import requests
import xml.etree.ElementTree as ET
import os
import json
import re
from datetime import datetime

url = "https://sourceforge.net/p/winscp/activity/feed.rss"
response = requests.get(url)
response.raise_for_status()

root = ET.fromstring(response.text)

# Helper to parse date string and return date only (YYYY-MM-DD)
def extract_date(date_str):
    try:
        # Parse date with time, convert to date only string YYYY-MM-DD
        dt = datetime.strptime(date_str.strip(), "%a, %d %b %Y %H:%M:%S %z")
        return dt.date()
    except Exception as e:
        return None

# Step 1: Get lastBuildDate and extract date only
last_build_date_tag = root.find("./channel/lastBuildDate")
if last_build_date_tag is None:
    print("❌ lastBuildDate tag not found")
    exit()

last_build_date = extract_date(last_build_date_tag.text)
if last_build_date is None:
    print("❌ Could not parse lastBuildDate")
    exit()

# Step 2: Filter <item> by pubDate date only matching lastBuildDate date
items = root.findall(".//item")
filtered = []

for item in items:
    pub_date_str = item.findtext("pubDate", "").strip()
    pub_date = extract_date(pub_date_str)

    # Only continue if pub_date date matches last_build_date
    if pub_date != last_build_date:
        continue

    title = item.findtext("title", "").strip()
    link = item.findtext("link", "").strip()
    filename = title.split("/")[-1].strip()

    # Extract version number (e.g. 6.5.1)
    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", title)
    version = match.group(1) if match else "N/A"

    filtered.append({
        "product": "WinSCP",
        "version": version,
        "text": filename,
        "url": link,
        "platform": "Windows"
    })

# Step 3: Print and save
for entry in filtered:
    print(entry)

file_path = "/home/yash-gaudani/R%D/Vlc/winscp/winscp_patch_data.json"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=4)

print(f"✅ JSON saved to: {file_path}")
