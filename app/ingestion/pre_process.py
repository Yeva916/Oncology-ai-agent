def build_eligibility_criteria_string(eligibility_criteria_dict):
    try:
        eligibility_text = f"""Inclusion Criteria: {eligibility_criteria_dict.get('inclusion_rules', [])}
                            \nExclusion Criteria: {eligibility_criteria_dict.get('exclusion_rules', [])}
                            \nRequired Mutations: {eligibility_criteria_dict.get('required_mutations', [])}
                            \nPermitted Mutations: {eligibility_criteria_dict.get('permitted_mutations', [])}\n"""
        return eligibility_text
    
    except Exception as e:
        print(f"Error building eligibility criteria string: {e}")
        return "Error occurred while processing eligibility criteria."
    
