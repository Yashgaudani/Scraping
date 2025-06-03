import requests
import xml.etree.ElementTree as ET
import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

def extract_version(title: str) -> str:
    """
    Extract version number from Slack update title.
    
    Args:
        title (str): The title text containing version information
        
    Returns:
        str: Extracted version number or "Unknown"
    """
    # Common patterns for Slack version numbers
    patterns = [
        r'(\d+\.\d+(?:\.\d+)?)',  # Standard version (e.g., 4.36.0)
        r'Version\s+(\d+\.\d+(?:\.\d+)?)',  # Version X.X.X
        r'v(\d+\.\d+(?:\.\d+)?)'  # vX.X.X
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(1)
    return "Unknown"

def fetch_slack_updates(platform: str = "macos") -> Optional[List[Dict]]:
    """
    Fetch Slack release notes from RSS feed for the specified platform.
    
    Args:
        platform (str): Platform to fetch updates for ('macos' or 'windows')
        
    Returns:
        Optional[List[Dict]]: List of updates or None if there's an error
    """
    try:
        # Construct URL based on platform
        url = f"https://slack.com/intl/en-in/release-notes/{platform}/rss"
        
        # Fetch the RSS feed
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Namespace for content:encoded
        namespaces = {'content': 'http://purl.org/rss/1.0/modules/content/'}
        
        # Extract items
        items = []
        latest_version = None
        
        for item in root.findall("./channel/item"):
            title = item.findtext("title")
            link = item.findtext("link")
            pub_date = item.findtext("pubDate")
            content_encoded = item.find("content:encoded", namespaces).text
            
            # Extract version from title
            version = extract_version(title)
            
            # Update latest version if this is the first item or newer version
            if not latest_version or version > latest_version:
                latest_version = version
            
            # Extract all http/https links using regex
            links = re.findall(r"https?://[^\s\"<>]+", content_encoded)
            
            items.append({
                "title": title,
                "link": link,
                "version": version,
                "publication_date": pub_date,
                "content": links
            })
            
        return items, latest_version
        
    except requests.RequestException as e:
        print(f"❌ Error fetching Slack updates: {str(e)}")
        return None, None
    except ET.ParseError as e:
        print(f"❌ Error parsing XML: {str(e)}")
        return None, None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None, None

def save_slack_info(updates: List[Dict], platform: str, latest_version: str) -> bool:
    """
    Save Slack updates to a JSON file.
    
    Args:
        updates (List[Dict]): List of updates to save
        platform (str): Platform name for the filename
        latest_version (str): Latest version number
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Prepare the data structure
        data = {
            "product": "Slack",
            "platform": platform,
            "latest_version": latest_version,
            "last_updated": datetime.now().isoformat(),
            "updates": updates
        }
        
        # Save to JSON file
        output_file = os.path.join("output", f"slack_updates_{platform}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Data has been saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving Slack updates: {str(e)}")
        return False

def scrape_slack() -> bool:
    """
    Main function to scrape Slack updates for both macOS and Windows.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("\n=== Scraping Slack Updates ===")
    
    success = True
    for platform in ["macos", "windows"]:
        print(f"\nFetching {platform} updates...")
        updates, latest_version = fetch_slack_updates(platform)
        
        if updates:
            if not save_slack_info(updates, platform, latest_version):
                success = False
        else:
            success = False
            
    return success

if __name__ == "__main__":
    scrape_slack()
