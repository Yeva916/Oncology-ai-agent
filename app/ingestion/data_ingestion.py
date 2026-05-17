import requests

def fetch_clinical_trials_data(term,page_size=1):
    url = "https://clinicaltrials.gov/api/v2/studies"

    # 2. Organize your fields into a single comma-separated string
    fields_list = [
        "protocolSection.identificationModule.nctId",
        "protocolSection.identificationModule.briefTitle",
        "protocolSection.armsInterventionsModule.interventions",
        "protocolSection.descriptionModule.briefSummary",
        "protocolSection.conditionsModule.conditions",
        "protocolSection.eligibilityModule", #amendments protocolSection.eligibilityModule.eligibilityCriteria -> protocolSection.eligibilityModule
        "protocolSection.designModule.phases",
        "protocolSection.contactsLocationsModule.locations"
    ]

    # 3. Define the parameters
    # Note: Use 'query.term' for general search expressions in API v2
    params = {
        "query.term": term,#"lung cancer AND EGFR"
        "filter.overallStatus": "RECRUITING",
        "pageSize": page_size,
        "fields": ",".join(fields_list)
    }

    try:
        # 4. Execute the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # 5. Parse the JSON data
        data = response.json()
        # Example: Print the title of the first study found
        # if "studies" in data and len(data["studies"]) > 0:
        #     with open("app/data/clinical_trials_results.json", "w", encoding="utf-8") as f:
        #         # json.(data, f, indent=4)
        #         json.dump(data, f, indent=4)
        #     first_study = data["studies"][0]
        #     title = first_study['protocolSection']['identificationModule']['briefTitle']
        #     print(f"First Study Found: {title}")
        # else:
        #     print("No studies found matching the criteria.")
        
        if "studies" in data and len(data["studies"]) > 0:
            print(f"Successfully fetched {len(data.get('studies', []))} studies from ClinicalTrials.gov.")
            return data
        else:
            raise ValueError("No studies found matching the criteria.")
        

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
        # print(f"HTTP error occurred: {err}")
    except Exception as err:
        raise SystemExit(err)
        # print(f"An error occurred: {err}")