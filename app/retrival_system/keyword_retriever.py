from sqlalchemy import select,func
from app.db.postgres_db.session import get_db
from app.db.postgres_db.models import ClinicalTrial


def keyword_retriever(search_query):
    # search_query = "non small lung cancer Osimertinib"
    ts_query = func.websearch_to_tsquery('english', search_query)
    search_rank = func.ts_rank(ClinicalTrial.search_vector, ts_query)
    db = next(get_db())
    query = select(
        ClinicalTrial,
        search_rank.label('rank')
                ).where(ClinicalTrial.search_vector.bool_op('@@')(ts_query)
                        ).order_by(search_rank.desc()
                                    ).limit(10)

    results = db.execute(query).all()
    # print(results)
    output = []
    for row_obj in results:
        trial = row_obj.ClinicalTrial
        score = row_obj.rank
        output.append({
            "nct_id": trial.nct_id,
            "rank": score
        })
    #     print(f"NCI ID: {trial.nct_id}, Title: {trial.brief_title}, Rank: {score}")
    return output

print(keyword_retriever("non small lung Osimertinib"))
#output
# [{'nct_id': 'NCT06670196', 'rank': 0.99999994}, {'nct_id': 'NCT06417814', 'rank': 0.9999998}]