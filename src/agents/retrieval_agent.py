import requests
import os
from langchain_core.tools import tool
from dotenv import load_dotenv

@tool
def query_nasa_api(query):
    """Query NASA TechTransfer API for technology projects"""
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')
    nasa_url = f"https://api.nasa.gov/techtransfer/patent/?{query}&api_key={nasa_api_key}"
    response = requests.get(nasa_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}