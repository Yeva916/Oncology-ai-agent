from typing import TypedDict, Optional, List, Any
from langgraph.graph import StateGraph, START, END
from app.demo import generate_response

class AnalysisState(TypedDict):
    """State for the clinical analysis workflow"""
    query: str
    context: Optional[List[Any]]
    response: Optional[str]
    error: Optional[str]

def validate_input(state: AnalysisState) -> AnalysisState:
    """Validate the clinical query input"""
    if not state.get("query") or not state["query"].strip():
        state["error"] = "Clinical query cannot be empty"
        return state
    state["error"] = None
    return state
def get_context(state: AnalysisState) -> AnalysisState:
    """Placeholder for context retrieval logic (if needed)"""
    # In a real implementation, this could fetch additional context based on the query
    
    state["context"] = None
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
    return "generate"

def build_analysis_graph():
    """Build the LangGraph workflow for clinical trial analysis"""
    workflow = StateGraph(AnalysisState)
    
    # Add nodes
    workflow.add_node("validate", validate_input)
    workflow.add_node("generate", generate_analysis)
    
    # Add edges
    workflow.add_edge(START, "validate")
    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "generate": "generate",
            "end_error": END,
        }
    )
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
