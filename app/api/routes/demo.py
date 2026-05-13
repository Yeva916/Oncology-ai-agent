from fastapi import APIRouter, HTTPException

from app.workflow import run_analysis

router = APIRouter()


@router.get("/demo")
def demo():
    """Run demo analysis with sample clinical data using LangGraph workflow"""
    try:
        user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
        context = [
            {"nct_id": "NCT06116682", "final_score": 0.8472808895},
            {"nct_id": "NCT06538038", "final_score": 0.8447493505},
        ]
        
        result = run_analysis(user_query, context)
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {"response": result["response"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
