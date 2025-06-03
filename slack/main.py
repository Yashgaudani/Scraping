import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import re

def extract_version_from_url(url):
    # Try to extract version from URL
    version_pattern = r'(\d+\.\d+\.\d+)'
    match = re.search(version_pattern, url)
    if match:
        return match.group(1)
    return None

def scrape_slack():
    # URLs for different platforms
    urls = {
        'windows': 'https://slack.com/intl/en-in/downloads/windows',
        'mac': 'https://slack.com/intl/en-in/downloads/mac',
        'linux': 'https://slack.com/intl/en-in/downloads/linux'
    }
    
    all_files = []
    all_links = []  # Store all links
    
    # Platform versions
    platform_versions = {
        'windows': '4.44.60.0',
        'mac': '4.43.52',
        'linux': '4.43.52'
    }
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Scrape each platform
    for platform, url in urls.items():
        print(f"\n=== Scraping {platform} ===")
        try:
            # Get the webpage
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            print(f"\nAll links found on {platform} page:")
            print("-" * 50)
            
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                text = link.text.strip() or "No Text"
                
                # Extract version from URL if available
                version = extract_version_from_url(href) or platform_versions[platform]
                
                # Print all links
                print(f"Text: {text}")
                print(f"URL: {href}")
                print(f"Version: {version}")
                print("-" * 50)
                
                # Store all links
                all_links.append({
                    "product": "slack",
                    "version": version,
                    "text": text,
                    "url": href,
                    "platform": platform
                })
                
                # Process download links separately
                if any(ext in href.lower() for ext in ['.exe', '.dmg', '.deb', '.rpm', '.AppImage']):
                    # Determine OS
                    os_type = "Unknown"
                    if "windows" in href.lower() or "win" in href.lower():
                        os_type = "Windows"
                    elif "mac" in href.lower() or "osx" in href.lower():
                        os_type = "macOS"
                    elif "linux" in href.lower():
                        os_type = "Linux"
                    
                    # Add to files list
                    all_files.append({
                        "file_name": os.path.basename(href),
                        "download_url": href,
                        "os": os_type,
                        "version": version
                    })
            
        except Exception as e:
            print(f"Error scraping {platform}: {str(e)}")
    
    # Save all links to a separate JSON file
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        all_links_file = os.path.join(current_dir, "slack_all_links.json")
        
        with open(all_links_file, "w", encoding="utf-8") as f:
            json.dump(all_links, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(all_links)} total links to slack_all_links.json")
    except Exception as e:
        print(f"Error saving all links: {str(e)}")
    
    # Create the output structure for download files
    output = {
        "name": "slack",
        "versions": {
            "windows": platform_versions['windows'],
            "mac": platform_versions['mac'],
            "linux": platform_versions['linux']
        },
        "files": all_files
    }
    
    # Save download files to JSON
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, "slack_info.json")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully saved {len(all_files)} download files to slack_info.json")
        
        # Print the download files
        print("\n=== Slack Download Information ===")
        print(json.dumps(output, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")

def main():
    try:
        scrape_slack()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
