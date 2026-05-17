from langchain_google_genai import ChatGoogleGenerativeAI
import json
from langchain_core.prompts import ChatPromptTemplate
# from app.prompts.context import context_prompt

system_template = """You are an expert clinical data engineer. Your task is to analyze a brief definition of a disease/condition and convert it into optimized search parameters for the ClinicalTrials.gov API v2.
"""
human_message = """
Analyze the following text:
---
"{user_query}"
---

Extract and format the information exactly into a JSON object with the following fields:
1. "primary_condition": The main canonical name of the disease.
2. "synonyms": A list of 2-4 alternative medical names, acronyms, or MeSH terms for this condition.
3. "boolean_query": A single string combining the primary condition and synonyms using 'OR' and quotes for multi-word phrases (e.g., "Condition A" OR "Synonym B"). All boolean operators must be capitalized.

Output ONLY valid JSON. No conversational text.
"""

context_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_message),
])



# print("Saved successfully")
def generate_clinical_trials_query(user_query):
    llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
    chain = context_prompt | llm
    response = chain.invoke({"user_query": user_query,})
    raw_text = response.content[1]['text']

    clean_text = raw_text.replace("```json", "").replace("```", "").strip()

    data = json.loads(clean_text)
    boolean_query = data["boolean_query"]
    clean = boolean_query.replace('\\"', '"')
    # with open("output.json", "w") as f:
    #     json.dump(data, f, indent=4)
    # response_text = getattr(response, "content", response)
    return clean
# if __name__ == "__main__":
    # user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
    # response = generate_response(user_query)
    # print(response)
    # s = "\"Non-Small Cell Lung Cancer\" OR \"NSCLC\""
    # print(s.replace('\\"', '"'))