
from enum import Enum
from typing import List, Literal
from pydantic import BaseModel, Field


class Mutation(BaseModel):
    gene:str
    mutation:str
    full_name:str
    chromosome:str
    position:str
    variant_type:str
    clinical_significance:str=None
    confidence:str

class KnowledgeEntry(BaseModel):
    mutation:str = Field(..., description="The specific variant, e.g., 'L858R'")
    gene:str = Field(..., description="The gene symbol, e.g., 'EGFR'")
    disease:str = Field(..., description="The specific cancer type found in literature")
    therapies:List[str] = Field(default_factory=list)
    resistance:List[str]= Field(default_factory=list)
    evidence_level:Literal["low", "medium", "high"]
    source:str = Field(..., description="DOI, PubMed ID, or Document name")
    text:str = Field(..., description="The raw excerpt from the source text")

class ClinicalTrialEntry(BaseModel):
    trial_id:str= Field(..., description="The NCT ID, e.g., 'NCT01234567'")
    title:str= Field(..., description="Official title of the clinical study")
    mutation_target:str = Field(..., description="The specific variant targeted, e.g., 'L858R'")
    gene:str= Field(..., description="Gene targeted, e.g., 'EGFR'")
    therapy:str= Field(..., description="Experimental or control drug name")
    phase:Literal["Phase 1", "Phase 2", "Phase 3", "Phase 4", "N/A"]= Field(..., description="The phase of the clinical trial")
    status:str= Field(..., description="Recruiting, Active, or Completed")
    eligibility:str = Field(..., description="Summary of key inclusion/exclusion criteria")
    location:str= Field(..., description="Primary site or geographic availability")

class GraphOutputEntry(BaseModel):
    source:str = Field(..., description="The source node, e.g., 'EGFR L858R'")
    target:str = Field(..., description="The target node, e.g., 'Osimertinib'")
    relation:str = Field(..., description="The type of relationship, e.g., 'sensitive to' or 'resistant to'")

class AffinityScore(BaseModel):
    mutation:str = Field(..., description="The specific variant evaluated, e.g., 'L858R'")
    therapy:str = Field(..., description="The drug for which binding affinity was predicted, e.g., 'Osimertinib'")
    binding_score:float = Field(..., description="The predicted binding affinity score from docking simulations")
    confidence:Literal["low", "medium", "high"] = Field(..., description="The confidence level of the docking prediction based on score thresholds")
    method:Literal["proxy","docking","dataset"] = Field(..., description="The method used to calculate the affinity score")

class FinalTrialSummary(BaseModel):
    trail_id:str
    therapy:str
    phase:str

class FinalAffinitySummary(BaseModel):
    binding_score:str = Field(..., description="Qualitative or quantitative score")
    summary:str = Field(..., description="A brief conclusion from the docking layer")

class FinalValidation(BaseModel):
    approved:bool = Field(..., description="Flag for clinical guideline compliance")
    notes:str = Field(..., description="Warnings or specific notes from the validation agent")

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"