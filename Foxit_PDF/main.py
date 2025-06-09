import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



# Define the URL to scrape
url = 'https://cdn01.foxitsoftware.com/product/phantomPDF/desktop/win/2025.1.0/tools/'

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Ensure we got a successful response

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the links and their text
links = []

# Iterate over all anchor tags to extract href and text
for link in soup.find_all('a', href=True):
    href = link['href']
    link_text = link.get_text(strip=True)
    full_url = urljoin(url, href)  # Handle relative URLs
    links.append((link_text, full_url))

# Output the collected links
for text, link in links:
    print(f"Text: {text}\nLink: {link}\n")
