import json
from app.ingestion.db_integration import save_clinical_trial_data_to_postgres
with open("app/data/clinical_trials_results.json", "r", encoding="utf-8") as f:
    clinical_trial_data = json.load(f)
    save_clinical_trial_data_to_postgres(clinical_trial_data)
