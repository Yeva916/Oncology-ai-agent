from app.ingestion.data_ingestion import fetch_clinical_trials_data
from app.ingestion.db_integration import save_clinical_trial_data_to_postgres, save_clinical_trials_data_to_vector_db
from app.ingestion.query_builder import generate_clinical_trials_query
def run_pipeline(search_term, vector_client):
    # Step 1: Fetch clinical trials data
    print("Generating query for clinical trials data...")
    query = generate_clinical_trials_query(search_term)
    print("Fetching clinical trials data...")
    clinical_trials_data = fetch_clinical_trials_data(query, page_size=5)  

    # Step 2: Save data to PostgreSQL
    print("Saving clinical trials data to PostgreSQL...")
    save_clinical_trial_data_to_postgres(clinical_trials_data)

    # Step 3: Save data to Vector Database
    print("Saving clinical trials data to Vector Database...")
    save_clinical_trials_data_to_vector_db(clinical_trials_data, vector_client)
    print("Ingestion Pipeline execution completed.")
