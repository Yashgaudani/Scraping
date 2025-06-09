# VLC Download Link Scraper

This folder contains a Python script to scrape and collect all download links for VLC from the official VideoLAN download server. The script extracts download URLs, version numbers, and platform information, and saves them in structured JSON files.

## Files
- `main.py`: The main script that scrapes the VLC download server and generates the JSON files.
- `vlc_all_links.json`: Output file containing all scraped download links and metadata in JSON format.
- `vlc_info.json`: Output file containing structured download information for VLC.

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

- The script fetches the latest download links from the VLC download server.
- Output is saved to `vlc_all_links.json` and `vlc_info.json` in this folder.

## Output Format
Each entry in `vlc_all_links.json` contains:
- `product`: Always "vlc"
- `file_name`: Name of the downloadable file
- `version`: Extracted version number
- `text`: File name
- `url`: Direct download URL
- `platform`: Detected platform (e.g., "Windows 64-bit", "macOS", "Linux")

## Notes
- The script suppresses SSL warnings for convenience.
- If the VLC download server structure changes, the script may need updates.
- The script is intended for educational and automation purposes only. 