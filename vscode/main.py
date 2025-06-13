import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import re
import os

# Target URL
url = "https://code.visualstudio.com/updates"

# Output file path
output_path = "/home/yash-gaudani/R%D/Vlc/vscode/vscode_links.json"

# Fetch and parse the page
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Regex to extract version
version_pattern = re.compile(r"/(\d+\.\d+\.\d+)/")

# Platform label mapping
platform_map = {
    "x64": "win",
    "Arm64": "win",
    "Universal": "mac",
    "Intel": "mac",
    "silicon": "mac",
    "deb": "linux",
    "rpm": "linux",
    "tarball": "linux",
    "snap": "linux"
}

# Collect results
results = []

# Loop through all anchor tags
for a in soup.find_all("a", href=True):
    text = a.get_text(strip=True)
    href = urljoin(url, a['href'])

    if text in platform_map:
        version_match = version_pattern.search(href)
        version = version_match.group(1) if version_match else "unknown"
        filename = href.split("/")[-2] if href.endswith("stable") else href.split("/")[-1]

        results.append({
            "platform": platform_map[text],
            "product": "vscode",
            "version": version,
            "filename": filename,
            "url": href
        })

# Ensure directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to file
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ JSON saved to: {output_path}")
