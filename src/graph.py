"""
Graph definition for the Intelligent Research Assistant.
"""
from typing import Dict, List, Any, Literal, Optional, Union
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from src.models import (
    Analyst, ResearchQuestion, Interview, Report, Source,
    ResearchAssistantState
)
from src.components import (
    create_analysts, plan_research, conduct_interviews, generate_report
)

def human_feedback(state: ResearchAssistantState) -> Dict:
    """No-op node that should be interrupted for human feedback."""
    # This function doesn't modify state, it's a placeholder for human interruption
    return {}

def should_continue_analysts(state: ResearchAssistantState) -> Literal["plan_research", "create_analysts"]:
    """Determine whether to continue to planning or regenerate analysts."""
    # Check if human feedback exists
    human_feedback = state.get('human_feedback')
    if human_feedback:
        # Reset human feedback and regenerate analysts
        return "create_analysts"
    
    # Continue to planning
    return "plan_research"

def should_continue_planning(state: ResearchAssistantState) -> Literal["conduct_interviews", "plan_research"]:
    """Determine whether to continue to interviews or replan research."""
    # Check if human feedback exists
    human_feedback = state.get('human_feedback')
    if human_feedback:
        # Reset human feedback and replan research
        return "plan_research"
    
    # Continue to interviews
    return "conduct_interviews"

def should_continue_interviews(state: ResearchAssistantState) -> Literal["generate_report", "conduct_interviews"]:
    """Determine whether to continue to report generation or redo interviews."""
    # Check if human feedback exists
    human_feedback = state.get('human_feedback')
    if human_feedback:
        # Reset human feedback and redo interviews
        return "conduct_interviews"
    
    # Continue to report generation
    return "generate_report"

def should_continue_report(state: ResearchAssistantState) -> Literal[END, "generate_report"]:
    """Determine whether to end or regenerate the report."""
    # Check if human feedback exists
    human_feedback = state.get('human_feedback')
    if human_feedback:
        # Reset human feedback and regenerate report
        return "generate_report"
    
    # End the process
    return END

def create_research_assistant_graph() -> StateGraph:
    """Create the research assistant graph."""
    # Create the graph
    builder = StateGraph(ResearchAssistantState)
    
    # Add nodes
    builder.add_node("create_analysts", create_analysts)
    builder.add_node("review_analysts", human_feedback)
    builder.add_node("plan_research", plan_research)
    builder.add_node("review_plan", human_feedback)
    builder.add_node("conduct_interviews", conduct_interviews)
    builder.add_node("review_interviews", human_feedback)
    builder.add_node("generate_report", generate_report)
    builder.add_node("review_report", human_feedback)
    
    # Add edges
    builder.add_edge(START, "create_analysts")
    builder.add_edge("create_analysts", "review_analysts")
    builder.add_conditional_edges(
        "review_analysts",
        should_continue_analysts,
        {
            "create_analysts": "create_analysts",
            "plan_research": "plan_research"
        }
    )
    
    builder.add_edge("plan_research", "review_plan")
    builder.add_conditional_edges(
        "review_plan",
        should_continue_planning,
        {
            "plan_research": "plan_research",
            "conduct_interviews": "conduct_interviews"
        }
    )
    
    builder.add_edge("conduct_interviews", "review_interviews")
    builder.add_conditional_edges(
        "review_interviews",
        should_continue_interviews,
        {
            "conduct_interviews": "conduct_interviews",
            "generate_report": "generate_report"
        }
    )
    
    builder.add_edge("generate_report", "review_report")
    builder.add_conditional_edges(
        "review_report",
        should_continue_report,
        {
            "generate_report": "generate_report",
            END: END
        }
    )
    
    # Compile the graph with interruptions at review nodes
    memory = MemorySaver()
    graph = builder.compile(
        interrupt_before=[
            "review_analysts",
            "review_plan",
            "review_interviews",
            "review_report"
        ],
        checkpointer=memory
    )
    
    return graph
