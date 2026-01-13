# Popular Services IP Lists

Plain text IP lists for firewall rules. Updated weekly via GitHub Actions.

## Available Lists

| Service | File | Note |
|---------|------|------|
| Azure Bot Service | [`azure-bot-service.txt`](../../raw/main/azure-bot-service.txt) | ⊂ Cloud |
| Azure Connectors | [`azure-connectors.txt`](../../raw/main/azure-connectors.txt) | ⊂ Cloud |
| Azure Cloud (IPv4) | [`azure-cloud-v4.txt`](../../raw/main/azure-cloud-v4.txt) | superset |
| Azure Cloud (IPv6) | [`azure-cloud-v6.txt`](../../raw/main/azure-cloud-v6.txt) | superset |

## Format

One CIDR per line, Unix line endings. Compatible with pfSense URL Table Aliases.

```
102.133.124.8/30
2603:1000:4:402::178/125
```

## How It Works

1. GitHub Action runs every Monday at 06:00 UTC
2. Script downloads Microsoft's [Service Tags JSON](https://www.microsoft.com/en-us/download/details.aspx?id=56519)
3. Extracts and aggregates IPs (large lists collapsed to fit pfSense 3k limit)
4. Commits changes if any

## pfSense Usage

1. Firewall → Aliases → Add
2. Type: `URL Table (IPs)`
3. URL: `https://raw.githubusercontent.com/Sullson/popular_services_ips/main/azure-bot-service.txt`
4. Update Frequency: 1 day
