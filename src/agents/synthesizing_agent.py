from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI


def generate_query_with_context(query: str, llm: ChatOpenAI):
    def agent(state: MessagesState):
        """Generate answer"""
        recent_tool_messages = []
        for message in reversed(state["messages"]):
            if message.type == "tool":
                recent_tool_messages.append(message)
            else:
                break
        tool_messages = recent_tool_messages[::-1]

        docs_content = "\n\n".join(doc.content for doc in tool_messages)
        context = f"Context: {docs_content}"
        augmented_query = f"""You are a helpful assistant on NASA projects.
        The user has asked: {query}. Use the following retrieved context
        to answer

        {context}
        """
        conversation_messages = [
            message
            for message in state["messages"]
            if message.type in ("human", "system")
            or (message.type == "ai" and not message.tool_calls)
        ]

        prompt = [SystemMessage(augmented_query)] + conversation_messages

        response = llm.invoke(prompt)
        return {"messages": [response]}

    return agent
