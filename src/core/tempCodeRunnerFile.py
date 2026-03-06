data = OncoDatabase.load_data(os.getenv("DATA_DIR"))
    
    print(os.getenv("DATA_DIR"))
    gene_data = data.get("EGFR")
    print(gene_data)
