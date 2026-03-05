"""
input schema 
input = {
    mutation:"",
    cancer_type:"",
}
"""
from pydantic import BaseModel, ValidationError,Field
from enum import Enum

class MutationType(str, Enum):
    EGFR_EXON_19 = "Exon 19 deletion"  
    EGFR_L858R = "L858R"
    EGFR_T790M = "T790M"

class CancerType(str,Enum):
    NSCLC = "nsclc"
class InputData(BaseModel):
    mutation:MutationType = Field(..., description="The mutation identifier")
    cancer_type:CancerType = Field(..., description="The type of cancer")


def validate_input(input_data):
   try:
       validate_input = InputData(**input_data)
       return validate_input
   except ValidationError as e:
       print(f"Total errors found: {len(e.errors())}")
       print(e.json())

if __name__ == "__main__":
    input_data = {
        "mutation": "Exon 19 deletion",
        "cancer_type": "lungs"
    }
    validated_data = validate_input(input_data)
    print(validated_data)

    """
    output:
    
    valid data -> mutation=<MutationType.EGFR_EXON_19: 'Exon 19 deletion'> cancer_type=<CancerType.NSCLC: 'nsclc'>
    
    
    invalid data -> 
    Total errors found: 1
    [{"type":"enum","loc":["cancer_type"],"msg":"Input should be 'nsclc'","input":"lungs","ctx":{"expected":"'nsclc'"},"url":"https://errors.pydantic.dev/2.12/v/enum"}]
    """
