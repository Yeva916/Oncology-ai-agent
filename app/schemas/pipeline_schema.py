from typing import List, Literal
from pydantic import BaseModel, Field
from util import AffinityScore, ClinicalTrialEntry, FinalAffinitySummary, FinalValidation, GraphOutputEntry, KnowledgeEntry, Mutation,FinalTrialSummary

class GenomicInputSchema(BaseModel):
    vcf_file:str

class GenomicOutputSchema(BaseModel):
    mutations:List[Mutation] = Field(default_factory=list)

class ClinicalKnowledgeInputSchema(BaseModel):
    mutations:List[str] = Field(default_factory=list)
    cancer_type:str

class ClinicalKnowledgeOutputSchema(BaseModel):
    entries:List[KnowledgeEntry] = Field(default_factory=list)
    
class ClinicalTrialsInputSchema(BaseModel):
    mutations:List[str] = Field(default_factory=list)
    gene:str
    cancer_type:str

class ClinicalTrialsOutputSchema(BaseModel):
    results:List[ClinicalTrialEntry] = Field(default_factory=list)

class KnowlegeGraphInputSchema(BaseModel):
    mutations:List[str] = Field(default_factory=list)

class KnowledgeGraphOutputSchema(BaseModel):
    relations:List[GraphOutputEntry] = Field(default_factory=list)

class ReasoningInputSchema(BaseModel):
    mutations:List[Mutation] = Field(default_factory=list,description="List of validated mutations from the VCF layer")
    knowledge:List[KnowledgeEntry] = Field(default_factory=list,description="Retrieved clinical evidence and therapy guidelines")
    trials:List[ClinicalTrialEntry] = Field(default_factory=list,description="Matching active trials for the patient's profile")
    graph:List[GraphOutputEntry] = Field(default_factory=list,description="Knowledge graph triples showing gene-drug interactions")

class ReasoningOutputSchema(BaseModel):
    recommended_therapy:str = Field(...,description="The top-ranked treatment based on clinical evidence")
    alternative_therapies:List[str] = Field(default_factory=list,description="Other viable treatments or secondary lines of therapy")
    matched_mutations:List[str] = Field(default_factory=list,description="The specific variants that justified this therapy choice")
    confidence_score:Literal["low", "medium", "high"] = Field(...,description="The strength of the underlying evidence (guidelines vs trials)")
    explanation:str = Field(...,description="A concise clinical summary for the oncologist")
    decision_trace:List[str] = Field(default_factory=list,description="A step-by-step trace of how the agent reached the conclusion")

class DockingInputSchema(BaseModel):
    mutation:List[str] = Field(default_factory=list,description="The specific variant(s) to evaluate for drug binding")
    therapy:str = Field(...,description="The drug for which to predict binding affinity")
    protein:str = Field(...,description="The target protein for docking simulations")


class DockingOutputSchema(BaseModel):
    score:List[AffinityScore] = Field(default_factory=list,description="Predicted binding affinity scores for the mutation-therapy pair")

class ValidationInputSchema(BaseModel):
    mutation:str = Field(...,description="The specific variant to validate")
    therapy:str = Field(...,description="The recommended therapy to validate against clinical guidelines")
    cancer_type:str = Field(...,description="The patient's cancer type for guideline matching")

class ValidationOutputSchema(BaseModel):
    approved:bool = Field(...,description="Whether the therapy is FDA-approved for this mutation and cancer type")
    guideline_match:bool = Field(...,description="Whether the recommendation aligns with NCCN or ESMO guidelines")
    warnings:List[str] = Field(default_factory=list,description="Any safety concerns or contraindications based on the mutation profile")
    reasons:List[str] = Field(default_factory=list,description="Clinical rationale for any mismatches with guidelines or approvals")
    evidence_level:Literal["low", "medium", "high"] = Field(...,description="The overall confidence in the recommendation based on validation results")

class PipelineOutputSchema(BaseModel):
    patient_id:str
    therapy:str
    confidence:Literal["low", "medium", "high"]
    explanation:str
    matched_mutations:List[str] = Field(default_factory=list)
    affinity:FinalAffinitySummary
    validation:FinalValidation
    clinical_trials:List[FinalTrialSummary]


