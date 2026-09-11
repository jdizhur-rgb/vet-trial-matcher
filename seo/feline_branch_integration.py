"""Apply diagnosis-specific feline decision branches without duplicating page boilerplate."""
from __future__ import annotations
import practical_cancer_pages as pages
from feline_branch_content import FELINE_BRANCHES

def validate_feline_branch_coverage(practical:dict)->list[str]:
 return sorted(set(practical)-set(FELINE_BRANCHES))

def activate_feline_branches()->None:
 original=pages.section
 def section(label,key,pet,practical):
  if pet!='cat' or key not in FELINE_BRANCHES:return original(label,key,pet,practical)
  old=pages.BRANCHES.get(key)
  pages.BRANCHES[key]=FELINE_BRANCHES[key]
  try:return original(label,key,pet,practical)
  finally:
   if old is None:pages.BRANCHES.pop(key,None)
   else:pages.BRANCHES[key]=old
 pages.section=section
