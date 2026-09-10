"""Production-safe oncology finder wrapper.

The broad third-party locator is useful for research, but its current HTML can merge
multiple hospital cards into one malformed record. Public search therefore uses only
the curated/verified hospital records until locator ingestion is normalized offline.
"""
import importlib.util
from pathlib import Path


def render():
    helper=Path(__file__).with_name("_oncology_center_finder.py")
    spec=importlib.util.spec_from_file_location("oncology_center_finder_base",helper)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Disable live locator scraping in the public renderer. Curated EXTRAS + verified
    # Canadian records remain available, including the expanded ECT audit.
    mod._locator_centers=lambda: []
    try:
        mod.load_centers.clear()
    except Exception:
        pass
    mod.render()
