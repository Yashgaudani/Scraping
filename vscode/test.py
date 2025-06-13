import requests
from bs4 import BeautifulSoup
import json
import os
import re

# Save path and target version from filename
SAVE_PATH = "/home/yash-gaudani/R%D/Vlc/vscode/vscode_links_micro.json"

# Fetch page
url = "https://stealthpuppy.com/apptracker/apps/m/microsoftvisualstudiocode/"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Parse table
table = soup.find("table")
data = []

for row in table.find("tbody").find_all("tr"):
    cols = row.find_all("td")
    if len(cols) >= 6:
        link_tag = cols[5].find("a")
        if not link_tag:
            continue

        filename = link_tag.text.strip()
        url_link = link_tag['href']

        # Extract version from filename using regex
        version_match = re.search(r'(\d+\.\d+\.\d+)', filename)
        if not version_match:
            continue
        version = version_match.group(1)

        # Guess platform
        if "win" in filename:
            platform = "win"
        elif "linux" in filename:
            platform = "linux"
        elif "darwin" in filename or "mac" in filename:
            platform = "mac"
        else:
            platform = "unknown"

        data.append({
            "platform": platform,
            "product": "vscode",
            "version": version,
            "filename": filename,
            "url": url_link
        })

# Save JSON
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
with open(SAVE_PATH, "w") as f:
    json.dump(data, f, indent=4)

print(f"✅ JSON saved to: {SAVE_PATH}")
