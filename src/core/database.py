
import json
import os
from pathlib import Path

from dotenv import load_dotenv

class OncoDatabase:
    _data = None

    @classmethod
    def load_data(cls,file_path:str|None = None):
        
        if cls._data is None:
            print("---Loading Guidelines into Memory---")
            print(file_path)
            full_path = Path(file_path).resolve()
            
            with open(full_path,'r') as f:
                cls._data = json.load(f)
        
        return cls._data

    @classmethod
    def lookup(cls,gene:str,mutation:str):
        db = cls.load_data()

        gene_data = db.get(gene,{})[mutation]
        return gene_data

if __name__ == "__main__":
    load_dotenv()
    # print(type(os.getenv("DATA_DIR")))
    data = OncoDatabase.load_data(os.getenv("DATA_DIR"))
    
    # print(os.getenv("DATA_DIR"))
    gene_data = data.get("EGFR",{})["L858R"]
    print(gene_data)
