import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

# Target URL
url = "https://download.anydesk.com/linux/"

# Local output path
output_path = "/home/yash-gaudani/R%D/Vlc/anydesk/anydesk_linux_downloads.json"

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Send GET request
response = requests.get(url)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract links
results = []

for link in soup.find_all("a", href=True):
    href = urljoin(url, link['href'])
    text = link.get_text(strip=True)
    if href.endswith(('.deb', '.rpm', '.tar.gz', '.xz')):
        results.append({
            "product": "anydesk",
            "version": "",  # You can add logic to extract version from filename
            "text": text,
            "url": href,
            "platform": "linux"
        })

# Write JSON to specified file
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ JSON saved to: {output_path}")
