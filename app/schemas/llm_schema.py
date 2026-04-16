from typing import List, Optional
from pydantic import BaseModel, Field

class ClinicalTrialSchema(BaseModel):
    condition: str = Field(description="The specific cancer type, e.g., NSCLC")
    stage: str = Field(description="The disease stage, e.g., Stage III Unresectable")
    
    # Genomic Markers
    required_mutations: List[str] = Field(description="Mutations required for entry (e.g., Ex19Del, L858R)")
    permitted_mutations: List[str] = Field(description="Mutations allowed but not required (e.g., T790M)")
    
    # Eligibility Logic
    inclusion_rules: List[str] = Field(description="Key clinical inclusion criteria")
    exclusion_rules: List[str] = Field(description="Key clinical exclusion criteria")

class PatientQuerySchema(BaseModel):
    pass
