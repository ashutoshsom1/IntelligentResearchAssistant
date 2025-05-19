"""
Configuration module for the Intelligent Research Assistant.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# LangSmith configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "intelligent-research-assistant")

# LLM Configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-35-turbo-16k")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0"))

# Research Assistant Configuration
MAX_ANALYSTS = int(os.getenv("MAX_ANALYSTS", "3"))
MAX_SOURCES = int(os.getenv("MAX_SOURCES", "5"))
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "3"))
