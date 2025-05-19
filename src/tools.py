"""
Tools for the Intelligent Research Assistant.
"""
import os
from typing import List, Dict, Any, Optional

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_core.tools import BaseTool, StructuredTool, tool

from src.config import TAVILY_API_KEY

# Set Tavily API key
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

class ResearchTools:
    """Collection of tools for research."""
    
    @staticmethod
    def get_web_search_tool() -> BaseTool:
        """Get a tool for web search using Tavily."""
        return TavilySearchResults(max_results=5)
    
    @staticmethod
    @tool
    def search_wikipedia(query: str) -> str:
        """Search Wikipedia for information on a topic."""
        wikipedia = WikipediaAPIWrapper()
        return wikipedia.run(query)
    
    @staticmethod
    def get_all_tools() -> List[BaseTool]:
        """Get all available research tools."""
        return [
            ResearchTools.get_web_search_tool(),
            ResearchTools.search_wikipedia,
        ]
