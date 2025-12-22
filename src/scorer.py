import math

# Scoring Matrix as defined in the requirements
BREAKING_CHANGE_SCORES = {
    "endpoint-removed": 25,
    "method-removed": 20,
    "parameter-required-added": 15,
    "parameter-removed": 25,
    "parameter-type-changed": 18,
    "parameter-made-required": 12,
    "response-required-field-removed": 20,
    "response-schema-changed": 15,
    "response-required-field-added": 8,
    "endpoint-deprecated-with-timeline": 5,
    "endpoint-deprecated": 8,
    "parameter-optional-added": 0,
    "response-optional-field-added": 0,
    "endpoint-added": 0,
}

def get_change_score(change_type):
    """Look up the score for a change type"""
    return BREAKING_CHANGE_SCORES.get(change_type, 0)

def calculate_raw_score(differences):
    """Calculate raw total breaking change score"""
    total_score = 0
    # Handle case where differences is a list or a dict containing a list
    diff_list = differences if isinstance(differences, list) else differences.get('differences', [])
    
    for change in diff_list:
        change_type = change.get('type', 'unknown')
        score = get_change_score(change_type)
        total_score += score
    return total_score

def normalize_to_1_10_scale(raw_score, max_possible_score=30):
    """Convert raw score to 1–10 risk scale"""
    if raw_score <= 0:
        return 1
        
    # Normalize to 0–10 scale
    normalized = (raw_score / max_possible_score) * 10
    
    # Clamp to 1–10 (never score lower than 1 if there's any risk, but 1 is min)
    # The requirement says "Scores 1-3 (Low Risk)".
    risk_score = max(1, min(10, normalized))
    return round(risk_score, 1)

def determine_risk_level_and_action(risk_score):
    """Determine risk level and recommended reviewer actions"""
    if risk_score <= 3:
        return {
            'risk_level': 'LOW',
            'emoji': '[LOW]',
            'message': 'Safe to deploy. No special review required.',
            'reviewer_action': 'Standard review; merge confidently.'
        }
    elif risk_score <= 6:
        return {
            'risk_level': 'MEDIUM',
            'emoji': '[MED]',
            'message': 'Review carefully. Some changes may impact clients.',
            'reviewer_action': 'Require one reviewer; ensure testing coverage; notify affected teams.'
        }
    else:
        return {
            'risk_level': 'HIGH',
            'emoji': '[HIGH]',
            'message': 'High-risk change. Extra vigilance required.',
            'reviewer_action': 'Require two reviewers; mandate QA verification; consider staged rollout; notify clients.'
        }
