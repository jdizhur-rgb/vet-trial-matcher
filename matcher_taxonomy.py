"""Shared diagnosis matching for the browser, legacy matcher and diagnosis pages.

Family matches are only invitations to protocol screening. Explicit exclusions
and species-scoped cohorts take precedence over a generic tumor label.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TAXONOMY = json.loads((ROOT / 'data/diagnosis_taxonomy.json').read_text())
ALIASES = TAXONOMY['aliases']
FAMILIES = TAXONOMY['families']
PROTOCOL_RULES = json.loads((ROOT / 'data/matcher_protocol_rules.json').read_text())


def diagnosis_match(trial, diagnosis, species=None):
    scoped = trial.get('cancers_by_species')
    allowed = scoped.get(species, []) if scoped and species else trial.get('cancers', [])
    if scoped and species and not allowed:
        return False, False
    exact = {diagnosis, *ALIASES.get(diagnosis, [])}
    if diagnosis == 'Spindle cell sarcoma':
        exact.add('Soft tissue sarcoma')
    families = set(FAMILIES.get(diagnosis, []))
    if (exact.intersection(trial.get('excluded_cancers', [])) or
            families.intersection(trial.get('excluded_disease_families', [])) or
            diagnosis in trial.get('pending_diagnosis_review', [])):
        return False, False
    if exact.intersection(allowed):
        return True, False
    broad = set(trial.get('broad_disease_families', []))
    if 'all_tumors' in broad or (not broad and 'Cancer — any type' in allowed):
        return diagnosis in FAMILIES, True
    matched = bool(families.intersection(broad))
    return matched, matched


def universal_limits_pass(requirements, patient):
    """Honor literal inclusive/exclusive protocol limits, including browse mode."""
    if patient.get('age_known'):
        age = patient['age']
        if requirements.get('min_age_years') is not None and age < requirements['min_age_years']:
            return False
        if requirements.get('min_age_years_exclusive') is not None and age <= requirements['min_age_years_exclusive']:
            return False
        if requirements.get('max_age_years') is not None and age > requirements['max_age_years']:
            return False
    if patient.get('weight_known'):
        weight = patient['weight_lb']
        factor = 2.2046226218
        minimum = requirements.get('min_weight_lb')
        if minimum is None:
            minimum = (requirements.get('min_weight_kg') or 0) * factor
        maximum = requirements.get('max_weight_lb')
        if maximum is None:
            maximum = (requirements.get('max_weight_kg') if requirements.get('max_weight_kg') is not None else float('inf')) * factor
        if weight < minimum or weight > maximum:
            return False
        if requirements.get('min_weight_kg_exclusive') is not None and weight <= requirements['min_weight_kg_exclusive'] * factor:
            return False
        if requirements.get('max_weight_kg_exclusive') is not None and weight >= requirements['max_weight_kg_exclusive'] * factor:
            return False
    return True


def owner_cohort_possible(cohorts, patient):
    """At least one protocol cohort must survive known owner answers.

    Uncertain staging and missing answers require prescreening. Procedure type
    is meaningful only when cancer surgery was actually performed.
    """
    for cohort in cohorts:
        rejected = False
        for field, allowed in cohort.items():
            if field == 'required_preferences':
                rejected |= not set(allowed).issubset(patient.get('prefs', set()))
                continue
            if field == 'prior_procedure' and patient.get('surgery') == 'No':
                continue
            answer = patient.get(field)
            if answer not in (None, "I don't know", 'Suspected / staging incomplete'):
                rejected |= answer not in allowed
        if not rejected:
            return True
    return False


def protocol_screening(trial, patient):
    """Evaluate additional stored constraints or leave a visible screening item."""
    unknown = []
    excluded = False
    for group in ('requires', 'excludes'):
        for key, value in trial.get(group, {}).items():
            if value is None or value is False:
                continue
            rule = PROTOCOL_RULES[group].get(key)
            if rule is None:
                raise ValueError(f'Unclassified matcher constraint: {group}.{key}')
            if rule.get('when_family') and rule['when_family'] not in FAMILIES.get(patient.get('cancer'), []):
                continue
            if rule.get('when_field') and not all(patient.get(field) in allowed for field, allowed in rule['when_field'].items()):
                continue
            if rule.get('alternative_owner_cohorts'):
                excluded |= not owner_cohort_possible(value, patient)
                continue
            if rule.get('handled'):
                continue
            if rule.get('confirmation_or_appendicular_osa'):
                if patient.get('diagnosis_status') == 'Suspected / not confirmed' and (
                    patient.get('cancer') != 'Osteosarcoma' or
                    patient.get('osa_location') == 'Axial — skull, spine, rib, or pelvis'
                ):
                    excluded = True
                unknown.append('required ' + rule['label'])
                continue
            if rule.get('history_or_preference'):
                option = rule['history_or_preference']
                answer = patient.get(option['field'])
                if answer not in option['allowed']:
                    if answer not in (None, "I don't know") and option['preference'] not in patient.get('prefs', set()):
                        excluded = True
                    else:
                        unknown.append('required ' + rule['label'])
                continue
            field = rule.get('field')
            answer = patient.get(field) if field else None
            if rule.get('allowed') and answer not in (None, "I don't know"):
                excluded |= answer not in rule['allowed']
            elif rule.get('disallowed') and answer not in (None, "I don't know"):
                excluded |= answer in rule['disallowed']
            elif rule.get('preference'):
                excluded |= rule['preference'] not in patient.get('prefs', set())
                unknown.append('required study ' + rule['preference'].lower())
            else:
                suffix = '' if value is True else ': ' + str(value)
                unknown.append(('required ' if group == 'requires' else 'exclusion: ') + rule['label'] + suffix)
    return excluded, unknown
