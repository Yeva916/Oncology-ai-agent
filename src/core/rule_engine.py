from .validator import InputData
from .database import OncoDatabase
from dotenv import load_dotenv
import os

def rule_engine(input_data:InputData,gene:str = "EGFR"):
    mutation = input_data.mutation.value
    gene_data = OncoDatabase.lookup(gene, mutation)
    therapy = gene_data.get("therapies",[])
    return {
        "gene": gene,
        "mutation": mutation,
        "therapy": therapy
    }

if __name__ == "__main__":
    load_dotenv()
    print(os.getenv("DATA_DIR"))
    OncoDatabase.load_data(os.getenv("DATA_DIR"))

    input_data = {
        "mutation": "L858R",
        "cancer_type": "nsclc"
    }
    validated_data = InputData(**input_data)
    result = rule_engine(validated_data)
    print(result)
    
    