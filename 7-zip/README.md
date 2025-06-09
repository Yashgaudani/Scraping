# 7-Zip Download Link Scraper

This folder contains a Python script to scrape and collect all download links for 7-Zip from the official [7-Zip downloads page](https://www.7-zip.org/download.html). The script extracts download URLs, version numbers, and platform information, and saves them in a structured JSON file.

## Files

- `main.py`: The main script that scrapes the 7-Zip website and generates the JSON file.
- `7zip_all_links.json`: Output file containing all scraped download links and metadata in JSON format.

## Requirements

Install the required dependencies (see also `vlc/requirements.txt`):

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script from the command line:

```bash
python main.py
```

- The script fetches the latest download links from the 7-Zip website.
- Output is saved to `7zip_all_links.json` in this folder.

## Output Format

Each entry in `7zip_all_links.json` contains:

- `product`: Always "7-zip"
- `file_name`: Name of the downloadable file
- `version`: Extracted version number (e.g., "24.9")
- `text`: Link text (usually "Download")
- `url`: Direct download URL
- `platform`: Detected platform (e.g., "Windows 64-bit", "Source Code")

## Example Output

```json
{
  "product": "7-zip",
  "file_name": "7z2409-x64.exe",
  "version": "24.9",
  "text": "Download",
  "url": "https://www.7-zip.org/a/7z2409-x64.exe",
  "platform": "Windows 64-bit"
}
```

## Notes

- The script suppresses SSL warnings for convenience.
- If the 7-Zip website structure changes, the script may need updates.
- The script is intended for educational and automation purposes only. 