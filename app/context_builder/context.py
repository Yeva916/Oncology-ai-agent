from app.db.postgres_db.models import ClinicalTrial
# from app.retrival_system.hybrid_retriever import hybrid_retriever
from app.db.postgres_db.session import get_db
from app.prompts.context import context_prompt
# from app.schemas.util import EligibilityContext, Trial_context
def format_trial(trial):
    return f"""
Trial ID: {trial['Trial ID']}
Title: {trial['Title']}
Condition: {trial['Condition']}
Eligibility:
Inclusion:
{chr(10).join(f"    - {i}" for i in trial['Eligibility']['Inclusion'])}
Exclusion:
{chr(10).join(f"    - {i}" for i in trial['Eligibility']['Exclusion'])}
            """

def build_context(results,user_query):
    try:
        db = next(get_db())
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return []
    context = ""
    formated_trials = []

    for res in results:
        nct_id = res['nct_id']
        trial_data = db.query(ClinicalTrial).filter(ClinicalTrial.nct_id == nct_id).first()
        if trial_data:
            trial_context = {
                "Trial ID": trial_data.nct_id,
                "Title": trial_data.brief_title,
                "Condition": ", ".join(trial_data.conditions),
                "Eligibility": {
                    "Inclusion": trial_data.eligibility_criteria.get("inclusion_rules", []),
                    "Exclusion": trial_data.eligibility_criteria.get("exclusion_rules", [])
                }
            }

            formated_trials.append(format_trial(trial_context))
            
    context = context = "\n---\n".join(
    [f"Trial {i+1}\n{trial}" for i, trial in enumerate(formated_trials)]
)
    prompt = context_prompt.format(user_query=user_query, context=context)
    return prompt



if __name__ == "__main__":
    # Example results from retriever
    results = [{'nct_id': 'NCT06116682', 'final_score': 0.8472808895, 'breakdown': {'keyword': 0.694561839, 'vector': 0.99999994}}, 
               {'nct_id': 'NCT06538038', 'final_score': 0.8447493505, 'breakdown': {'keyword': 0.689498901, 'vector': 0.9999998}}]
    context = build_context(results, "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy.")
    print(context)
    #/home/yeshwant/mini_project/onco_agent/app/context_builder /context.py