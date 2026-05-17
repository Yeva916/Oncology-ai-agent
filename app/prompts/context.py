
from langchain_core.prompts import ChatPromptTemplate

system_template = """
You are a clinical trial matching assistant.

You must compare a patient query against retrieved clinical trials and write a concise eligibility report.
You must rely only on the supplied patient data and trial context.
If any detail is missing, write "Not specified" instead of guessing.
Do not provide medical advice.
"""

human_message = """
PATIENT DATA:
{user_query}

RETRIEVED CLINICAL TRIALS:
{context}

Write the response in plain text using this exact structure for each trial:

Trial ID: <NCT ID>
Relevance: <High / Medium / Low>
Clinical Summary: <one concise paragraph describing the study>
Eligibility Assessment:

    • Inclusion Match: <criteria the patient appears to meet>
    • Inclusion Gaps: <missing, unknown, or unmet criteria>
    • Exclusion Conflicts: <explicit disqualifiers or None>

Final Judgment: <clear conclusion about eligibility and why>

Separate each trial with a line containing only ---.

After the trial blocks, add this final section exactly:

**FINAL SUMMARY:**

**Best matching trial:** <trial ID>

**Why it is the best:** <one short paragraph>

**Any risks or uncertainties:** <one short paragraph>

Use the trial context to rank the results from most relevant to least relevant.
If the patient is clearly ineligible, say so directly.
"""

context_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_message),
])

if __name__ == "__main__":
    # Example usage
    example_context = """
    Trial ID: NCT12345678
    Title: A Study of Drug X in Lung Cancer
    Condition: Non-Small Cell Lung Cancer

    Eligibility:
    Inclusion:
    - Must have EGFR mutation (exon 19 deletion or L858R)
    - Age ≥ 18 years
    - ECOG performance status 0-1

    Exclusion:
    - History of interstitial lung disease (ILD)
    - QTc interval > 450 ms
    - LVEF < 50%
    """
    
    prompt_text = context_prompt.format(user_query="Patient with metastatic colorectal cancer", context=example_context)
    print(prompt_text)