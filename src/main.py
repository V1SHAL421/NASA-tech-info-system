from agents.planning_agent import query_or_respond
from agents.retrieval_agent import query_nasa_api
from agents.synthesizing_agent import generate_query_with_context
from utils.setup_llm import setup_openai_llm
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

st.title("NASA Tech Info System")
st.write("Here you can enter a query related to NASA patents and technology transfer!")

tools = ToolNode([query_nasa_api])

llm = setup_openai_llm()
graph_builder = StateGraph(MessagesState)
graph_builder.add_node(query_or_respond(llm=llm, retrieval_tool=query_nasa_api()))
graph_builder.add_node(tools)
graph_builder.add_node(generate_query_with_context)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"}
)
graph_builder.add_edge("tools", "generate_query_with_context")
graph_builder.add_edge("generate_query_with_context", END)

memory = MemorySaver()
app = graph_builder.compile(checkpoint=memory)

config = {"configurable": {"thread_id": "1"}}

user_query = st.text_input("Enter your query:")

if user_query:
    for step in app.stream(
        {"messages": [
            ("system", "You are a helpful assistant. You can use the tools to answer questions."),
            ("human", user_query),
        ]},
        config=config,
    ):
        step["messages"][-1].pretty_print()