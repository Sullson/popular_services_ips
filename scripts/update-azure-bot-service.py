#!/usr/bin/env python3
"""
Fetches Azure service IP ranges from Microsoft's Service Tags JSON.
Outputs plain text lists compatible with pfSense URL Table Aliases.
"""
import json
import re
import urllib.request
from ipaddress import ip_network, collapse_addresses
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

def write_list(path, ips):
    path.write_text("\n".join(ips) + "\n", newline="\n")

def aggregate_cidrs(prefixes):
    """Collapse adjacent CIDR ranges into larger blocks."""
    v4 = [ip_network(x) for x in prefixes if ":" not in x]
    v6 = [ip_network(x) for x in prefixes if ":" in x]
    v4_agg = sorted(collapse_addresses(v4), key=lambda x: x.network_address)
    v6_agg = sorted(collapse_addresses(v6), key=lambda x: x.network_address)
    return [str(x) for x in v4_agg], [str(x) for x in v6_agg]

def main():
    url = get_download_url()
    print(f"Downloading: {url}")
    with urllib.request.urlopen(url) as resp:
        data = json.load(resp)

    # Standard services (small lists, no aggregation needed)
    for tag, filename in SERVICES.items():
        entry = next((v for v in data["values"] if v["name"] == tag), None)
        if not entry:
            print(f"Warning: {tag} not found")
            continue
        ips = sorted(entry["properties"]["addressPrefixes"])
        write_list(ROOT / filename, ips)
        print(f"{tag}: {len(ips)} prefixes -> {filename}")

    # AzureCloud - aggregated and split by IP version
    cloud = next((v for v in data["values"] if v["name"] == "AzureCloud"), None)
    if cloud:
        raw = cloud["properties"]["addressPrefixes"]
        v4, v6 = aggregate_cidrs(raw)
        write_list(ROOT / "azure-cloud-v4.txt", v4)
        write_list(ROOT / "azure-cloud-v6.txt", v6)
        print(f"AzureCloud: {len(raw)} -> {len(v4)} IPv4 + {len(v6)} IPv6 (aggregated)")

if __name__ == "__main__":
    main()
