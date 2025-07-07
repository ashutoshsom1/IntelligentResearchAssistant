"""
Core components for the Intelligent Research Assistant.
"""
from typing import List, Dict, Any, Optional

from langchain_openai import AzureChatOpenAI

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from src.config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, ENDPOINT, API_VERSION, LLM_MODEL_NAME, OPENAI_API_KEY
from src.models import (
    Analyst, Perspectives, ResearchQuestion, Interview, Report,
    GenerateAnalystsState, PlanResearchState, ConductInterviewsState, GenerateReportState
)
from src.tools import ResearchTools

# OPENAI_API_KEY = "dfc1185767ac474c9be05d2ac537f410"
# ENDPOINT = "https://openaitest-005.openai.azure.com/"
# API_VERSION = "2024-10-21"
# LLM_MODEL_NAME="gpt-35-turbo-16k"

def get_llm(azure_deployment: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, endpoint: str = ENDPOINT, api_key: str = OPENAI_API_KEY) -> AzureChatOpenAI:
    """Get a Azure open ai language model instance."""
    return AzureChatOpenAI(
        azure_deployment=azure_deployment,  # Replace with your deployment name
        temperature=temperature,
        azure_endpoint=endpoint,
        api_version=API_VERSION,
        api_key=api_key
    )

#prompt Guiding Component

# Analyst Generation Component
def create_analysts(state: GenerateAnalystsState) -> Dict[str, List[Analyst]]:
    """Create analyst personas based on the research topic."""
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    # Get LLM with structured output
    llm = get_llm()
    print (f"LLM Model: {llm}")
    
    # Use response_format with json_object instead of json_schema
    # structured_llm = llm.with_structured_output(Perspectives,)
    structured_llm = llm.with_structured_output(Perspectives)


    # System message
    system_message = f"""You are tasked with creating a set of AI analyst personas. Follow these instructions carefully:

1. First, review the research topic:
{topic}

2. Examine any editorial feedback that has been optionally provided to guide creation of the analysts:

{human_analyst_feedback}

3. Determine the most interesting themes based upon the topic and feedback above.

4. Pick the top {max_analysts} themes.

5. Assign one analyst to each theme.

Each analyst should have a unique perspective and expertise relevant to the research topic."""

    # Generate analysts
    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the set of analysts.")
    ])

    # Return the list of analysts
    return {"analysts": analysts.analysts}

# Research Planning Component
def plan_research(state: PlanResearchState) -> Dict[str, List[ResearchQuestion]]:
    """Plan research questions for each analyst."""
    topic = state['topic']
    analysts = state['analysts']

    # Get LLM
    llm = get_llm()

    research_questions = []

    for analyst in analysts:
        # Create prompt for generating research questions
        prompt = f"""You are helping to generate research questions for an analyst with the following profile:

{analyst.persona}

The research topic is: {topic}

Based on this analyst's perspective and expertise, generate 3 specific, focused research questions that this analyst would want to investigate.
Each question should be directly relevant to the analyst's role and interests.
"""

        # Generate questions
        response = llm.invoke([HumanMessage(content=prompt)])

        # Parse questions from response
        question_lines = [line.strip() for line in response.content.split('\n') if line.strip() and ('?' in line)]

        # Create research question objects
        for question in question_lines[:3]:  # Limit to 3 questions per analyst
            research_questions.append(ResearchQuestion(
                question=question,
                analyst=analyst
            ))

    return {"research_questions": research_questions}

# Interview Conducting Component
def conduct_interviews(state: ConductInterviewsState) -> Dict[str, List[Interview]]:
    """Conduct interviews between analysts and experts."""
    topic = state['topic']
    analysts = state['analysts']
    research_questions = state['research_questions']
    sources = state.get('sources', [])

    # Get LLM
    llm = get_llm()

    # Get research tools
    tools = ResearchTools.get_all_tools()

    interviews = []

    # Group questions by analyst
    questions_by_analyst = {}
    for question in research_questions:
        analyst_name = question.analyst.name
        if analyst_name not in questions_by_analyst:
            questions_by_analyst[analyst_name] = []
        questions_by_analyst[analyst_name].append(question.question)

    # Conduct interviews for each analyst
    for analyst in analysts:
        if analyst.name not in questions_by_analyst:
            continue

        questions = questions_by_analyst[analyst.name]
        answers = []

        for question in questions:
            # Create expert prompt
            expert_prompt = f"""You are an expert being interviewed by {analyst.name}, a {analyst.role} from {analyst.affiliation}.

The interview is about: {topic}

The question you need to answer is: {question}

Use the available research tools to gather information and provide a comprehensive, well-informed answer.
Your answer should be detailed, factual, and directly address the question from the perspective of an expert in this field.
"""

            # Use tools to research and answer the question
            tool_response = ""
            for tool in tools:
                try:
                    tool_result = tool.invoke({"query": f"{topic} {question}"})
                    tool_response += f"\n\nResults from {tool.name}:\n{tool_result}\n"
                except Exception as e:
                    tool_response += f"\n\nError using {tool.name}: {str(e)}\n"

            # Generate answer using research results
            answer_prompt = f"""Based on the following research results, provide a comprehensive answer to the question: {question}

Research results:
{tool_response}

Your answer should be detailed, factual, and directly address the question from the perspective of an expert in this field.
"""

            answer_response = llm.invoke([HumanMessage(content=answer_prompt)])
            answers.append(answer_response.content)

        # Create interview object
        interviews.append(Interview(
            analyst=analyst,
            questions=questions,
            answers=answers
        ))

    return {"interviews": interviews}

# Report Generation Component
def generate_report(state: GenerateReportState) -> Dict[str, Report]:
    """Generate a comprehensive research report."""
    topic = state['topic']
    analysts = state['analysts']
    interviews = state['interviews']

    # Get LLM with structured output
    llm = get_llm()
    structured_llm = llm.with_structured_output(Report)

    # Compile interview transcripts
    transcripts = "\n\n".join([interview.transcript for interview in interviews])

    # System message for report generation
    system_message = f"""You are tasked with creating a comprehensive research report on the following topic:

{topic}

The report should be based on the following interview transcripts with various analysts:

{transcripts}

Create a well-structured report that synthesizes the insights from all interviews.
The report should include:
1. An executive summary
2. Sections covering the main themes and findings (at least 3-5 sections)
3. A conclusion with recommendations
4. Citations of sources mentioned in the interviews

Format the report professionally and ensure it provides valuable insights for decision-makers.

IMPORTANT: Make sure to include sections in your report with headings and content."""
    # Generate report
    report = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the research report with all required fields including sections.")
    ])
    #make it highlighted
    print ("\n\nReport:", report)

    return {"report": report}
