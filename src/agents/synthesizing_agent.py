from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

def generate_query_with_context(state: MessagesState, query: str, llm: ChatOpenAI):
    """Generate answer"""
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.page_content for doc in tool_messages)
    context = f"Context: {docs_content}"
    augmented_query = (
        query,
        context
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]

    prompt = [SystemMessage(augmented_query)] + conversation_messages

    response = llm.invoke(prompt)
    return {"messages": [response]}