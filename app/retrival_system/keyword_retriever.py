from sqlalchemy import func, select

from app.db.postgres_db.models import ClinicalTrial
from app.db.postgres_db.session import get_db


def keyword_retriever(search_query, limit=10):
    """Return keyword-ranked clinical trials for a search query."""
    ts_query = func.websearch_to_tsquery("english", search_query)
    search_rank = func.ts_rank(ClinicalTrial.search_vector, ts_query)
    db = next(get_db())

    query = (
        select(ClinicalTrial, search_rank.label("rank"))
        .where(ClinicalTrial.search_vector.bool_op("@@")(ts_query))
        .order_by(search_rank.desc())
        .limit(limit)
    )

    results = db.execute(query).all()
    output = []
    for row_obj in results:
        trial = row_obj.ClinicalTrial
        output.append({
            "nct_id": trial.nct_id,
            "rank": row_obj.rank,
        })
    # print(f"Keyword Retriever Output for query '{search_query}': {output}")
    return output