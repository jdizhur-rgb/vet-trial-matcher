#!/usr/bin/env python3
"""Apply and validate Vet Trial Finder's sentence-case editorial style."""
from __future__ import annotations

import re
from pathlib import Path

import generate_seo as g


SITE_COPY = {
    "Find Trials": "Find trials",
    "Trial Registry": "Trial registry",
    "Cancer Types": "Cancer types",
    "Oncology Centers": "Oncology centers",
    "Trial Centers": "Trial centers",
    "Other Treatments": "Other treatments",
    "How We Verify": "How we verify",
    "Cancer Trial Coverage": "Cancer trial coverage",
    "Help Center": "Help center",
    "Why This Project Exists": "Why this project exists",
    "Other Cancer Treatment Options": "Other cancer treatment options",
    "Advanced Treatments": "Advanced treatments",
    "Expanded Access": "Expanded access",
    "Veterinary Cancer Articles": "Veterinary cancer articles",
    "Electrochemotherapy in Veterinary Oncology": "Electrochemotherapy in veterinary oncology",
    "Clinical Trials for Pets with Cancer": "Clinical trials for pets with cancer",
    "Cancer Vaccines for Dogs": "Cancer vaccines for dogs",
    "Clean, Close, and Dirty Margins After Tumor Removal": "Clean, close, and dirty margins after tumor removal",
    "Clean, Close, and Dirty Surgical Margins": "Clean, close, and dirty surgical margins",
    "Free Veterinary Cancer Clinical Trial Finder for Dogs and Cats": "Free veterinary cancer clinical trial finder for dogs and cats",
    "Search Clinical Trials": "Search clinical trials",
    "Find Clinical Trials": "Find clinical trials",
    "Browse the Trial Registry": "Browse the trial registry",
    "Browse Cancer Types": "Browse cancer types",
    "Find Oncology Centers": "Find oncology centers",
    "Clinical Trials &amp; Experimental Treatments for Dogs and Cats": "Clinical trials and experimental treatments for dogs and cats",
    "Clinical Trials & Experimental Treatments for Dogs and Cats": "Clinical trials and experimental treatments for dogs and cats",
    "Oncology Centers &amp; Research Programs": "Oncology centers and research programs",
    "Oncology Centers & Research Programs": "Oncology centers and research programs",
    "Page Not Found": "Page not found",
    "Cancer Clinical Trials for Dogs and Cats": "Cancer clinical trials for dogs and cats",
    "How to Use Vet Trial Finder": "How to use Vet Trial Finder",
    "Other Veterinary Cancer Treatments": "Other veterinary cancer treatments",
    "How We Verify Clinical Trial Listings": "How we verify clinical trial listings",
    "How we verify Clinical Trial Listings": "How we verify clinical trial listings",
    "How we verify Listings": "How we verify listings",
    "Veterinary Oncology Centers &amp; Research Programs": "Veterinary oncology centers and research programs",
    "Veterinary Oncology Centers & Research Programs": "Veterinary oncology centers and research programs",
    "Veterinary Oncology centers &amp; Research Programs": "Veterinary oncology centers and research programs",
    "Veterinary Oncology centers & Research Programs": "Veterinary oncology centers and research programs",
    "Veterinary Clinical Trial centers": "Veterinary clinical trial centers",
    "Electrochemotherapy for Dogs and Cats": "Electrochemotherapy for dogs and cats",
    "Find clinical trials for Dogs and Cats": "Find clinical trials for dogs and cats",
    # Component labels above may be normalized before these longer phrases.
    "Browse the Trial registry": "Browse the trial registry",
    "Browse Cancer types": "Browse cancer types",
    "Find Oncology centers": "Find oncology centers",
}


def sentence_diagnosis(label: str) -> str:
    first, *rest = label.split(" ")
    return " ".join([first, *(word.lower() for word in rest)])


def diagnosis_species(path: Path | None) -> str | None:
    if path is None:
        return None
    parts = path.parts
    if "north-america" not in parts:
        return None
    if "dogs" in parts:
        return "dogs"
    if "cats" in parts:
        return "cats"
    return None


SEARCH_TITLES = {
    "index.html": "Vet Trial Finder | Find cancer care for dogs and cats",
    "matcher/index.html": "Find cancer clinical trials for dogs and cats",
    "matcher/centers/index.html": "Find a veterinary oncologist near you",
    "about/index.html": "About this project",
    "help/index.html": "How to use this site | Help center",
    "contact/index.html": "Contact",
}


def search_title(text: str, path: Path | None) -> str:
    if path is not None:
        parts = path.parts
        if "site" in parts:
            route = "/".join(parts[parts.index("site") + 1:])
            if route == "index.html":
                return SEARCH_TITLES[route]
            if route in SEARCH_TITLES:
                text = SEARCH_TITLES[route]
    text = re.sub(r"\s*\|\s*Vet Trial Finder\s*$", "", text)
    text = re.sub(r"^Vet Trial Finder\s*\|\s*", "", text)
    text = text.replace("Vet Trial Finder", "this project").strip()
    return f"{text} | Vet Trial Finder"


