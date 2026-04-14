# from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from pydantic import json
import json
from app.schemas.llm_schema import ClinicalTrialSchema
from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts.eligibility import prompt

def build_eligibility_criteria_string(eligibility_criteria):
    try:
        model = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
        structured_model = model.with_structured_output(ClinicalTrialSchema)
        extraction_chain = prompt | structured_model
        response = extraction_chain.invoke({"protocol_text": eligibility_criteria})
        data_as_dict = response.model_dump()
        eligibility_text = f"Inclusion Criteria: {data_as_dict.get('inclusion_rules', [])}\nExclusion Criteria: {data_as_dict.get('exclusion_rules', [])}\nRequired Mutations: {data_as_dict.get('required_mutations', [])}\nPermitted Mutations: {data_as_dict.get('permitted_mutations', [])}\n"
        # with open("app/data/eligibility_extraction_result.json", "w", encoding="utf-8") as f:
        #     data_as_dict = response.model_dump()
        #     json.dump(data_as_dict, f, indent=4)
        return eligibility_text
    
    except Exception as e:
        print(f"Error building eligibility criteria string: {e}")
        return "Error occurred while processing eligibility criteria."