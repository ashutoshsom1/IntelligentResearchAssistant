"""
Test script for the Intelligent Research Assistant.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if required API keys are set
required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
    print("Please set these keys in your .env file.")
    sys.exit(1)

# Import components
from src.config import DEFAULT_MODEL, MAX_ANALYSTS
from src.models import Analyst, Source
from src.components import create_analysts, plan_research, conduct_interviews, generate_report
from src.graph import create_research_assistant_graph

def test_analyst_generation():
    """Test the analyst generation component."""
    print("\n=== Testing Analyst Generation ===")
    
    # Create test state
    state = {
        "topic": "The impact of artificial intelligence on healthcare",
        "max_analysts": 2,
        "human_analyst_feedback": ""
    }
    
    # Generate analysts
    try:
        result = create_analysts(state)
        analysts = result.get("analysts", [])
        
        if not analysts:
            print("Error: No analysts generated.")
            return False
        
        print(f"Successfully generated {len(analysts)} analysts:")
        for analyst in analysts:
            print(f"- {analyst.name}: {analyst.role} ({analyst.affiliation})")
        
        return True
    except Exception as e:
        print(f"Error generating analysts: {str(e)}")
        return False

def test_research_planning(analysts):
    """Test the research planning component."""
    print("\n=== Testing Research Planning ===")
    
    # Create test state
    state = {
        "topic": "The impact of artificial intelligence on healthcare",
        "analysts": analysts
    }
    
    # Generate research questions
    try:
        result = plan_research(state)
        questions = result.get("research_questions", [])
        
        if not questions:
            print("Error: No research questions generated.")
            return False
        
        print(f"Successfully generated {len(questions)} research questions:")
        for i, question in enumerate(questions):
            print(f"{i+1}. {question.question} (by {question.analyst.name})")
        
        return questions
    except Exception as e:
        print(f"Error generating research questions: {str(e)}")
        return False

def test_graph_creation():
    """Test the graph creation."""
    print("\n=== Testing Graph Creation ===")
    
    try:
        graph = create_research_assistant_graph()
        print("Successfully created research assistant graph.")
        return True
    except Exception as e:
        print(f"Error creating graph: {str(e)}")
        return False

def main():
    """Run tests for the Intelligent Research Assistant."""
    print("Starting tests for Intelligent Research Assistant...")
    
    # Test analyst generation
    analysts = test_analyst_generation()
    if not analysts:
        print("Analyst generation test failed.")
        return
    
    # Test research planning
    questions = test_research_planning(analysts)
    if not questions:
        print("Research planning test failed.")
        return
    
    # Test graph creation
    if not test_graph_creation():
        print("Graph creation test failed.")
        return
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main()