def normalize(text: str, path: Path | None = None) -> str:
    for old, new in SITE_COPY.items():
        text = text.replace(old, new)
    text = text.replace(" | Veterinary Oncology &amp; Clinical Trials |", " | Veterinary oncology and clinical trials |")
    text = text.replace(" | Veterinary Oncology & Clinical Trials |", " | Veterinary oncology and clinical trials |")
    text = text.replace(" | Veterinary Cancer Study |", " | Veterinary cancer study |")
    text = text.replace(" | Veterinary Cancer Research |", " | Veterinary cancer research |")
    text = re.sub(r" Clinical Trials for (Dogs|Cats)(?= \|)", lambda m: f" clinical trials for {m.group(1).lower()}", text)
    for old, new in (
        ("Veterinary Oncology", "veterinary oncology"),
        ("Comparative Oncology", "comparative oncology"),
        ("Veterinary Cancer Research", "veterinary cancer research"),
        ("Veterinary Clinical Research", "veterinary clinical research"),
        ("Animal Cancer Research", "animal cancer research"),
    ):
        text = re.sub(rf"(<h2>About [^<]*?){old}(</h2>)", rf"\1{new}\2", text)
    for key in g.DISEASE_INFO:
        label = g.display_name(key)
        sentence = sentence_diagnosis(label)
        text = re.sub(
            rf"(<h1\b[^>]*>){re.escape(label)}(</h1>)",
            rf"\1{sentence}\2",
            text,
        )
        text = text.replace(f"<strong>{label}</strong>", f"<strong>{sentence}</strong>")
        text = text.replace(f"<h2>Understanding {label}</h2>", f"<h2>Understanding {sentence.lower()}</h2>")
        text = text.replace(f"{label} clinical trials for dogs", f"{sentence} clinical trials for dogs")
        text = text.replace(f"{label} clinical trials for cats", f"{sentence} clinical trials for cats")
        species = diagnosis_species(path)
        if species:
            old_title = f"{sentence} clinical trials for {species}"
            new_title = f"{sentence} in {species}: treatment, prognosis and clinical trials"
            text = text.replace(old_title, new_title)
            text = re.sub(
                rf"(<h1\b[^>]*>){re.escape(sentence)}(</h1>)",
                rf"\1{new_title}\2",
                text,
            )
    text = text.replace("University / Teaching Hospital", "University / teaching hospital")
    text = text.replace("Specialty Hospital / Research Center", "Specialty hospital / research center")
    text = text.replace("Multicenter Study", "Multicenter study")
    text = text.replace("Research Organization", "Research organization")
    # Change page-title metadata only; keep site identity and visible copy intact.
    text = re.sub(r"(<title>)(.*?)(</title>)",
                  lambda m: m[1] + search_title(m[2], path) + m[3], text, flags=re.S)
    text = re.sub(r'(<meta\b[^>]*(?:property|name)="(?:og:title|twitter:title)"[^>]*content=")([^"]*)(")',
                  lambda m: m[1] + search_title(m[2], path) + m[3], text)
    return text


def validate(root: Path) -> None:
    failures: list[str] = []
    for path in root.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        for phrase in SITE_COPY:
            if phrase in text:
                failures.append(f"{path.relative_to(root)}: {phrase}")
        if re.search(r" Clinical Trials for (Dogs|Cats)(?= \|)", text):
            failures.append(f"{path.relative_to(root)}: diagnosis SEO title")
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        if title and (not title[1].strip() or title[1].count("Vet Trial Finder") != 1):
            failures.append(f"{path.relative_to(root)}: missing or duplicate title brand")
        elif title and path != root / "index.html" and not title[1].endswith(" | Vet Trial Finder"):
            failures.append(f"{path.relative_to(root)}: missing title brand suffix")
        expected_title = SEARCH_TITLES.get(path.relative_to(root).as_posix())
        if expected_title and (not title or title[1] != search_title(expected_title, path)):
            failures.append(f"{path.relative_to(root)}: search title override")
        species = diagnosis_species(path)
        if species:
            h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.S)
            title = re.search(r"<title>(.*?)</title>", text, re.S)
            expected = f"in {species}: treatment, prognosis and clinical trials"
            if not h1 or expected not in h1.group(1):
                failures.append(f"{path.relative_to(root)}: diagnosis H1")
            if not title or expected not in title.group(1):
                failures.append(f"{path.relative_to(root)}: diagnosis SEO title")
    if failures:
        raise AssertionError("Sentence-case validation failed:\n" + "\n".join(failures[:40]))


def main() -> None:
    root = Path(__file__).resolve().parent / "site"
    pages = list(root.rglob("*.html"))
    if not pages:
        raise AssertionError("Generated site is missing")
    for path in pages:
        path.write_text(normalize(path.read_text(encoding="utf-8"), path), encoding="utf-8")
    validate(root)
    print(f"SENTENCE_CASE_OK pages={len(pages)}")


if __name__ == "__main__":
    main()
