"""Inventory links from a saved official roster. This command makes no requests."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit


class RosterLinks(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.links = {}
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.handle_endtag("a")
            attributes = dict(attrs)
            href = (attributes.get("href") or "").strip()
            if href and not href.startswith("#"):
                try:
                    url = urldefrag(urljoin(self.base, href)).url
                    parts = urlsplit(url)
                except ValueError:
                    return
                if parts.scheme in {"http", "https"} and parts.hostname and not parts.username:
                    self.anchor = (url, [attributes.get("aria-label") or attributes.get("title") or "", " "])
        elif tag == "img" and self.anchor:
            self.anchor[1].append(dict(attrs).get("alt") or "")

    def handle_data(self, data):
        if self.anchor:
            self.anchor[1].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor:
            url, words = self.anchor
            label = " ".join("".join(words).split())
            labels = self.links.setdefault(url, [])
            if label and label not in labels:
                labels.append(label)
            self.anchor = None

    def close(self):
        super().close()
        self.handle_endtag("a")


def roster_links(html, base):
    parser = RosterLinks(base)
    parser.feed(html)
    parser.close()
    return [{"url": url, "labels": labels} for url, labels in parser.links.items()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--url", required=True, help="Actual final URL of the saved official page")
    args = parser.parse_args()
    print(json.dumps(roster_links(args.html.read_text(encoding="utf-8", errors="replace"), args.url),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
