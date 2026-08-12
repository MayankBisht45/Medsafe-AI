import json
from rapidfuzz import process, fuzz

def load_medicine_data(json_path="data/medicines.json"):
    """Loads medicine and interaction records from JSON database."""
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"medicines": [], "interactions": []}

def match_medicine_name(user_query, medicine_list, score_cutoff=70):
    """
    Uses RapidFuzz to map user query (even with typos) to canonical medicine name.
    """
    # Create a lookup dictionary of names and aliases
    choices = []
    med_map = {}
    
    for med in medicine_list:
        canonical_name = med["name"]
        choices.append(canonical_name)
        med_map[canonical_name.lower()] = canonical_name
        
        for alias in med.get("aliases", []):
            choices.append(alias)
            med_map[alias.lower()] = canonical_name

    # RapidFuzz extract One match
    match = process.extractOne(user_query, choices, scorer=fuzz.WRatio)
    
    if match and match[1] >= score_cutoff:
        matched_string = match[0]
        confidence = match[1]
        canonical = med_map[matched_string.lower()]
        return canonical, round(confidence, 1)
    
    return None, 0

def check_drug_interactions(selected_medicines, interaction_list):
    """
    Checks all pairs within selected_medicines against known interactions.
    """
    found_interactions = []
    
    # Standardize names to set
    med_set = set(selected_medicines)
    
    for item in interaction_list:
        pair_set = set(item["pair"])
        # If both medicines in pair match user's input list
        if pair_set.issubset(med_set):
            found_interactions.append(item)
            
    return found_interactions