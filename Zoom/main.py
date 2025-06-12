import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

# Source article
url = "https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060407"

# Platform-specific text labels
windows_texts = [
    "Zoom Workplace desktop app for Meetings",
    "Zoom Workplace desktop app for Meetings (64-bit)",
    "Zoom Workplace desktop app for Meetings (ARM)",
    "Zoom Workplace desktop app for Meetings - MSI installer",
    "Zoom Workplace desktop app for Meetings (64-bit) - MSI installer",
    "Zoom Workplace desktop app for Meetings (ARM) - MSI installer",
    "Zoom Workplace desktop app (Windows 7)",
    "Zoom Workplace desktop app (Windows 7, 64-bit)",
    "Zoom Workplace desktop app (Windows 7, ARM)",
    "Zoom Workplace desktop app (Windows 7)(MSI installer)",
    "Zoom Workplace desktop app (Windows 7, 64-bit)(MSI installer)",
    "Zoom Workplace desktop app (Windows 7, ARM)(MSI installer)",
    "Zoom Plugin for Microsoft Outlook",
    "Zoom Plugin for Notes",
    "Zoom Plugin for Microsoft Lync",
    "Zoom Rooms app (64-bit)",
    "Zoom Rooms app (64-bit) - MSI installer",
    "Zoom Rooms Custom AV controller app"
]

mac_texts = [
    "Zoom Workplace desktop app for Meetings",
    "Zoom Workplace desktop app for Meetings (ARM)",
    "Zoom Workplace desktop app for Meetings (for IT Admins)",
    "Zoom Plugin for Microsoft Outlook",
    "Zoom Rooms app",
    "Zoom Rooms Custom AV controller app"
]

linux_texts = [
    "Zoom Workplace desktop app (32-bit)",
    "Zoom Workplace desktop app (64-bit)"
]

# Request and parse the page
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Extract embedded JSON content
script_tag = soup.find("script", {"type": "application/ld+json"})
json_data = json.loads(script_tag.string)
article_html = json_data.get("articleBody", "")
article_soup = BeautifulSoup(article_html, "html.parser")

# Helper to get version from URL
def extract_version(link):
    parts = urlparse(link).path.split('/')
    for part in parts:
        if "." in part and any(c.isdigit() for c in part):
            return part
    return "latest"

# Helper to build a result entry
def build_entry(text, link, platform):
    return {
        "product": "zoom",
        "version": extract_version(link),
        "text": text,
        "url": link,
        "platform": "None"
    }

# Extract download links
seen = set()
result = []

for a in article_soup.find_all("a", href=True):
    text = a.get_text(strip=True)
    href = urljoin(url, a["href"])

    key = (text, href)
    if key in seen:
        continue
    seen.add(key)

    if text in windows_texts:
        result.append(build_entry(text, href, "Windows"))
    elif text in mac_texts:
        result.append(build_entry(text, href, "macOS"))
    elif text in linux_texts:
        result.append(build_entry(text, href, "Linux"))

# Save to JSON
with open("/home/yash-gaudani/R%D/Vlc/Zoom/zoom_all_articials.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ All Zoom installers (Windows, macOS, Linux) saved to 'zoom_all_installers.json'")







###################################################################### json #############33#######################33


import requests
import json

# Zoom Windows download JSON endpoint
url = "https://zoom.us/rest/download?os=win"
url = "https://zoom.us/rest/download?os=mac"
url = "https://zoom.us/rest/download?os=linux"

# Send GET request
response = requests.get(url)
response.raise_for_status()

# Parse JSON response
data = response.json()

# Save to file
with open("/home/yash-gaudani/R%D/Vlc/Zoom/zoom_api_download.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Zoom Windows download data saved to 'zoom_windows_download.json'")
