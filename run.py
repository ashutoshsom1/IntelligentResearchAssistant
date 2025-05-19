"""
Run script for the Intelligent Research Assistant.
"""
import os
import sys
import subprocess
from dotenv import load_dotenv

def check_environment():
    """Check if the environment is properly set up."""
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        print("Please set these keys in your .env file.")
        return False
    
    return True

def run_application():
    """Run the Streamlit application."""
    if not check_environment():
        return
    
    print("Starting Intelligent Research Assistant...")
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {str(e)}")
    except FileNotFoundError:
        print("Error: Streamlit not found. Please make sure it's installed.")
        print("You can install it with: pip install streamlit")

if __name__ == "__main__":
    run_application()
