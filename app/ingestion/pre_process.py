# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from pydantic import json
# import json
# from app.schemas.llm_schema import ClinicalTrialSchema
# from langchain_google_genai import ChatGoogleGenerativeAI
# from app.prompts.eligibility import prompt
# from app.db.postgres_db.session import get_db
# from app.db.postgres_db.models import EligibilityCriteria

def build_eligibility_criteria_string(eligibility_criteria_dict):
    try:
        # print(eligibility_criteria_dict)
        # print(type(eligibility_criteria_dict))
        # eligibility_criteria_dict = eligibility_criteria_json.model_dump()
        eligibility_text = f"""Inclusion Criteria: {eligibility_criteria_dict.get('inclusion_rules', [])}
                            \nExclusion Criteria: {eligibility_criteria_dict.get('exclusion_rules', [])}
                            \nRequired Mutations: {eligibility_criteria_dict.get('required_mutations', [])}
                            \nPermitted Mutations: {eligibility_criteria_dict.get('permitted_mutations', [])}\n"""
        # with open("app/data/eligibility_extraction_result.json", "w", encoding="utf-8") as f:
        #     data_as_dict = response.model_dump()
        #     json.dump(data_as_dict, f, indent=4)
        return eligibility_text
    
    except Exception as e:
        print(f"Error building eligibility criteria string: {e}")
        return "Error occurred while processing eligibility criteria."
    

# def build_eligibility_criteria_json(clinical_trial_data):
#     try:
#         db = next(get_db())
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         return
#     try:
#         model = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
#         structured_model = model.with_structured_output(ClinicalTrialSchema)
#         extraction_chain = prompt | structured_model
#         for trial in clinical_trial_data.get("studies", []):
#             nct_id = trial['protocolSection']['identificationModule']['nctId']
#             eligibility_criteria = trial['protocolSection'].get('eligibilityModule', {}).get('eligibilityCriteria', '')
#             response = extraction_chain.invoke({"protocol_text": eligibility_criteria})
#             data_as_dict = response.model_dump()
#             db.add(EligibilityCriteria(nct_id=nct_id, criteria=data_as_dict))
#             db.commit()
#         print("Eligibility criteria JSON built and saved to the database successfully.")
#         return "Eligibility criteria JSON built and saved to the database successfully."
#     except Exception as e:
#         print(f"Error building eligibility criteria JSON: {e}")
#         return {"error": "Error occurred while processing eligibility criteria."}