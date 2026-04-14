from app.db.postgres_db.session import get_db
from app.db.postgres_db.models import ClinicalTrial
from langchain_core.documents import Document
from app.ingestion.pre_process import build_eligibility_criteria_string


def save_clinical_trial_data_to_postgres(clinical_trial_data):
    try:
        db = next(get_db())
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return
    try:

        for trial in clinical_trial_data.get("studies", []):
            nct_id = trial['protocolSection']['identificationModule']['nctId']
            brief_title = trial['protocolSection']['identificationModule']['briefTitle']
            interventions = trial['protocolSection'].get('armsInterventionsModule', {}).get('interventions', [])
            brief_summary = trial['protocolSection'].get('descriptionModule', {}).get('briefSummary', '')
            conditions = trial['protocolSection'].get('conditionsModule', {}).get('conditions', [])
            eligibility_criteria = trial['protocolSection'].get('eligibilityModule', {}).get('eligibilityCriteria', '')
            phases = trial['protocolSection'].get('designModule', {}).get('phases', '')
            locations = trial['protocolSection'].get('contactsLocationsModule', {}).get('locations', [])

            clinical_trial_entry = ClinicalTrial(
                nct_id=nct_id,
                brief_title=brief_title,
                interventions=interventions,
                brief_summary=brief_summary,
                conditions=conditions,
                eligibility_criteria=eligibility_criteria,
                phases=phases,
                locations=locations
            )
            db.add(clinical_trial_entry)
        db.commit()
        print(f"Successfully saved {len(clinical_trial_data.get('studies', []))} clinical trials to PostgreSQL.")
    except Exception as e:
        print(f"Error saving clinical trial data to PostgreSQL: {e}")
        db.rollback()

def save_clinical_trials_data_to_vector_db(clinical_trial_data, vector_client):
    try:
        doc = []
        for trial in clinical_trial_data.get("studies", []):
            nct_id = trial['protocolSection']['identificationModule']['nctId']
            brief_title = trial['protocolSection']['identificationModule']['briefTitle']
            brief_summary = trial['protocolSection'].get('descriptionModule', {}).get('briefSummary', '')
            conditions = trial['protocolSection'].get('conditionsModule', {}).get('conditions', [])
            eligibility_criteria = trial['protocolSection'].get('eligibilityModule', {})
            sex = eligibility_criteria.get('sex', 'N/A')
            minimum_age = eligibility_criteria.get('minimumAge', 'N/A')
            maximum_age = eligibility_criteria.get('maximumAge', 'N/A')
            eligibility_text = build_eligibility_criteria_string(eligibility_criteria.get('eligibilityCriteria', ''))
            document_content = f"Title: {brief_title}\nSummary: {brief_summary}\nConditions: {', '.join(conditions)}\nEligibility Criteria: {eligibility_text}\nSex: {sex}\nMinimum Age: {minimum_age}\nMaximum Age: {maximum_age}"
            metadata = {"nct_id": nct_id}
            document = Document(page_content=document_content, metadata=metadata)
            doc.append(document)
        vector_client.add_documents(doc)
        print(f"Successfully added {len(doc)} clinical trial documents to the vector database.")
    except Exception as e:
        print(f"Error saving clinical trial data to vector database: {e}")


