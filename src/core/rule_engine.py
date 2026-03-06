from validator import InputData
from database import OncoDatabase
from dotenv import load_dotenv
import os

def rule_engine(input_data:InputData,gene:str = "EGFR"):
    mutation = input_data.mutation.value
    gene_data = OncoDatabase.lookup(gene, mutation)
    return gene_data

if __name__ == "__main__":
    load_dotenv()
    print(os.getenv("DATA_DIR"))
    OncoDatabase.load_data(os.getenv("DATA_DIR"))

    input_data = {
        "mutation": "Exon19del",
        "cancer_type": "nsclc"
    }
    validated_data = InputData(**input_data)
    result = rule_engine(validated_data)
    print(result)
    
    """
    ouput:
    {'protein_change': ['E746_A750del'], 'cancer_type': 'NSCLC', 'therapy': {'first_line': 'Osimertinib', 'alternative': ['Erlotinib', 'Gefitinib']}, 'evidence_level': 'High', 'description': 'EGFR exon 19 deletion activates the EGFR signaling pathway and responds well to EGFR tyrosine kinase inhibitors.'}
    """


