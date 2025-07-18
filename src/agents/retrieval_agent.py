import requests
from langchain_core.tools import tool
import streamlit as st


@tool
def query_nasa_techtransfer_api(query):
    """Query NASA TechTransfer API for technology projects"""
    nasa_tech_api_key = st.secrets.get("NASA_API_KEY")
    nasa_url = (
        f"https://api.nasa.gov/techtransfer/patent/?{query}&api_key={nasa_tech_api_key}"
    )
    response = requests.get(nasa_url)
    if response.status_code == 200:
        # print(f"The API responded with {response.json()}")
        data = response.json().get("results", [])
        # title_idx = 2
        summary_idx = 3
        max_context_retrieved = 10
        if len(data) > max_context_retrieved:
            data = data[:max_context_retrieved]

        print(f"The condensed data is {data}")
        data_summary = "\n".join(patent[summary_idx] for patent in data)
        return data_summary
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}


@tool
def query_nasa_images_api(query):
    """Query NASA Images and Video Library API"""
    nasa_images_api_key = st.secrets.get("NASA_API_KEY")
    nasa_url = (
        f"https://images-api.nasa/gov/search?q={query}&api_key={nasa_images_api_key}"
    )
    response = requests.get(nasa_url)
    if response.status_code == 200:
        data = response.json().get("results", [])
        print(f"The API responded with {response.json()}")
        max_context_retrieved = 10
        if len(data) > max_context_retrieved:
            data = data[:max_context_retrieved]

            data_summary = "\n".join(patent for patent in data)
            return data_summary
        else:
            return {
                "error": f"Failed to fetch data. Status code: {response.status_code}"
            }
