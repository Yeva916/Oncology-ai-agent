from app.db.postgres_db.models import ClinicalTrial
from app.db.postgres_db.session import get_db
from app.retrival_system.hybrid_retriever import hybrid_retriever
from app.retrival_system.keyword_retriever import keyword_retriever
from app.retrival_system.vector_retriever import vector_retriever


def _safe_text(value):
    if value is None:
        return "Not specified"
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped else "Not specified"
    if isinstance(value, list):
        values = [str(item).strip() for item in value if str(item).strip()]
        return ", ".join(values) if values else "Not specified"
    return str(value)


def _format_bullets(items):
    values = [str(item).strip() for item in (items or []) if str(item).strip()]
    if not values:
        return "    • Not specified"
    return "\n".join(f"    • {item}" for item in values)


def _normalize_seed_results(results):
    normalized = []
    for item in results or []:
        if isinstance(item, dict) and item.get("nct_id"):
            normalized.append({
                "nct_id": item["nct_id"],
                "final_score": item.get("final_score", 0.0),
                "breakdown": item.get("breakdown", {}),
            })
    return normalized


def _retrieve_trials(user_query, results):
    seed_results = _normalize_seed_results(results)
    if seed_results:
        return sorted(seed_results, key=lambda item: item.get("final_score", 0.0), reverse=True)

    try:
        keyword_results = keyword_retriever(user_query)
        vector_results = vector_retriever(user_query)
        return hybrid_retriever(keyword_results, vector_results, alpha=0.5)
    except Exception as exc:
        print(f"Error retrieving clinical trials: {exc}")
        return []


def _build_trial_block(trial, trial_score=None):
    eligibility = trial.eligibility_criteria or {}
    inclusion_rules = eligibility.get("inclusion_rules", [])
    exclusion_rules = eligibility.get("exclusion_rules", [])

    lines = [
        f"Trial ID: {trial.nct_id}",
        f"Title: {_safe_text(trial.brief_title)}",
        f"Condition: {_safe_text(trial.conditions)}",
    ]

    if trial_score is not None:
        lines.append(f"Relevance Score: {trial_score:.3f}")

    lines.extend([
        f"Brief Summary: {_safe_text(trial.brief_summary)}",
        "Eligibility:",
        "Inclusion:",
        _format_bullets(inclusion_rules),
        "Exclusion:",
        _format_bullets(exclusion_rules),
    ])
    return "\n".join(lines)


def build_context(results, user_query):
    try:
        db = next(get_db())
    except Exception as exc:
        print(f"Error connecting to database: {exc}")
        return "No clinical trial context is available."

    ranked_trials = _retrieve_trials(user_query, results)
    formatted_trials = []

    for trial_result in ranked_trials:
        nct_id = trial_result.get("nct_id")
        if not nct_id:
            continue

        trial_data = db.query(ClinicalTrial).filter(ClinicalTrial.nct_id == nct_id).first()
        if not trial_data:
            continue

        formatted_trials.append(_build_trial_block(trial_data, trial_result.get("final_score")))

    if not formatted_trials:
        return "No matching clinical trials were found for the provided query."

    return "\n---\n".join(formatted_trials)


if __name__ == "__main__":
    results = [
        {"nct_id": "NCT06116682", "final_score": 0.8472808895, "breakdown": {"keyword": 0.694561839, "vector": 0.99999994}},
        {"nct_id": "NCT06538038", "final_score": 0.8447493505, "breakdown": {"keyword": 0.689498901, "vector": 0.9999998}},
    ]
    context = build_context(results, "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy.")
    print(context)