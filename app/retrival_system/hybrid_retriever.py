
keyword_output = [{'nct_id': 'NCT06670196', 'score': 0.694561839}, {'nct_id': 'NCT06417814', 'score': 0.689498901}]
vector_output = [{'nct_id': 'NCT06670196', 'rank': 0.99999994}, {'nct_id': 'NCT06417814', 'rank': 0.9999998}]

def hybrid_retriever(keyword_results, vector_results, alpha=0.5):
    """
    Combines results using a Linear Weighted Score.
    alpha: weight for vector search (0.0 to 1.0).
    """

    combined_data = {}

    for item in keyword_results:
        nid = item['nct_id']
        combined_data[nid] = {"keyword": item['score'], "vector": 0.0}


    for item in vector_results:
        nid = item['nct_id']
        if nid in combined_data:
            combined_data[nid]["vector"] = item['rank']
        else:
            combined_data[nid] = {"keyword": 0.0, "vector": item['rank']}


    final_results = []
    for nid, scores in combined_data.items():

        weighted_score = (alpha * scores["vector"]) + ((1 - alpha) * scores["keyword"])
        
        final_results.append({
            "nct_id": nid,
            "final_score": weighted_score,
            "breakdown": scores
        })
    final_results = filter_results(final_results, threshold=0.5)
    return sorted(final_results, key=lambda x: x['final_score'], reverse=True)

def filter_results(results, threshold=0.5):
    """
    Filters results based on a final score threshold.
    """
    return [res for res in results if res['final_score'] >= threshold]

if __name__ == "__main__":
    combined_results = hybrid_retriever(keyword_output, vector_output, alpha=0.5)
    for res in combined_results:
        print(res)
# Output
# {'nct_id': 'NCT06670196', 'final_score': 0.8472808895, 'breakdown': {'keyword': 0.694561839, 'vector': 0.99999994}}
# {'nct_id': 'NCT06417814', 'final_score': 0.8447493505, 'breakdown': {'keyword': 0.689498901, 'vector': 0.9999998}}