import requests
from bs4 import BeautifulSoup
import re
import json

# Target URL
url = 'https://www.ultraviewer.net/changelogs.html'

# Fetch page content
response = requests.get(url)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize result
data = None

# Find all <a> tags
for link in soup.find_all('a', href=True):
    text = link.get_text(strip=True)
    href = link['href'].strip()
    
    # Match the specific "Download here" link with version in URL
    if text == "Download here" and "UltraViewer_setup" in href:
        full_url = href if href.startswith("http") else f"https://www.ultraviewer.net/{href}"
        version_match = re.search(r'UltraViewer_setup_([\d.]+)_en\.exe', full_url)
        if version_match:
            version = version_match.group(1)
            filename = f"UltraViewer_setup_{version}_en.exe"
            data = {
                "product": "UltraViewer",
                "version": version,
                "text": filename,
                "url": full_url,
                "platform": "Windows"
            }
            break  # Stop after finding the first match

# Save to JSON file if found
if data:
    with open('ultraviewer_download.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("✅ Data saved to ultraviewer_download.json")
    print(json.dumps(data, indent=4))
else:
    print("❌ No matching download link found.")
