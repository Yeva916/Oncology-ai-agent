
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class MetaData(BaseModel):
    patient_id:str
    timestamp:str
    version:str="v1"

class AgentInput(BaseModel):
    vcf_file:Optional[str]=None
    cancer_type:Optional[str]=None

class GenomicData(BaseModel):
    mutations:List[Dict[str,Any]] = Field(default_factory=list)

# mutations = [
#     {"gene": "EGFR", "variant": "L858R", "chromosome": 7}, # Dictionary 1
#     {"gene": "KRAS", "variant": "G12D", "chromosome": 12}  # Dictionary 2
# ]
class KnowledgeGraph(BaseModel):
    entries:List[str] = Field(default_factory=list)
    source: List[str] = Field(default_factory=list)

# knowledge = KnowledgeGraph(
#     entries=[
#         "Osimertinib is preferred for EGFR mutations.", 
#         "Resistance may occur via T790M mutation."
#     ],
#     sources=[
#         "Source A: FDA Label", 
#         "Source B: Clinical Trial NCT0123"
#     ]
# )

class ReasoningData(BaseModel):
    recommended_therapy:Optional[str]=None
    alternative_therapies:List[str] = Field(default_factory=list)
    confidence_score:Optional[float]=None
    explanation:Optional[str]=None
    decision_trace:List[str] = Field(default_factory=list)

class ValidationData(BaseModel):
    approved:Optional[bool]=None
    guideline_match:Optional[bool]=None
    warnings:List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)

class AgentState(BaseModel):
    meta:MetaData = Field(default_factory=MetaData)
    input:AgentInput = Field(default_factory=AgentInput)
    genomic:GenomicData = Field(default_factory=GenomicData)
    knowledge:KnowledgeGraph = Field(default_factory=KnowledgeGraph)
    trials:Dict[str,List] = Field(default_factory=lambda:{"results":[]})
    graph:Dict[str,List] = Field(default_factory=lambda:{"relations":[]})
    reasoning:ReasoningData = Field(default_factory=ReasoningData)
    affinity:Dict[str,Any] = Field(default_factory=lambda:{"score":[]})
    validation:ValidationData = Field(default_factory=ValidationData)
    output:Dict[str,Any] = Field(default_factory=dict)

