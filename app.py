"""
Streamlit application for the Intelligent Research Assistant.
"""
import streamlit as st
from typing import Dict, List, Any, Optional
import time

from src.config import MAX_ANALYSTS
from src.models import Analyst, ResearchQuestion, Interview, Report, Source
from src.graph import create_research_assistant_graph

# Set page configuration
st.set_page_config(
    page_title="Intelligent Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.graph = create_research_assistant_graph()
    st.session_state.thread_id = None
    st.session_state.current_step = None
    st.session_state.topic = None
    st.session_state.max_analysts = MAX_ANALYSTS
    st.session_state.analysts = []
    st.session_state.research_questions = []
    st.session_state.interviews = []
    st.session_state.report = None
    st.session_state.sources = [
        Source(name="Web Search", description="Search the web for information", enabled=True),
        Source(name="Wikipedia", description="Search Wikipedia for information", enabled=True)
    ]
    st.session_state.initialized = True

# Helper functions
def start_research():
    """Start the research process."""
    # Reset session state
    st.session_state.analysts = []
    st.session_state.research_questions = []
    st.session_state.interviews = []
    st.session_state.report = None
    
    # Create a new thread
    thread = {"configurable": {"thread_id": str(time.time())}}
    st.session_state.thread_id = thread
    
    # Start the graph
    initial_state = {
        "topic": st.session_state.topic,
        "max_analysts": st.session_state.max_analysts,
        "analysts": [],
        "research_questions": [],
        "interviews": [],
        "sources": st.session_state.sources,
        "report": None,
        "human_feedback": None,
        "current_step": "create_analysts"
    }
    
    # Run the graph until the first interruption
    for event in st.session_state.graph.stream(initial_state, thread, stream_mode="values"):
        # Update session state with event values
        for key, value in event.items():
            if key == "analysts":
                st.session_state.analysts = value
            elif key == "research_questions":
                st.session_state.research_questions = value
            elif key == "interviews":
                st.session_state.interviews = value
            elif key == "report":
                st.session_state.report = value
    
    # Get the current state
    state = st.session_state.graph.get_state(thread)
    st.session_state.current_step = state.next[0] if state.next else None

def continue_research(feedback=None):
    """Continue the research process with optional feedback."""
    if not st.session_state.thread_id:
        st.error("No active research session. Please start a new research.")
        return
    
    # Update state with feedback if provided
    if feedback:
        st.session_state.graph.update_state(
            st.session_state.thread_id,
            {"human_feedback": feedback},
            as_node=st.session_state.current_step
        )
    else:
        st.session_state.graph.update_state(
            st.session_state.thread_id,
            {"human_feedback": None},
            as_node=st.session_state.current_step
        )
    
    # Continue the graph execution
    for event in st.session_state.graph.stream(None, st.session_state.thread_id, stream_mode="values"):
        # Update session state with event values
        for key, value in event.items():
            if key == "analysts":
                st.session_state.analysts = value
            elif key == "research_questions":
                st.session_state.research_questions = value
            elif key == "interviews":
                st.session_state.interviews = value
            elif key == "report":
                st.session_state.report = value
    
    # Get the current state
    state = st.session_state.graph.get_state(st.session_state.thread_id)
    st.session_state.current_step = state.next[0] if state.next else None

# Main application UI
st.title("🔍 Intelligent Research Assistant")
st.markdown("""
This application helps you conduct in-depth research on any topic using AI analysts.
Each analyst brings a unique perspective to your research topic, asking targeted questions
and synthesizing information from various sources.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Research Configuration")
    
    # Topic input
    topic = st.text_input("Research Topic", value=st.session_state.topic or "")
    if topic != st.session_state.topic:
        st.session_state.topic = topic
    
    # Number of analysts
    max_analysts = st.slider("Number of Analysts", min_value=1, max_value=5, value=st.session_state.max_analysts)
    if max_analysts != st.session_state.max_analysts:
        st.session_state.max_analysts = max_analysts
    
    # Sources configuration
    st.subheader("Information Sources")
    for i, source in enumerate(st.session_state.sources):
        source.enabled = st.checkbox(f"{source.name}", value=source.enabled, help=source.description)
    
    # Start button
    if st.button("Start Research", disabled=not topic):
        with st.spinner("Starting research process..."):
            start_research()

# Main content area
if st.session_state.current_step == "review_analysts":
    st.header("Review Analysts")
    st.markdown("The following analysts have been generated based on your research topic. You can provide feedback to refine them.")
    
    # Display analysts
    for i, analyst in enumerate(st.session_state.analysts):
        with st.expander(f"{analyst.name} - {analyst.role}", expanded=True):
            st.markdown(f"**Affiliation:** {analyst.affiliation}")
            st.markdown(f"**Description:** {analyst.description}")
    
    # Feedback input
    feedback = st.text_area("Feedback (optional)", placeholder="Provide feedback to refine the analysts...")
    
    # Continue buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue with these analysts"):
            with st.spinner("Planning research..."):
                continue_research()
    with col2:
        if st.button("Regenerate analysts", disabled=not feedback):
            with st.spinner("Regenerating analysts..."):
                continue_research(feedback)

elif st.session_state.current_step == "review_plan":
    st.header("Review Research Plan")
    st.markdown("The following research questions have been generated for each analyst. You can provide feedback to refine them.")
    
    # Group questions by analyst
    questions_by_analyst = {}
    for question in st.session_state.research_questions:
        analyst_name = question.analyst.name
        if analyst_name not in questions_by_analyst:
            questions_by_analyst[analyst_name] = []
        questions_by_analyst[analyst_name].append(question.question)
    
    # Display questions by analyst
    for analyst in st.session_state.analysts:
        if analyst.name in questions_by_analyst:
            with st.expander(f"{analyst.name} - {analyst.role}", expanded=True):
                for i, question in enumerate(questions_by_analyst[analyst.name]):
                    st.markdown(f"{i+1}. {question}")
    
    # Feedback input
    feedback = st.text_area("Feedback (optional)", placeholder="Provide feedback to refine the research questions...")
    
    # Continue buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue with these questions"):
            with st.spinner("Conducting interviews..."):
                continue_research()
    with col2:
        if st.button("Regenerate questions", disabled=not feedback):
            with st.spinner("Regenerating questions..."):
                continue_research(feedback)

elif st.session_state.current_step == "review_interviews":
    st.header("Review Interviews")
    st.markdown("The following interviews have been conducted with experts. You can provide feedback to refine them.")
    
    # Display interviews
    for interview in st.session_state.interviews:
        with st.expander(f"Interview with {interview.analyst.name}", expanded=True):
            for i in range(len(interview.questions)):
                st.markdown(f"**Q: {interview.questions[i]}**")
                if i < len(interview.answers):
                    st.markdown(f"A: {interview.answers[i]}")
    
    # Feedback input
    feedback = st.text_area("Feedback (optional)", placeholder="Provide feedback to refine the interviews...")
    
    # Continue buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Continue with these interviews"):
            with st.spinner("Generating report..."):
                continue_research()
    with col2:
        if st.button("Regenerate interviews", disabled=not feedback):
            with st.spinner("Regenerating interviews..."):
                continue_research(feedback)

elif st.session_state.current_step == "review_report":
    st.header("Research Report")
    
    if st.session_state.report:
        report = st.session_state.report
        
        # Display report
        st.markdown(f"# {report.title}")
        st.markdown("## Executive Summary")
        st.markdown(report.summary)
        
        # Display sections
        if report.sections:
            for section in report.sections:
                for heading, content in section.items():
                    st.markdown(f"## {heading}")
                    st.markdown(content)
        else:
            st.markdown("## No Sections Available")
            st.markdown("The report does not contain any sections.")
        
        # Display conclusion
        st.markdown("## Conclusion")
        st.markdown(report.conclusion)
        
        # Display sources
        st.markdown("## Sources")
        for source in report.sources:
            st.markdown(f"- {source}")
    
    # Feedback input
    feedback = st.text_area("Feedback (optional)", placeholder="Provide feedback to refine the report...")
    
    # Continue buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Finalize Report"):
            st.success("Research completed successfully!")
            continue_research()
    with col2:
        if st.button("Regenerate Report", disabled=not feedback):
            with st.spinner("Regenerating report..."):
                continue_research(feedback)

elif not st.session_state.current_step:
    # Initial state or completed state
    if st.session_state.report:
        st.header("Research Completed")
        st.success("Your research has been completed successfully!")
        
        # Display final report
        report = st.session_state.report
        st.markdown(f"# {report.title}")
        st.markdown("## Executive Summary")
        st.markdown(report.summary)
        
        # Display sections
        for section in report.sections:
            for heading, content in section.items():
                st.markdown(f"## {heading}")
                st.markdown(content)
        
        # Display conclusion
        st.markdown("## Conclusion")
        st.markdown(report.conclusion)
        
        # Display sources
        st.markdown("## Sources")
        for source in report.sources:
            st.markdown(f"- {source}")
        
        # New research button
        if st.button("Start New Research"):
            st.session_state.topic = None
            st.session_state.analysts = []
            st.session_state.research_questions = []
            st.session_state.interviews = []
            st.session_state.report = None
            st.session_state.thread_id = None
            st.session_state.current_step = None
            st.experimental_rerun()
    else:
        # Initial state
        st.info("Enter a research topic in the sidebar and click 'Start Research' to begin.")

