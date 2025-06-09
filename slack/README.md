# Slack Download Link Scraper

This folder contains a Python script to scrape and collect all download links for Slack from the official website for Windows, macOS, and Linux. The script extracts download URLs, version numbers, and platform information, and saves them in structured JSON files.

## Files
- `main.py`: The main script that scrapes the Slack website and generates the JSON files.
- `slack_all_links.json`: Output file containing all scraped download links and metadata in JSON format.
- `slack_info.json`: Output file containing structured download information for Slack.

## Requirements

Install the required dependencies:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script from the command line:

```bash
python main.py
```

- The script fetches the latest download links from the Slack website.
- Output is saved to `slack_all_links.json` and `slack_info.json` in this folder.

## Output Format
Each entry in `slack_all_links.json` contains:
- `product`: Always "slack"
- `file_name`: Name of the downloadable file (if available)
- `version`: Extracted version number
- `text`: Link text
- `url`: Direct download URL
- `platform`: Detected platform (e.g., "Windows", "macOS", "Linux")

## Notes
- The script suppresses SSL warnings for convenience.
- If the Slack website structure changes, the script may need updates.
- The script is intended for educational and automation purposes only. 