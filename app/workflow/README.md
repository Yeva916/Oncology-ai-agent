# LangGraph Workflow - Clinical Trial Analysis

This module implements a LangGraph-based workflow orchestrator for the clinical trial analysis pipeline.

## Architecture

The workflow is built using **LangGraph**, a framework for building multi-step AI agent flows with state management.

### Workflow Steps

1. **Validate** — Validate the clinical query input
2. **Generate** — Generate trial analysis using LLM (calls `app.demo.generate_response`)
3. **Error Handling** — Gracefully handle errors and return error state

### Flow Diagram

```
START
  ↓
validate (check query)
  ↓
should_continue?
  ├─→ if error → END (with error)
  └─→ if valid → generate (LLM analysis)
       ↓
      END (with response)
```

## Usage

### In Routes

```python
from app.workflow import run_analysis

# Simple call
result = run_analysis(
    query="Patient with advanced NSCLC, age 65, ECOG 1...",
    context=[{"nct_id": "NCT06116682", "final_score": 0.85}]
)

# Returns
{
    "response": "Trial ID: NCT06116682\nRelevance: Low\n...",
    "error": None,  # or error message if occurred
    "query": "..."
}
```

### Direct Graph Access

```python
from app.workflow import analysis_graph

# Invoke graph directly with state
state = {
    "query": "...",
    "context": [],
    "response": None,
    "error": None
}

result = analysis_graph.invoke(state)
```

## Integration Points

- **`/api/analyze`** — Uses workflow via `run_analysis()`
- **`/api/demo`** — Uses workflow via `run_analysis()` with sample data
- **`/api/debug`** — Can be extended to output full workflow state

## Extension Points

### Add Custom Nodes

Edit `app/workflow/analysis_graph.py` to add nodes:

```python
def my_custom_step(state: AnalysisState) -> AnalysisState:
    # your logic
    return state

workflow.add_node("my_step", my_custom_step)
```

### Add Context Enrichment

Add a retrieval step before generation:

```python
def retrieve_trials(state: AnalysisState) -> AnalysisState:
    # call retrieval system
    state["context"] = results
    return state

workflow.add_node("retrieve", retrieve_trials)
workflow.add_edge("validate", "retrieve")
workflow.add_edge("retrieve", "generate")
```

## Dependencies

- `langgraph>=1.0.10` (already in pyproject.toml)
- `langchain>=1.2.10`
- `langchain-google-genai>=4.2.1` (for LLM generation)

## State Schema

```python
class AnalysisState(TypedDict):
    query: str                    # Clinical query
    context: Optional[List[Any]]  # Trial context (scores, etc.)
    response: Optional[str]       # Generated analysis
    error: Optional[str]          # Error message if any
```
