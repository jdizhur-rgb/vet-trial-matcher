"""Production-only aliases for catalog site labels that map to known physical centers.

These aliases keep strict address validation enabled while allowing short site labels
used in trial records to resolve to the canonical location directory.
"""
from __future__ import annotations

SITE_ALIASES = {
    "📍 University of Florida Vet Med": "University of Florida College of Veterinary Medicine",
    "📍 University of Illinois Vet Med": "University of Illinois College of Veterinary Medicine",
    "📍 Penn Vet": "University of Pennsylvania School of Veterinary Medicine",
    "📍 University of Minnesota Vet Med": "University of Minnesota College of Veterinary Medicine",
    "📍 Tufts Cummings Vet": "Tufts University Cummings School of Veterinary Medicine",
    "📍 Michigan State Vet Med": "Michigan State University College of Veterinary Medicine",
    "📍 Cornell Vet": "Cornell University College of Veterinary Medicine",
    "📍 University of Georgia Vet Med": "University of Georgia College of Veterinary Medicine",
    "📍 Colorado State Flint Animal Cancer Center": "Colorado State University Flint Animal Cancer Center",
    "📍 Texas A&M Vet Med": "Texas A&M School of Veterinary Medicine",
    "📍 University of Missouri Vet Med": "University of Missouri College of Veterinary Medicine",
    "📍 University of Milan Vet Hospital": "University of Milan Veterinary Teaching Hospital (Lodi)",
    "📍 University of Zurich Vet Hospital": "University of Zurich Veterinary Hospital",
    "📍 NC State Vet Hospital": "NC State College of Veterinary Medicine",
    "📍 Ohio State Vet Medical Center": "Ohio State University College of Veterinary Medicine",
    "📍 Auburn Vet Med": "Auburn University College of Veterinary Medicine",
    "📍 LSU Vet Med": "Louisiana State University School of Veterinary Medicine",
    "📍 Virginia Tech Vet Med": "Virginia-Maryland College of Veterinary Medicine / Virginia Tech",
    "📍 Johns Hopkins CIGAT": "Johns Hopkins Center for Image-Guided Animal Therapy (CIGAT)",
}


def apply_aliases(center_directory):
    """Add aliases to the already-built center-directory indexes in memory."""
    for alias, canonical in SITE_ALIASES.items():
        if canonical not in center_directory.LOCATIONS:
            raise KeyError(f"Unknown canonical center for alias {alias!r}: {canonical!r}")
        key = center_directory.normalize(alias)
        center_directory.ALIASES[alias] = canonical
        center_directory._CANONICAL_INDEX[key] = canonical
        center_directory._INDEX[key] = center_directory.LOCATIONS[canonical]
