from langchain_core.prompts import ChatPromptTemplate

# Efficiently structured prompt
system_template = """
You are a Clinical Trial Extraction Agent. Your goal is to parse eligibility text into structured genomic and clinical data.

RULES:
1. Focus on EGFR status: Distinguish between 'required' and 'permitted' mutations.
2. Filter out 'Recommended but not required' procedures from hard inclusion rules.
3. Capture safety contraindications (ILD, QTc interval, LVEF) in exclusion rules.
4. Normalize all outputs to professional medical terminology.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "Extract data from the following protocol: {protocol_text}")
])