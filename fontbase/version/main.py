import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

url = "https://fontba.se/updates"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    text = link.get_text(strip=True)
    href = link.get('href')

    if href and "Latest" in text:
        # Convert relative URL to full URL
        full_url = urljoin(url, href)

        # Extract version from the href like /updates/2.22.4
        version_match = re.search(r'/updates/([\d\.]+)', href)
        if version_match:
            version = version_match.group(1)
            print(f'Latest Version: {version}')
        else:
            print(f'Could not extract version from href: {href}')
        
        break  # Only print the first "Latest" link
