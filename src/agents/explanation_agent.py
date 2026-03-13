from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from typing import Annotated,TypedDict
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import json
# import os
# from core.rule_engine import rule_engine
# from core.validator import InputData
load_dotenv()

model = GoogleGenerativeAI(model="gemini-2.5-flash")
class AgentState(TypedDict):
    message: BaseMessage

def explanation_agent(state:Annotated[AgentState, "The state of the agent, containing the message to be processed."]) -> Annotated[BaseMessage, "The response message from the agent, providing an explanation based on the input message."]:
    message = state["message"]
    data = json.loads(message.content)
    analysis_prompt = """
    You are an oncology explanation assistant.

    Your task is to explain why a specific therapy was recommended for a cancer mutation.

    IMPORTANT RULES:
    - Do NOT change the recommended therapy.
    - Do NOT invent additional drugs or treatments.
    - Use only the provided information.
    - Provide a short, clear clinical explanation.

    Patient Genomic Information:
    Gene: {gene}
    Mutation: {mutation}
    Cancer Type: {cancer_type}

    Recommended Therapy:
    {recommended_therapy}

    Evidence Level:
    {evidence_level}

    Mutation Description:
    {mutation_description}

    Write a concise explanation describing:
    1. What the mutation does biologically.
    2. Why the recommended therapy targets this mutation.
    3. Why this therapy is appropriate for this cancer type.

    Limit the explanation to 4-6 sentences.
    """

    # print(analysis_prompt.format(**data))
    return model.invoke([HumanMessage(content=analysis_prompt.format(**data))])


