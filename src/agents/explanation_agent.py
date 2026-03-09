from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from typing import Annotated,TypedDict
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
# import os
# from core.rule_engine import rule_engine
# from core.validator import InputData
load_dotenv()

model = GoogleGenerativeAI(model="gemini-2.5-flash")
class AgentState(TypedDict):
    message: BaseMessage

def explanation_agent(state:Annotated[AgentState, "The state of the agent, containing the message to be processed."]) -> Annotated[BaseMessage, "The response message from the agent, providing an explanation based on the input message."]:
    message = state["message"]
    analysis_prompt = """
    You are an expert Oncology Agent.
    Please analyze the following message and provide a clear and concise explanation:
    {message}
"""
    return model.invoke([HumanMessage(content=analysis_prompt.format(message=message.content))])


