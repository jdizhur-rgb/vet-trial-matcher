from pathlib import Path

HERO = "https://images.unsplash.com/photo-1770836037275-38b44e4b101f?auto=format&fit=crop&q=80&w=1800"


def apply_vaccine_hero(root: Path) -> None:
    page = root / "articles" / "cancer-vaccines" / "index.html"
    if not page.exists():
        return
    text = page.read_text(encoding="utf-8")
    text = text.replace("/assets/ect-article-hero.jpg", HERO)
    text = text.replace("A dog being examined by a veterinary oncology team", "A veterinarian giving a dog an injection")
    page.write_text(text, encoding="utf-8")
