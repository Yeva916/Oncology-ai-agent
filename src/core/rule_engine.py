from .validator import InputData
from .database import OncoDatabase
from dotenv import load_dotenv
import os

def rule_engine(input_data:InputData,gene:str = "EGFR"):
    mutation = input_data.mutation.value
    gene_data = OncoDatabase.lookup(gene, mutation)
    drugs = []
    therapy = gene_data.get("therapy",{})
    for type_, drug in therapy.items():
        if isinstance(drug, list):

            for d in drug:
                drugs.append({"drug": d, "type": type_})
        else:
            drugs.append({"drug": drug, "type": type_})

    return drugs

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
    [
    {'drug': 'Osimertinib', 'type': 'first_line'}, 
    {'drug': 'Erlotinib', 'type': 'alternative'}, 
    {'drug': 'Gefitinib', 'type': 'alternative'}
    ]
    """


""""therapy": {
        "first_line": "Osimertinib",
        "alternative": ["Erlotinib", "Gefitinib"]
      }"""