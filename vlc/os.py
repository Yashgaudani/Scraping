import requests
from bs4 import BeautifulSoup
import json
import os

version_url = "http://download.videolan.org/vlc/3.0.21/"
json_file = "vlc_3.0.21_links.json"

response = requests.get(version_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract all <a> tags except parent directory link
links = []
for a in soup.find_all("a"):
    href = a.get("href")
    text = a.text.strip()
    if href and href != "../":  # ignore parent directory link
        # Build absolute URL
        link_url = version_url + href
        links.append({"text": text, "url": link_url})

# Save to JSON file
with open(json_file, "w") as f:
    json.dump(links, f, indent=2)

print(f"Saved {len(links)} links to {json_file}")
