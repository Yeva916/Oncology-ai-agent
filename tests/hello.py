# from app.retrival_system.hybrid_retriever import hybrid_retriever
from app.context_builder.context import build_context

if __name__ == "__main__":
    results = [
            {"nct_id": "NCT06116682", "final_score": 0.8472808895, "breakdown": {"keyword": 0.694561839, "vector": 0.99999994}},
            {"nct_id": "NCT06538038", "final_score": 0.8447493505, "breakdown": {"keyword": 0.689498901, "vector": 0.9999998}},
        ]
    context = build_context(results, "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy.")
    print(context)