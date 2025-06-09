
import requests
from bs4 import BeautifulSoup
import re
import json

def extract_version(text):
    match = re.search(r'(\d+\.\d+\.\d+)', text)
    return match.group(1) if match else "unknown"

def detect_platform(rss_url):
    if "windows" in rss_url:
        return "Windows", ["exe", "msi", "msix"]
    elif "mac" in rss_url:
        return "macOS", ["dmg", "pkg"]
    elif "linux" in rss_url:
        return "Linux", ["deb", "rpm", "AppImage"]
    else:
        return "Unknown", []

def get_slack_release_info(rss_url):
    platform, extensions = detect_platform(rss_url)

    response = requests.get(rss_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    latest_item = soup.find("item")
    title = latest_item.find("title").text.strip()
    content_encoded = latest_item.find("content:encoded").text.strip()
    version = extract_version(title)

    urls = []
    for ext in extensions:
        urls += re.findall(rf'https://[^\s<>"]+\.{ext}', content_encoded, re.IGNORECASE)

    if platform == "Linux" and "https://snapcraft.io/slack" in content_encoded:
        urls.append("https://snapcraft.io/slack")

    results = []
    for url in urls:
        filename = url.split("/")[-1] if "snapcraft" not in url else "slack.snap"
        results.append({
            "product": "slack",
            "version": version,
            "text": filename,
            "url": url,
            "platform": platform
        })

    return results

def main():
    # rss_url = "https://slack.com/intl/en-in/release-notes/linux/rss"
    # rss_url = "https://slack.com/intl/en-in/release-notes/mac/rss"
    rss_url = "https://slack.com/intl/en-in/release-notes/windows/rss"


    result = get_slack_release_info(rss_url)

    print(json.dumps(result, indent=2))

    with open("slack_dynamic_release.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        print("\n✅ Saved to slack_dynamic_release.json")

if __name__ == "__main__":
    main()

