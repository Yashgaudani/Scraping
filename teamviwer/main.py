import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json

# Ask user for the TeamViewer download page URL
url = "https://www.teamviewer.com/en-in/download/portal/windows/"
# url = "https://www.teamviewer.com/en-in/download/portal/macos/"
# url = "https://www.teamviewer.com/en-in/download/portal/linux/"

# Detect platform from URL
if "linux" in url:
    platform = "Linux"
    valid_ext = [".deb", ".rpm", ".tar.xz", ".tar.gz", ".tgz"]
elif "macos" in url:
    platform = "macOS"
    valid_ext = [".dmg", ".pkg"]
elif "windows" in url:
    platform = "Windows"
    valid_ext = [".exe", ".msi"]
else:
    platform = "Unknown"
    valid_ext = []

# Send GET request
response = requests.get(url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a", href=True)

# Collect valid download links
target_links = []
for link in links:
    text = link.get_text(strip=True)
    href = urljoin(url, link["href"])
    if any(href.endswith(ext) for ext in valid_ext):
        target_links.append((text, href))

# Extract version from filename
def extract_version_from_url(href):
    filename = urlparse(href).path.split("/")[-1]
    for part in filename.replace("-", "_").split("_"):
        if any(char.isdigit() for char in part):
            return part
    return "latest"

# Build JSON result
result = []
for text, href in target_links:
    filename = urlparse(href).path.split("/")[-1]
    version = extract_version_from_url(href)
    result.append({
        "product": "TeamViewer",
        "version": version,
        "text": filename,
        "url": href,
        "platform": platform
    })

# Save output
output_file = f"/home/yash-gaudani/R%D/Vlc/teamviwer/teamviewer_downloads_{platform.lower()}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"✅ TeamViewer {platform} download links saved to '{output_file}'")
