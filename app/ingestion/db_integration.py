from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts.eligibility import prompt
from app.db.postgres_db.session import get_db
from app.db.postgres_db.models import ClinicalTrial
from langchain_core.documents import Document
from app.ingestion.pre_process import  build_eligibility_criteria_string
from app.schemas.llm_schema import ClinicalTrialSchema


def save_clinical_trial_data_to_postgres(clinical_trial_data):
    try:
        db = next(get_db())
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return
    try:
        model = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
        structured_model = model.with_structured_output(ClinicalTrialSchema)
        extraction_chain = prompt | structured_model
        for trial in clinical_trial_data.get("studies", []):
            nct_id = trial['protocolSection']['identificationModule']['nctId']
            brief_title = trial['protocolSection']['identificationModule']['briefTitle']
            interventions = trial['protocolSection'].get('armsInterventionsModule', {}).get('interventions', [])
            brief_summary = trial['protocolSection'].get('descriptionModule', {}).get('briefSummary', '')
            conditions = trial['protocolSection'].get('conditionsModule', {}).get('conditions', [])
            eligibility_criteria = trial['protocolSection'].get('eligibilityModule', {}).get('eligibilityCriteria', '')
            phases = trial['protocolSection'].get('designModule', {}).get('phases', [])
            locations = trial['protocolSection'].get('contactsLocationsModule', {}).get('locations', [])
            response = extraction_chain.invoke({"protocol_text": eligibility_criteria})
            clinical_trial_entry = ClinicalTrial(
                nct_id=nct_id,
                brief_title=brief_title,
                interventions=interventions,
                brief_summary=brief_summary,
                conditions=conditions,
                eligibility_criteria=response.model_dump(),
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
        db = next(get_db())
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return
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
            trial = db.query(ClinicalTrial).filter(ClinicalTrial.nct_id == nct_id).first()
            eligibility_criteria_json = trial.eligibility_criteria if trial else None
            eligibility_text = build_eligibility_criteria_string(eligibility_criteria_json)
            document_content = f"Title: {brief_title}\nSummary: {brief_summary}\nConditions: {', '.join(conditions)}\nEligibility Criteria: {eligibility_text}\nSex: {sex}\nMinimum Age: {minimum_age}\nMaximum Age: {maximum_age}"
            metadata = {"nct_id": nct_id}
            document = Document(page_content=document_content, metadata=metadata)
            doc.append(document)
        vector_client.add_documents(doc)
        print(f"Successfully added {len(doc)} clinical trial documents to the vector database.")
    except Exception as e:
        print(f"Error saving clinical trial data to vector database: {e}")


