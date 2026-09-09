"""Verified official imagery for owner-facing center pages.

Python imports usercustomize after sitecustomize, before the SEO generator runs. Keep
image ownership here instead of mixing presentation URLs into trial records.
"""
from center_profiles import PROFILES
from center_profiles_extra import EXTRA_PROFILES

IMAGES = {
    "University of Minnesota College of Veterinary Medicine": {
        "image": "https://vetmed.umn.edu/sites/vetmed.umn.edu/files/styles/folwell_full/public/2024-09/trials-vet-modiano.jpg.avif?itok=mBlyuZZ9",
        "image_alt": "Dog featured on the University of Minnesota canine cancer clinical trials page",
        "image_caption": "Photo: University of Minnesota College of Veterinary Medicine.",
    },
    "Michigan State University College of Veterinary Medicine": {
        "image": "https://cvm.msu.edu/assets/images/hospital/_imageFit350/oncology-2024-photo.jpg",
        "image_alt": "Veterinary oncology patient and team at Michigan State University",
        "image_caption": "Photo: Michigan State University Veterinary Medical Center.",
    },
    "University of Florida College of Veterinary Medicine": {
        "image": "https://vetmed-research-a2.sites.medinfo.ufl.edu/wordpress/files/2018/04/Brody_June2015-935x1120.jpg",
        "image_alt": "Dog featured by the University of Florida Veterinary Clinical Studies Program",
        "image_caption": "Photo: University of Florida College of Veterinary Medicine.",
    },
    "University of Illinois College of Veterinary Medicine": {
        "image": "https://vetmed.illinois.edu/wp-content/uploads/2021/04/pc-radiation-selting.jpg",
        "image_alt": "Dog receiving veterinary cancer care at the University of Illinois",
        "image_caption": "Photo: University of Illinois College of Veterinary Medicine.",
    },
    "Cornell University College of Veterinary Medicine": {
        "image": "https://www.vet.cornell.edu/sites/default/files/styles/nodecontent_default/public/cute%20terrier.jpg?itok=bnfSQ3QL",
        "image_alt": "Dog featured on a Cornell veterinary cancer clinical trial page",
        "image_caption": "Photo: Cornell University College of Veterinary Medicine.",
    },
}

for _name, _image in IMAGES.items():
    if _name in PROFILES:
        PROFILES[_name].update(_image)
    if _name in EXTRA_PROFILES:
        EXTRA_PROFILES[_name].update(_image)
