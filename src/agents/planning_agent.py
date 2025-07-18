from typing import Callable
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState


def query_or_respond(llm: ChatOpenAI, retrieval_tools: Callable[[str], dict]):
    def agent(state: MessagesState):
        """Respond or generate a tool call for retrieval"""
        llm_with_tools = llm.bind_tools([tool for tool in retrieval_tools])
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    return agent
