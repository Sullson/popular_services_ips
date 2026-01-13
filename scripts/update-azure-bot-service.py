#!/usr/bin/env python3
"""
Fetches Azure Bot Service IP ranges from Microsoft's Service Tags JSON.
Outputs plain text list compatible with pfSense URL Table Aliases.
"""
import json
import re
import urllib.request
from pathlib import Path

DOWNLOAD_PAGE = "https://www.microsoft.com/en-us/download/details.aspx?id=56519"
BASE_URL = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/"
SERVICE_TAG = "AzureBotService"
OUTPUT_FILE = Path(__file__).parent.parent / "azure-bot-service.txt"

def get_download_url():
    """Scrape the download page for the current JSON filename."""
    with urllib.request.urlopen(DOWNLOAD_PAGE) as resp:
        html = resp.read().decode("utf-8")
    match = re.search(r"ServiceTags_Public_\d{8}\.json", html)
    if not match:
        raise RuntimeError("Could not find ServiceTags JSON filename")
    return BASE_URL + match.group(0)

def fetch_ips(url):
    """Download JSON and extract IPs for the target service tag."""
    with urllib.request.urlopen(url) as resp:
        data = json.load(resp)
    for entry in data["values"]:
        if entry["name"] == SERVICE_TAG:
            return sorted(entry["properties"]["addressPrefixes"])
    raise RuntimeError(f"Service tag '{SERVICE_TAG}' not found")

def main():
    url = get_download_url()
    print(f"Downloading: {url}")
    ips = fetch_ips(url)
    OUTPUT_FILE.write_text("\n".join(ips) + "\n", newline="\n")
    print(f"Wrote {len(ips)} prefixes to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
