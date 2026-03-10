import os

from langchain.messages import HumanMessage
import json

from src.agents.explanation_agent import AgentState, explanation_agent
from src.core.database import OncoDatabase
from src.core.rule_engine import rule_engine
from src.core.validator import InputData


def run(input_data):
    validated_data = InputData(**input_data)
    result = rule_engine(validated_data)
    result = json.dumps(result, indent=2)  
    input_message = HumanMessage(content=result)
    agent_state = AgentState(message=input_message)
    explanation = explanation_agent(agent_state)
    return explanation

if __name__ == "__main__":
    input_data = {
        "mutation": "Exon19del",
        "cancer_type": "nsclc"
    }
    OncoDatabase.load_data(os.getenv("DATA_DIR"))
    explanation = run(input_data)
    print(explanation)


"""
output:
This patient has **Non-Small Cell Lung Cancer (NSCLC)** driven by a specific genetic alteration: an **EGFR exon 19 deletion (E746_A750del)**.

**Key Points:**

1.  **Molecular Profile:** The presence of an EGFR exon 19 deletion is a highly significant and actionable finding. This specific mutation leads to constitutive (always-on) activation of the EGFR signaling pathway, which promotes uncontrolled cell growth and survival in cancer cells.
2.  **Therapeutic Strategy:** Tumors with this mutation are highly sensitive to **EGFR tyrosine kinase inhibitors (TKIs)**.
    *   **First-Line Recommendation:** The preferred initial treatment is **Osimertinib**. Osimertinib is a third-generation EGFR TKI that has demonstrated superior efficacy and a favorable safety profile compared to older generations of TKIs in patients with EGFR-mutated NSCLC, including those with exon 19 deletions.
    *   **Alternative Options:** **Erlotinib** and **Gefitinib** (first-generation EGFR TKIs) are also effective alternatives, though Osimertinib is generally favored for first-line therapy due to its enhanced activity and ability to overcome common resistance mechanisms.
3.  **Evidence Level:** The recommendation for these targeted therapies is supported by a **High level of evidence**, indicating robust clinical data from well-designed studies, which strongly validates this treatment approach.

**In summary:** This patient has a classic, highly targetable mutation (EGFR exon 19 deletion) in their NSCLC, making them an excellent candidate for precision oncology with EGFR TKIs, with Osimertinib being the optimal first-line choice based on strong clinical evidence.
"""