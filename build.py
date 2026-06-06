#!/usr/bin/env python3
"""Build a combined AltStore/SideStore source from Drakonis96's scattered app sources.

Each app keeps its own repo as the source of truth (releases, icons, screenshots).
This script just fetches those sources and merges their `apps` (and `news`) into a
single source served from GitHub Pages:

    https://drakonis96.github.io/drakonis96repo/apps.json

Run `python3 build.py` after any app publishes a new version to regenerate apps.json.
"""

import json
import urllib.request

# Upstream sources, one per app, scattered across GitHub.
SOURCES = [
    "https://raw.githubusercontent.com/Drakonis96/mytrackpad/main/source.json",
    "https://raw.githubusercontent.com/Drakonis96/tesstats/main/altstore.json",
    "https://drakonis96.github.io/nautilarr/apps.json",
]

# Source-level metadata for the combined store.
SOURCE = {
    "name": "Drakonis96",
    "identifier": "com.drakonis96.source",
    "subtitle": "All of Drakonis96's apps in one place.",
    "description": (
        "The official AltStore/SideStore source for all of Drakonis96's apps. "
        "Add this source once to install and auto-update MyTrackpad, Tesstats, "
        "Nautilarr and anything new that lands here."
    ),
    "iconURL": "https://drakonis96.github.io/drakonis96repo/repologo.png",
    "website": "https://github.com/Drakonis96/drakonis96repo",
    "tintColor": "5E5CE6",
    "featuredApps": [
        "com.drakonis96.mytrackpad",
        "com.tesstats.app",
        "com.drakonis96.nautilarr",
    ],
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "drakonis96repo-build"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    apps = []
    news = []
    seen = set()

    for url in SOURCES:
        data = fetch(url)
        for app in data.get("apps", []):
            bundle_id = app.get("bundleIdentifier")
            if bundle_id in seen:
                continue
            seen.add(bundle_id)
            apps.append(app)
            print(f"  + {app.get('name')} ({bundle_id})")
        news.extend(data.get("news", []))

    combined = {**SOURCE, "apps": apps, "news": news}

    with open("apps.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"\nWrote apps.json with {len(apps)} app(s) and {len(news)} news item(s).")


if __name__ == "__main__":
    main()
