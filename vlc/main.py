import requests
from bs4 import BeautifulSoup
import json
import os

# url = "http://download.videolan.org/vlc/3.0.21/win64/"
# url = "http://download.videolan.org/vlc/3.0.21/win32/"
url = "http://download.videolan.org/vlc/3.0.21/macosx/"
output_file = "vlc_3.0.21_macosx_links.json"

# Step 1: Fetch current links from the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

current_links = []
for a in soup.find_all("a"):
    href = a.get("href")
    text = a.text.strip()
    if href and href != "../":
        full_url = url + href
        current_links.append({"text": text, "url": full_url})

# Step 2: Load stored links from JSON file
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        old_links = json.load(f)
else:
    old_links = []

# Step 3: Compare and update only if needed
if current_links != old_links:
    print("🔄 Endpoint has changed!")

    old_set = set((l["text"], l["url"]) for l in old_links)
    new_set = set((l["text"], l["url"]) for l in current_links)

    added = new_set - old_set
    removed = old_set - new_set

    if added:
        print("New links added:")
        for text, url in added:
            print(f" - {text}: {url}")

    if removed:
        print("Links removed:")
        for text, url in removed:
            print(f" - {text}: {url}")

    #  Update the file only when there's a change
    with open(output_file, "w") as f:
        json.dump(current_links, f, indent=2)
else:
    print("No changes in the endpoint.")