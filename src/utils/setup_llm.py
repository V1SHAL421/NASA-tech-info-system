from langchain_openai import ChatOpenAI
import streamlit as st


def setup_groq_llm(expt_llm="llama-3.1-8b-instant", temperature=0.2):
    assert st.secrets.get("GROQ_API_KEY") is not None, (
        "GROQ_API_KEY is not set. Please set it in .env file"
    )

    llm = ChatOpenAI(
        model=expt_llm,
        temperature=temperature,
        max_completion_tokens=1000,
        verbose=True,
        timeout=None,
        api_key=st.secrets.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    return llm
