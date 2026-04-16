
from langchain_core.prompts import ChatPromptTemplate

system_template = """
You are a clinical research assistant specialized in analyzing clinical trial eligibility.

Your task is to evaluate and explain how relevant the retrieved clinical trials are to the given patient/query."""

human_message = """
------------------
PATIENT DATA:
{user_query}

RETRIEVED CLINICAL TRIALS:
{context}

Each trial is provided in the following format:

Trial ID:
Title:
Condition:

Eligibility:
Inclusion:
    •   ...
Exclusion:
    •  ...



INSTRUCTIONS:

1. Evaluate EACH trial independently using the provided patient data.
2. For each trial:
    •Provide a concise clinical summary (condition, intent of study)
    •Assess eligibility:
        • Inclusion criteria satisfied
        • Inclusion gaps (missing or unmet criteria)
        • Exclusion conflicts (explicit disqualifiers)
    •Classify relevance:
        • High → strong eligibility, minimal conflicts
        • Medium → partial eligibility or unclear factors
        • Low → clear exclusion or major mismatch
3. Base all reasoning STRICTLY on the provided data.
    •Do NOT infer or assume missing clinical details
    •If required data is absent, state: "Not specified"
4. Rank the trials from most relevant to least relevant.
5. Output format:

Trial ID:
Relevance: <High / Medium / Low>
Clinical Summary:
Eligibility Assessment:

    •Inclusion Match:
    •Inclusion Gaps:
    •Exclusion Conflicts:

Final Judgment:
<clear, clinically reasoned conclusion>

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
    
    prompt_text = context_prompt.format(user_query="Patient with metastatic colorectal cancer", context=example_context)
    print(prompt_text)