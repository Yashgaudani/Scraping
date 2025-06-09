# VLC Versioned Download Link Checker

This folder contains Python scripts to check and compare download links for specific VLC versions and platforms. The scripts fetch, compare, and update JSON files with the latest download links for VLC.

## Files
- `main.py`: Script to fetch and compare download links for a specific VLC version and platform.
- `vlc.py`, `version.py`, `os.py`: Helper scripts for VLC link management and versioning.
- `vlc_3.0.21_macosx_links.json`, `vlc_3.0.21_win32_links.json`, `vlc_3.0.21_win64_links.json`, `vlc_3.0.21_links.json`, `vlc_links.json`: Output files containing download links for different VLC versions and platforms.
- `latest_version.json`: JSON file storing the latest version info.
- `requirements.txt`: Python dependencies for this folder.
- `LICENSE`: License information.

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script from the command line:

```bash
python main.py
```

- The script fetches and compares download links for the specified VLC version and platform.
- Output is saved to the corresponding JSON file in this folder.

## Notes
- The script is intended for educational and automation purposes only. 