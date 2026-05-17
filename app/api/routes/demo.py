from fastapi import APIRouter, HTTPException

from app.demo import generate_demo_response

router = APIRouter()


@router.get("/demo")
def demo():
    """Run demo analysis with sample clinical data using the mock demo response."""
    try:
        user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
        context = [
            {"nct_id": "NCT06116682", "final_score": 0.8472808895},
            {"nct_id": "NCT06538038", "final_score": 0.8447493505},
        ]
        
        return {"response": generate_demo_response(user_query, context)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
