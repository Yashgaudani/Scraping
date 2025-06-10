import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# URL to scrape
url = 'https://www.postman.com/downloads/'

# Send GET request
response = requests.get(url)
response.raise_for_status()

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')



print("HTML saved to 'postman_downloads_template.html'")

# Base product info
product_name = "postman"
version = "latest"

# Updated platform map: Windows and macOS (intel + arm)
platform_map = {
    "win64": "Windows",
    "osx_64": "macOS",
    "osx_arm64": "macOS"
}

results = []

# Find and filter links
for link in soup.find_all('a', href=True):
    href = link['href']
    text = link.get_text(strip=True) or f"{product_name}-{version}"

    if any(key in href for key in platform_map):
        full_url = urljoin(url, href)
        for key in platform_map:
            if key in href:
                
                entry = {
                    "product": product_name,
                    "version": version,
                    "text": text,
                    "url": full_url,
                    "platform": platform_map[key]
                }
                results.append(entry)

# Save to JSON
with open("/home/yash-gaudani/R%D/Vlc/postman/postman_download_links.json", "w") as f:
    json.dump(results, f, indent=4)

print("Filtered Postman links saved to postman_download_links.json")
