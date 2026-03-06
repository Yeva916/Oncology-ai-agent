
import json
from pathlib import Path

class OncoDatabase:
    _data = None

    @classmethod
    def load_data(cls,file_path:str):
        
        if cls._data is None:
            print("---Loading Guidelines into Memory---")
            full_path = Path(file_path).resolve()
            with open(full_path,'r') as f:
                cls._data = json.load(f)
        
        return cls._data

    @classmethod
    def lookup(cls,gene:str):
        db = cls.load_data()

        gene_data = db.get(gene)
        return gene_data

if __name__ == "__main__":
    data = OncoDatabase.load_data("./data/mutation_db.json")
    gene_data = data.get("EGFR")
    print(gene_data)
