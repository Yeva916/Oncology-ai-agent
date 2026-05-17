from langchain_google_genai import ChatGoogleGenerativeAI

from app.context_builder.context import build_context
from app.prompts.context import context_prompt


def _build_mock_response(user_query, context):
    trial_blocks = []

    if isinstance(context, str) and context.strip():
        trial_blocks = [block.strip() for block in context.split("\n---\n") if block.strip()]

    parsed_trials = []
    for index, block in enumerate(trial_blocks[:2]):
        trial_id = f"NCT0418106{index}"
        for line in block.splitlines():
            if line.startswith("Trial ID:"):
                trial_id = line.split(":", 1)[1].strip() or trial_id
                break
        parsed_trials.append(trial_id)

    if len(parsed_trials) < 2:
        parsed_trials = ["NCT04181060", "NCT04181061"]

    trial_outputs = []
    for index, trial_id in enumerate(parsed_trials[:2]):
        relevance = "High" if index == 0 else "Medium"
        summary = (
            "This is a mock analysis for the provided patient query. It indicates a plausible match based on the retrieved trial context."
            if index == 0
            else "This is a secondary mock match that remains clinically plausible but requires additional confirmation."
        )
        inclusion_match = (
            "Age 65, ECOG performance status 1, and no prior systemic therapy align with the trial profile."
            if index == 0
            else "The patient profile is compatible with the broader study population."
        )
        inclusion_gaps = (
            "Biomarker status and site-specific laboratory requirements still need confirmation."
            if index == 0
            else "More detailed disease-specific eligibility criteria still need confirmation."
        )

        trial_outputs.append(
            f"Trial ID: {trial_id}\n"
            f"Relevance: {relevance}\n"
            f"Clinical Summary: {summary}\n"
            f"Eligibility Assessment:\n\n"
            f"    • Inclusion Match: {inclusion_match}\n"
            f"    • Inclusion Gaps: {inclusion_gaps}\n"
            f"    • Exclusion Conflicts: None identified in the mock response.\n\n"
            f"Final Judgment: Potentially eligible pending confirmation of the remaining criteria."
        )

    best_trial_id = parsed_trials[0]

    return (
        f"{trial_outputs[0]}\n\n"
        f"---\n\n"
        f"{trial_outputs[1]}\n\n"
        f"---\n\n"
        f"**FINAL SUMMARY:**\n\n"
        f"**Best matching trial:** {best_trial_id}\n\n"
        f"**Why it is the best:** This trial is the strongest mock match because it aligns with the patient’s age, ECOG status, and treatment history while remaining easy to parse in the UI.\n\n"
        f"**Any risks or uncertainties:** Biomarker confirmation and any study-specific lab thresholds should still be verified before treating this as a final clinical recommendation."
    )


def generate_demo_response(user_query, context):
    trial_context = context if isinstance(context, str) else build_context(context, user_query)
    response_text = _build_mock_response(user_query, trial_context)

    with open("response.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(str(response_text))

    return str(response_text)


def generate_response(user_query, context):
    trial_context = context if isinstance(context, str) else build_context(context, user_query)

    print("Generating response using LLM...")
    llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
    chain = context_prompt | llm
    response = chain.invoke({"user_query": user_query, "context": trial_context})
    response_text = getattr(response, "content", response)

    with open("response.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(str(response_text))

    return str(response_text)

if __name__ == "__main__":
    # Example user query and context
    user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
    context = [{'nct_id': 'NCT06116682', 'final_score': 0.8472808895, 'breakdown': {'keyword': 0.694561839, 'vector': 0.99999994}}, 
               {'nct_id': 'NCT06538038', 'final_score': 0.8447493505, 'breakdown': {'keyword': 0.689498901, 'vector': 0.9999998}}]
    response = generate_response(user_query, context)
    print(response)