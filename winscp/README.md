# WinSCP Patch Feed Scraper

This folder contains a Python script to fetch and filter the latest WinSCP patch activity from the SourceForge RSS feed. The script extracts patch information for the latest build date and saves it as a JSON file.

## Files
- `main.py`: Script that scrapes the WinSCP RSS feed and generates a JSON file of patch data.
- `winscp_patch_data.json`: Output file containing filtered patch data in JSON format.

## Requirements

Install the required dependencies:

```bash
pip install requests
```

## Usage

Run the script from the command line:

```bash
python main.py
```

- The script fetches the latest patch activity and saves it to `winscp_patch_data.json` in this folder.

## Notes
- The script is intended for educational and automation purposes only. 