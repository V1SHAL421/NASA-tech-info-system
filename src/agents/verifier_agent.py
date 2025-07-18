from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage

def verifier_response(llm: ChatOpenAI):
    def agent(state: MessagesState):
        last_message = state["messages"][-1].content
        verification_prompt = f"Is the following answer grounded in factual context?\n\nAnswer: {last_message}\n\nRespond with 'Yes' or 'No' and explain briefly."
        verification_result = llm.invoke([SystemMessage(content=verification_prompt)])
        print("Verification result:", verification_result.content)
        return {"messages": [verification_result]}
    return agent