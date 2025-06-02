import requests
from bs4 import BeautifulSoup
import json
import os
# VLC download directory
base_url = "http://download.videolan.org/vlc"


# File to store version info in JSON format
version_file = "latest_version.json"

# Fetch and parse HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract version directories (starting with a digit)
versions = [a["href"].strip("/") for a in soup.find_all("a") if a["href"][0].isdigit()]
print(versions)

# Function to convert version string to tuple of ints for comparison
def version_key(v):
    return tuple(int(part) for part in v.split('.') if part.isdigit())

# Sort versions
versions = sorted(versions, key=version_key)


previous_version = versions[-2]
latest_version = versions[-1]

# Build URLs
previous_version_url = f"{base_url}/{previous_version}/"
latest_version_url = f"{base_url}/{latest_version}/"

print(f"Least version found: {previous_version}")
print(f"URL: {previous_version_url}")

print(f"Latest version found: {latest_version}")
print(f"URL: {latest_version_url}")

# Read stored version info from JSON file (if exists)
if os.path.exists(version_file):
    with open(version_file, "r") as f:
        stored_data = json.load(f)
else:
    stored_data = {}

stored_latest = stored_data.get("latest_version", "")
stored_least = stored_data.get("least_version", "")

# Compare latest versions and update JSON file if new version found
if not stored_latest:
    print(f"No stored latest version found. Saving current versions.")
    data_to_save = {
        "latest_version": latest_version,
        "latest_version_url": latest_version_url,
        "least_version": previous_version,
        "least_version_url": previous_version_url
    }
    with open(version_file, "w") as f:
        json.dump(data_to_save, f, indent=2)
elif version_key(latest_version) > version_key(stored_latest):
    print(f"New latest version released! Previous: {stored_latest}, New: {latest_version}")
    data_to_save = {
        "latest_version": latest_version,
        "latest_version_url": latest_version_url,
        "least_version": previous_version,
        "least_version_url": previous_version_url
    }
    with open(version_file, "w") as f:
        json.dump(data_to_save, f, indent=2)
else:
    print(f"No new latest version released. Current latest: {stored_latest}")