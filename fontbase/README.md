# FontBase Download Link Scraper

This folder contains a Python script to scrape and collect all download links for FontBase from the official website. The script extracts download URLs, version numbers, and platform information, and saves them in a structured JSON file.

## Files
- `main.py`: The main script that scrapes the FontBase website and generates the JSON file.
- `fontbase_all_links.json`: Output file containing all scraped download links and metadata in JSON format.

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

- The script fetches the latest download links from the FontBase website.
- Output is saved to `fontbase_all_links.json` in this folder.

## Output Format
Each entry in `fontbase_all_links.json` contains:
- `product`: Always "fontbase"
- `file_name`: Name of the downloadable file
- `version`: Extracted version number
- `text`: File name
- `url`: Direct download URL
- `platform`: Detected platform (e.g., "Windows 64-bit", "macOS", "Linux")

## Notes
- The script suppresses SSL warnings for convenience.
- If the FontBase website structure changes, the script may need updates.
- The script is intended for educational and automation purposes only. 