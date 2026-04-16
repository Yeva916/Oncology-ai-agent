
from langchain_core.prompts import ChatPromptTemplate

system_template = """
You are a clinical research assistant specialized in analyzing clinical trial eligibility.

Your task is to evaluate and explain how relevant the retrieved clinical trials are to the given patient/query."""

human_message = """
RETRIEVED CLINICAL TRIALS:

Each trial is provided in the following format:

Trial ID:
Title:
Condition:

Eligibility:
Inclusion:
    •   ...
Exclusion:
    •  ...

{context}

INSTRUCTIONS:

1. Process EACH trial separately using its Trial ID.
2. For each clinical trial:
•Briefly summarize the trial (condition, purpose)
•Analyze eligibility criteria:
    • Inclusion criteria match
    • Exclusion criteria conflicts
•Explain whether the patient/query is:
    • Strong match
    • Partial match
    • Not suitable
3. Provide reasoning STRICTLY based on the provided context.
    •Do NOT assume missing data
    •Do NOT hallucinate medical facts
4. Rank the trials from most relevant to least relevant.
5. Output format:

Trial ID:
Relevance: <High / Medium / Low>
Summary:
Eligibility Analysis:

    •Inclusion Match:
    •Exclusion Risks:
    Final Verdict:

(Repeat for each trial)

6. At the end, provide a FINAL SUMMARY:
    •Best matching trial
    •Why it is the best
    •Any risks or uncertainties

IMPORTANT RULES:

    •Use ONLY the given context
    •If information is missing, say "Not specified"
    •Be precise and concise
    •Do NOT generate medical advice beyond the data

ANSWER:
"""
context_prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_message)
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
    
    prompt_text = context_prompt.format(context=example_context)
    print(prompt_text)