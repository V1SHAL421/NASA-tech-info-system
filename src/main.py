from agents.planning_agent import query_or_respond
from agents.retrieval_agent import query_nasa_api
from utils.setup_llm import setup_openai_llm
from langgraph.graph import MessagesState, StateGraph


llm = setup_openai_llm()
graph_builder = StateGraph(MessagesState)
graph_builder.add_node(query_or_respond(llm=llm, retrieval_tool=query_nasa_api()))