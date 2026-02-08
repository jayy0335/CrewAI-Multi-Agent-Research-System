"""Configuration settings for the CrewAI project"""
import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai import LLM

# Load environment variables
load_dotenv()

# Access the environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GROK_KEY = os.getenv("GROK_KEY")

# Configure LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=512,   # Response limit
    timeout=120,
    api_key=GROK_KEY
)

# Initialize search tool
search_tool = SerperDevTool()
