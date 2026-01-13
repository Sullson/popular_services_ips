#!/usr/bin/env python3
"""
Fetches Azure service IP ranges from Microsoft's Service Tags JSON.
Outputs plain text lists compatible with pfSense URL Table Aliases.
"""
import json
import re
import urllib.request
from pathlib import Path

DOWNLOAD_PAGE = "https://www.microsoft.com/en-us/download/details.aspx?id=56519"
BASE_URL = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/"
ROOT = Path(__file__).parent.parent

SERVICES = {
    "AzureBotService": "azure-bot-service.txt",
    "AzureConnectors": "azure-connectors.txt",
}

def get_download_url():
    with urllib.request.urlopen(DOWNLOAD_PAGE) as resp:
        html = resp.read().decode("utf-8")
    match = re.search(r"ServiceTags_Public_\d{8}\.json", html)
    if not match:
        raise RuntimeError("Could not find ServiceTags JSON filename")
    return BASE_URL + match.group(0)

def main():
    url = get_download_url()
    print(f"Downloading: {url}")
    with urllib.request.urlopen(url) as resp:
        data = json.load(resp)

    for tag, filename in SERVICES.items():
        entry = next((v for v in data["values"] if v["name"] == tag), None)
        if not entry:
            print(f"Warning: {tag} not found")
            continue
        ips = sorted(entry["properties"]["addressPrefixes"])
        out = ROOT / filename
        out.write_text("\n".join(ips) + "\n", newline="\n")
        print(f"{tag}: {len(ips)} prefixes -> {filename}")

if __name__ == "__main__":
    main()
