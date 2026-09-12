from __future__ import annotations
import re

VERIFIED_LOCATIONS = {
    'Royal Veterinary College Queen Mother Hospital for Animals': 'Queen Mother Hospital for Animals, The Royal Veterinary College, Hawkshead Lane, North Mymms, Hatfield AL9 7TA, UK',
    'Charleston Veterinary Referral Center': 'Charleston Veterinary Referral Center, 3484 Shelby Ray Ct, Charleston, SC 29414',
    'Boston West Veterinary Emergency & Specialty': 'Boston West Veterinary Emergency & Specialty, 5 Strathmore Rd, Natick, MA 01760',
    'Boston West Veterinary Emergency and Specialty': 'Boston West Veterinary Emergency & Specialty, 5 Strathmore Rd, Natick, MA 01760',
    'Pacific Northwest Pet ER & Specialty Center': 'Pacific Northwest Pet ER & Specialty Center, 815 SE 160th Ave, Vancouver, WA 98683',
    'Pacific Northwest Pet Emergency & Specialty Center': 'Pacific Northwest Pet ER & Specialty Center, 815 SE 160th Ave, Vancouver, WA 98683',
    'Upstate Vet Emergency + Specialty Care': 'Upstate Vet Emergency & Specialty Care, 393 Woods Lake Rd, Greenville, SC 29607',
    'Animal Medical Center of Plainfield': 'Animal Medical Center of Plainfield, 13813 S Route 59, Plainfield, IL 60544',
    'Eastern Carolina Veterinary Medical Center': 'Eastern Carolina Veterinary Medical Center, 50 Greenville Ave, Wilmington, NC 28403',
    'Spanaway Veterinary Clinic': 'Spanaway Veterinary Clinic, 16920 Pacific Ave S, Spanaway, WA 98387',
    'Nashville Veterinary Specialists': 'Nashville Veterinary Specialists, 2971 Sidco Dr, Nashville, TN 37204',
    'Veterinary Cancer Care': 'Veterinary Cancer Care, 2001 Vivigen Way #B, Santa Fe, NM 87505',
    'Animal Cancer Care and Research Center': 'Animal Cancer Care and Research Center, 4 Riverside Cir, Roanoke, VA 24016',
    'Animal Emergency Hospital': 'Animal Emergency Hospital, 722 Baltimore Pike, Bel Air, MD 21014',
    'McAbee Veterinary Hospital': 'McAbee Veterinary Hospital, 4586 N Palmetto Ave, Winter Park, FL 32792',
    'Sumner Veterinary Hospital': 'Sumner Veterinary Hospital, 16024 60th St E, Sumner, WA 98390',
    'Cornell University Hospital for Animals': 'Cornell University Hospital for Animals, 930 Campus Rd, Ithaca, NY 14853',
    'Lloyd Veterinary Medical Center, Iowa State University': 'Lloyd Veterinary Medical Center, 1809 S Riverside Dr, Ames, IA 50011',
    'University of Tennessee Veterinary Medical Center': 'UT Veterinary Medical Center, 2407 River Dr, Knoxville, TN 37996',
    'Auburn University Bailey Small Animal Teaching Hospital': 'Bailey Small Animal Teaching Hospital, 1220 Wire Rd, Auburn, AL 36832',
    'Care Center': 'CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249',
    'CARE Center': 'CARE Center, 6995 E Kemper Rd, Cincinnati, OH 45249',
    'Bridge Animal Referral Center': 'Bridge Animal Referral Center, 8401 Main St, Edmonds, WA 98026',
    'Bridge Animal Referral Center, 8401 Main St': 'Bridge Animal Referral Center, 8401 Main St, Edmonds, WA 98026',
}

def _norm(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', str(value or '').lower().replace('&', ' and ')).strip()

_INDEX = {_norm(k): v for k, v in VERIFIED_LOCATIONS.items()}

def verified_addresses_for(name: str):
    value = _INDEX.get(_norm(name), '')
    return [value] if value else []
