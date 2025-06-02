import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_files(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    files = []
    for link in links:
        href = link.get('href')
        text = link.text.strip()
        if href:  # No filter, collect all links
            files.append({
                "href": href,
                "text": text
            })
    return files

base_url = 'https://www.microsoft.com/en-us/edge/download'

files = fetch_files(base_url)

for file in files:
    print(f"Text: {file['text']}, Link: {file['href']}")
