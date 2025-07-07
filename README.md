# Intelligent Research Assistant

An advanced AI-powered research assistant that helps you conduct in-depth research on any topic using multiple AI analysts with different perspectives.

## Features

- **Multi-Analyst Approach**: Creates a team of AI analysts, each with a unique perspective and expertise relevant to your research topic.
- **Human-in-the-Loop**: Review and provide feedback at each stage of the research process.
- **Diverse Information Sources**: Utilizes web search and Wikipedia to gather comprehensive information.
- **Structured Research Process**: Follows a systematic approach from planning to report generation.
- **Interactive UI**: User-friendly Streamlit interface for easy interaction.

## Architecture

The application is built using LangGraph, a framework for creating complex, stateful workflows with LLMs. The research process is structured as a graph with the following main components:

1. **Analyst Generation**: Creates a team of AI analysts based on the research topic.
2. **Research Planning**: Generates specific research questions for each analyst.
3. **Interview Conducting**: Simulates interviews between analysts and experts using various information sources.
4. **Report Generation**: Synthesizes the findings into a comprehensive research report.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/intelligent-research-assistant.git
cd intelligent-research-assistant
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
conda activate intelligent-research-assistant   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Enter your research topic in the sidebar and configure the number of analysts and information sources.

3. Click "Start Research" to begin the process.

4. Review and provide feedback at each stage of the research process.

5. Receive a comprehensive research report at the end.

## Project Structure

- `app.py`: Main Streamlit application
- `src/`
  - `config.py`: Configuration settings
  - `models.py`: Data models for the application
  - `components.py`: Core components for the research process
  - `graph.py`: LangGraph definition
  - `tools.py`: Research tools for information gathering

## Requirements

- Python 3.9+
- OpenAI API key
- Tavily API key (for web search)
- LangSmith API key (optional, for tracing)

## License

MIT
