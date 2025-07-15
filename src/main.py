from agents.planning_agent import query_or_respond
from agents.retrieval_agent import query_nasa_api
from agents.synthesizing_agent import generate_query_with_context
from utils.setup_llm import setup_groq_llm
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

st.title("NASA Tech Info System")
st.write("Here you can enter a query related to NASA patents and technology transfer!")

user_query = st.text_input("Enter your query:")

if user_query:
    tools = ToolNode([query_nasa_api])

    llm = setup_groq_llm()
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(
        "query_or_respond", query_or_respond(llm=llm, retrieval_tool=query_nasa_api)
    )
    graph_builder.add_node("tools", tools)
    graph_builder.add_node(
        "generate_query_with_context",
        generate_query_with_context(query=user_query, llm=llm),
    )

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond", tools_condition, {END: END, "tools": "tools"}
    )
    graph_builder.add_edge("tools", "generate_query_with_context")
    graph_builder.add_edge("generate_query_with_context", END)

    memory = MemorySaver()
    app = graph_builder.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "1"}}

    nodes = ["query_or_respond", "tools", "generate_query_with_context"]

    for step in app.stream(
        {
            "messages": [
                (
                    "system",
                    "You are a helpful NASA assistant. You can use the tools to answer questions.",
                ),
                ("human", user_query),
            ]
        },
        config=config,
    ):
        print(f"Step entered: {step}")
        for node in nodes:
            if node in step and step[node]["messages"]:
                node_messages = step[node]["messages"]
                print(f"The step messages are {node_messages}")
                last_message = node_messages[-1]
                if hasattr(last_message, "content") and node == "generate_query_with_context":
                    st.write(f"{last_message.content}")
                # else:
                #     st.info(f"The last message is {last_message}")

            # else:
            #     st.warning("No messages returned")
