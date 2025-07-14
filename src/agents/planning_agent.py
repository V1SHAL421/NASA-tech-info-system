from typing import Callable
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState


def query_or_respond(llm: ChatOpenAI, retrieval_tool: Callable[[str], dict]):
    def agent(state: MessagesState):
        """Respond or generate a tool call for retrieval"""
        llm_with_tools = llm.bind_tools([retrieval_tool])
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    return agent
