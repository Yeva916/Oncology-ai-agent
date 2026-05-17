from typing import TypedDict, Optional, Any, List
from langgraph.graph import StateGraph, START, END

from app.db.vector_db.client import VectorClient
from app.context_builder.context import build_context
from app.demo import generate_response
from app.ingestion.pipeline import run_pipeline
from app.retrival_system.final_retriever import final_retriever

class AnalysisState(TypedDict):
    """State for the clinical analysis workflow"""
    query: str
    context: Optional[Any]
    response: Optional[str]
    error: Optional[str]

def validate_input(state: AnalysisState) -> AnalysisState:
    """Validate the clinical query input"""
    if not state.get("query") or not state["query"].strip():
        state["error"] = "Clinical query cannot be empty"
        return state
    state["error"] = None
    return state


def ingest_query(state: AnalysisState) -> AnalysisState:
    """Run the ingestion pipeline for the current query."""
    try:
        if state.get("error"):
            return state

        vector_client = VectorClient()
        run_pipeline(state["query"], vector_client)
    except Exception as exc:
        state["error"] = f"Ingestion pipeline failed: {str(exc)}"

    return state


def retrieve_context(state: AnalysisState) -> AnalysisState:
    """Build retrieval results that will be passed into analysis generation."""
    try:
        if state.get("error"):
            return state

        retrieved_trials = final_retriever(state["query"])
        state["context"] = build_context(retrieved_trials, state["query"])
    except Exception as exc:
        state["error"] = f"Context retrieval failed: {str(exc)}"

    return state


def generate_analysis(state: AnalysisState) -> AnalysisState:
    """Generate trial analysis using LLM"""
    try:
        if state.get("error"):
            return state
        
        query = state["query"]
        context = state.get("context") or []
        
        response = generate_response(query, context)
        state["response"] = response
        
    except Exception as e:
        state["error"] = f"Analysis generation failed: {str(e)}"
    
    return state

def should_continue(state: AnalysisState) -> str:
    """Route based on whether there was an error"""
    if state.get("error"):
        return "end_error"
    return "ingest"

def build_analysis_graph():
    """Build the LangGraph workflow for clinical trial analysis"""
    workflow = StateGraph(AnalysisState)
    
    # Add nodes
    workflow.add_node("validate", validate_input)
    workflow.add_node("ingest", ingest_query)
    workflow.add_node("retrieve", retrieve_context)
    workflow.add_node("generate", generate_analysis)
    
    # Add edges
    workflow.add_edge(START, "validate")
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "ingest": "ingest",
            "end_error": END,
        }
    )
    workflow.add_edge("ingest", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()

# Compile the graph
analysis_graph = build_analysis_graph()

def run_analysis(query: str, context: Optional[List[Any]] = None) -> dict:
    """
    Run the clinical analysis workflow
    
    Args:
        query: Clinical patient query/description
        context: Optional context data (trial scores, etc.)
    
    Returns:
        dict with response and error (if any)
    """
    initial_state: AnalysisState = {
        "query": query,
        "context": context or [],
        "response": None,
        "error": None,
    }
    
    # Run the graph
    result = analysis_graph.invoke(initial_state)
    
    return {
        "response": result.get("response"),
        "error": result.get("error"),
        "query": result.get("query"),
    }
