import json
import urllib.parse
import urllib.request
from pathlib import Path

UA = "SabzifyBot/1.0 (educational gardening website; local demo)"
OUT = Path(__file__).resolve().parent / "static" / "img"

JOBS = {
    "hero.jpg": "persian garden landscape",
    "inner-hero.jpg": "flower garden",
    "card-design.jpg": "formal garden",
    "card-care.jpg": "rose garden flowers",
    "card-team.jpg": "person gardening",
    "gardener.jpg": "gardener smiling",
    "stats.jpg": "green park lawn",
    "process.jpg": "planting garden soil",
    "cta.jpg": "vegetable garden rows",
    "blog-1.jpg": "potted houseplant",
    "blog-2.jpg": "tree branches garden",
    "blog-3.jpg": "garden hose watering",
    "avatar-1.jpg": "portrait smiling woman",
    "avatar-2.jpg": "portrait smiling man",
    "avatar-3.jpg": "portrait woman face",
    "about.jpg": "shiraz eram garden",
}


def search(query):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": 8,
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "iiurlwidth": 1400,
        "format": "json",
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as response:
        data = json.load(response)
    pages = data.get("query", {}).get("pages", {})
    found = []
    for page in pages.values():
        info = (page.get("imageinfo") or [{}])[0]
        thumb = info.get("thumburl") or ""
        if info.get("mime") == "image/jpeg" and thumb.startswith("https://"):
            width = info.get("thumbwidth") or 0
            if width >= 300:
                found.append((page.get("title", ""), thumb))
    return found


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    for name, query in JOBS.items():
        chosen = None
        for title, thumb in search(query):
            if title not in seen:
                chosen = (title, thumb)
                seen.add(title)
                break
        if not chosen:
            print("NONE", name)
            continue
        dest = OUT / name
        req = urllib.request.Request(chosen[1], headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as response:
            dest.write_bytes(response.read())
        print("OK", name, dest.stat().st_size, chosen[0])


if __name__ == "__main__":
    main()
