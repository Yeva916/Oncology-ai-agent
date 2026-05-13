from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.workflow import run_analysis


router = APIRouter()


class AnalyzeRequest(BaseModel):
    query: str
    context: Optional[List[Any]] = None


@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Analyze clinical query using LangGraph workflow"""
    try:
        result = run_analysis(req.query, req.context or [])
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {"response": result["response"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
