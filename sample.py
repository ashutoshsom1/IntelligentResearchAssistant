from langchain_openai import AzureChatOpenAI
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.messages import HumanMessage
import os

class Answer(BaseModel):
    answer: str

llm = AzureChatOpenAI(
    azure_deployment="gpt-35-turbo-16k",  # Replace with your deployment name
    temperature=0,
    azure_endpoint="https://openaitest-005.openai.azure.com/",
    api_version="2024-10-21",
    api_key="dfc1185767ac474c9be05d2ac537f410"
)


structured_llm = llm.with_structured_output(Answer)

response = structured_llm.invoke([HumanMessage(content="What is the capital of France?")])
print(response.answer)
