from langchain_google_genai import ChatGoogleGenerativeAI

from app.context_builder.context import build_context
from app.prompts.context import context_prompt

def generate_response(user_query, context):
    print("Generating response using LLM...")
    llm = ChatGoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)
    trial_context = context if isinstance(context, str) else build_context(context, user_query)
    chain = context_prompt | llm
    response = chain.invoke({"user_query": user_query, "context": trial_context})
    response_text = getattr(response, "content", response)

    with open("response.txt", "w", encoding="utf-8") as file_handle:
        file_handle.write(str(response_text))

    return str(response_text)

if __name__ == "__main__":
    # Example user query and context
    user_query = "Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1, with no prior systemic therapy."
    context = [{'nct_id': 'NCT06116682', 'final_score': 0.8472808895, 'breakdown': {'keyword': 0.694561839, 'vector': 0.99999994}}, 
               {'nct_id': 'NCT06538038', 'final_score': 0.8447493505, 'breakdown': {'keyword': 0.689498901, 'vector': 0.9999998}}]
    response = generate_response(user_query, context)
    print(response)