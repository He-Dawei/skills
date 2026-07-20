---
name: iptv
description: Use when you need IPTV channel playlists, live TV streams, electronic program guide (EPG) data, or TV channel metadata from around the world. Triggers: "IPTV channels", "live TV playlist", "watch TV online", "M3U playlist", "find channels for [country]", "electronic program guide", "TV channel database".
---

# IPTV

World's largest collection of publicly available IPTV channels. M3U playlists, EPG (electronic program guide), channel database, and REST API — all free, CC0-licensed, updated daily via GitHub Actions.

**No video files stored** — only user-submitted links to publicly available streams.

## Quick Reference

| Resource | URL |
|----------|-----|
| Main playlist (all channels) | `https://iptv-org.github.io/iptv/index.m3u` |
| Country-specific playlists | `https://iptv-org.github.io/iptv/countries/{iso2}.m3u` |
| Category playlists | `https://iptv-org.github.io/iptv/categories/{category}.m3u` |
| Language playlists | `https://iptv-org.github.io/iptv/languages/{lang}.m3u` |
| Full playlist listing | [PLAYLISTS.md](https://github.com/iptv-org/iptv/blob/master/PLAYLISTS.md) |
| EPG data | [iptv-org/epg](https://github.com/iptv-org/epg) |
| Channel database | [iptv-org/database](https://github.com/iptv-org/database) |
| API docs | [iptv-org/api](https://github.com/iptv-org/api) |
| Recommended players | [iptv-org/awesome-iptv](https://github.com/iptv-org/awesome-iptv) |

## How to Use

Paste playlist URL into any video player that supports M3U live streaming:

```
https://iptv-org.github.io/iptv/index.m3u
```

Works with: VLC, Kodi, IPTV Smarters, TiviMate, Perfect Player, OTT Navigator, and most smart TV IPTV apps.

## Playlist Types

### By Country (ISO 3166-1 alpha-2)
```
https://iptv-org.github.io/iptv/countries/cn.m3u   # China
https://iptv-org.github.io/iptv/countries/kr.m3u   # Korea
https://iptv-org.github.io/iptv/countries/jp.m3u   # Japan
https://iptv-org.github.io/iptv/countries/us.m3u   # United States
https://iptv-org.github.io/iptv/countries/uk.m3u   # United Kingdom
```

### By Category
```
https://iptv-org.github.io/iptv/categories/news.m3u
https://iptv-org.github.io/iptv/categories/sports.m3u
https://iptv-org.github.io/iptv/categories/music.m3u
https://iptv-org.github.io/iptv/categories/movies.m3u
https://iptv-org.github.io/iptv/categories/kids.m3u
```

### By Language
```
https://iptv-org.github.io/iptv/languages/zho.m3u   # Chinese
https://iptv-org.github.io/iptv/languages/kor.m3u   # Korean
https://iptv-org.github.io/iptv/languages/eng.m3u   # English
https://iptv-org.github.io/iptv/languages/jpn.m3u   # Japanese
```

## API Usage

REST API for programmatic channel queries:
```
GET https://iptv-org.github.io/api/channels.json     # All channels
GET https://iptv-org.github.io/api/channels/{id}.json # Single channel
GET https://iptv-org.github.io/api/countries.json     # Countries with channels
GET https://iptv-org.github.io/api/languages.json     # Languages with channels
GET https://iptv-org.github.io/api/categories.json    # All categories
GET https://iptv-org.github.io/api/regions.json       # Regions/subdivisions
```

Example: find all Korean news channels:
```python
import requests

# Get Korea channels
channels = requests.get("https://iptv-org.github.io/api/channels.json").json()
kr_news = [
    c for c in channels
    if c.get("country") == "KR"
    and "News" in (c.get("category") or "")
]
for ch in kr_news[:10]:
    print(ch["name"], "-", ch.get("url", "no stream"))
```

## EPG (Electronic Program Guide)

Get TV schedule data from [iptv-org/epg](https://github.com/iptv-org/epg):
```bash
git clone https://github.com/iptv-org/epg.git
# Guides organized by country/region in XMLTV format
```

EPG guides available at:
```
https://iptv-org.github.io/epg/guides/{language}/{source}.xml
```

## Building Custom Playlists

Combine with the database repo:
```bash
git clone https://github.com/iptv-org/database.git
# data/channels.csv — full channel metadata
# data/countries.csv — country codes and names
# data/categories.csv — category list
```

### Filter channels with script:
```python
import csv

with open("database/data/channels.csv") as f:
    channels = list(csv.DictReader(f))

# Filter: Korean channels with sports
kr_sports = [
    c for c in channels
    if c["country"] == "KR" and "Sports" in c["category"]
]
for ch in kr_sports:
    print(ch["name"], ch["url"])
```

## Ecosystem Repos

| Repo | Purpose |
|------|---------|
| [iptv-org/iptv](https://github.com/iptv-org/iptv) | Main playlist collection |
| [iptv-org/database](https://github.com/iptv-org/database) | Channel metadata database (CSV) |
| [iptv-org/epg](https://github.com/iptv-org/epg) | Electronic Program Guide |
| [iptv-org/api](https://github.com/iptv-org/api) | REST API for channel data |
| [iptv-org/awesome-iptv](https://github.com/iptv-org/awesome-iptv) | Curated list of IPTV resources |

## Common Mistakes

- **Expecting all streams to work forever**: Links are user-submitted and can go dead. Channels updated daily.
- **Using in commercial products**: CC0 license, but stream copyright may vary by jurisdiction. Check local laws.
- **Not filtering by country first**: Full playlist is massive (30,000+ channels). Always filter by country/category/language.
- **Assuming EPG coverage is universal**: Not all channels have EPG data. Check the epg repo for coverage.
