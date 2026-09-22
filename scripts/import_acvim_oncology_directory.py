#!/usr/bin/env python3
"""Download and parse the public ACVIM/VetSpecialists US oncology directory."""
from __future__ import annotations

import html
import json
import re
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = (
    "https://www.vetspecialists.com/search-results?animals=dog&specs=Onco"
    "&country=United%20States&page=46"
)
OUTPUT = ROOT / "data" / "acvim_oncology_profiles.json"


def clean(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    return "\n".join(" ".join(line.split()) for line in value.splitlines() if line.strip())


class DirectoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.current: dict[str, str] | None = None
        self.capture: str | None = None
        self.capture_depth = 0
        self.profiles: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if tag == "div" and "vet-search-item" in classes and self.current is None:
            self.current = {"name": "", "organization": "", "address": "", "phone": "", "website": "", "profile_url": ""}
            self.depth = 1
            return
        if self.current is None:
            return
        if tag == "div":
            self.depth += 1
        field = None
        if tag == "h3":
            field = "name"
        elif tag == "strong":
            field = "organization"
        elif tag == "div" and "vsiAddr" in classes:
            field = "address"
        elif tag == "div" and "vsiPhone" in classes:
            field = "phone"
        if field:
            self.capture = field
            self.capture_depth = self.depth
        if tag == "br" and self.capture == "address":
            self.current["address"] += "\n"
        if tag == "a":
            href = values.get("href") or ""
            if "btn-vet-result" in classes:
                self.current["profile_url"] = "https://www.vetspecialists.com" + html.unescape(href)
            elif href.startswith(("http://", "https://")) and "vetspecialists.com" not in href:
                self.current["website"] = html.unescape(href)

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        if self.capture and ((tag == "h3" and self.capture == "name") or (tag == "strong" and self.capture == "organization")):
            self.capture = None
        if tag == "div":
            if self.capture and self.capture_depth == self.depth:
                self.capture = None
            self.depth -= 1
            if self.depth == 0:
                item = {key: clean(value) for key, value in self.current.items()}
                if item["name"]:
                    self.profiles.append(item)
                self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is not None and self.capture:
            self.current[self.capture] += data


def main() -> None:
    request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "VetTrialFinder/1.0 directory audit"})
    with urllib.request.urlopen(request, timeout=60) as response:
        source = response.read().decode("utf-8", errors="replace")
    match = re.search(r"Search Results,\s*([0-9,]+) items found", source)
    expected = int(match.group(1).replace(",", "")) if match else 0
    parser = DirectoryParser()
    parser.feed(source)
    assert expected and len(parser.profiles) == expected, (len(parser.profiles), expected)
    coordinates = re.findall(r"locations\.push\(\{ lat: ([+-]?[0-9.]+), lng: ([+-]?[0-9.]+)\}\);", source)
    assert len(coordinates) == expected, (len(coordinates), expected)
    for profile, (latitude, longitude) in zip(parser.profiles, coordinates):
        profile["latitude"] = float(latitude)
        profile["longitude"] = float(longitude)
    payload = {
        "source": SOURCE_URL,
        "retrieved": date.today().isoformat(),
        "profile_count": len(parser.profiles),
        "profiles": parser.profiles,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ACVIM_ONCOLOGY_PROFILES_OK profiles={len(parser.profiles)}")


if __name__ == "__main__":
    main()
