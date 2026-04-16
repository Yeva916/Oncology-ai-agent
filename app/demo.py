from langchain_google_genai import GoogleGenerativeAI
from app.context_builder.context import build_context

def generate_response(user_query, context):
    llm = GoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
    context = build_context(context, user_query)
    response = llm.invoke(context)
    with open("response.txt", "w") as f:
        f.write(response)
    return response

if __name__ == "__main__":
    # Example user query and context
    user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
    context = [{'nct_id': 'NCT06116682', 'final_score': 0.8472808895, 'breakdown': {'keyword': 0.694561839, 'vector': 0.99999994}}, 
               {'nct_id': 'NCT06538038', 'final_score': 0.8447493505, 'breakdown': {'keyword': 0.689498901, 'vector': 0.9999998}}]
    response = generate_response(user_query, context)
    print(response)