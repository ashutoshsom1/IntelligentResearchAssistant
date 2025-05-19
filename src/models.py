"""
Data models for the Intelligent Research Assistant.
"""
from typing import List, Dict, Optional, Any
from typing_extensions import TypedDict
from langchain_core.pydantic_v1 import BaseModel, Field

class Analyst(BaseModel):
    """Model representing a research analyst."""
    name: str = Field(
        description="Name of the analyst."
    )
    affiliation: str = Field(
        description="Primary affiliation of the analyst.",
    )
    role: str = Field(
        description="Role of the analyst in the context of the topic.",
    )
    description: str = Field(
        description="Description of the analyst focus, concerns, and motives.",
    )
    
    @property
    def persona(self) -> str:
        """Return a formatted string representation of the analyst persona."""
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"

class Perspectives(BaseModel):
    """Model representing a collection of analyst perspectives."""
    analysts: List[Analyst] = Field(
        description="Comprehensive list of analysts with their roles and affiliations.",
    )

class Source(BaseModel):
    """Model representing an information source."""
    name: str = Field(
        description="Name of the source."
    )
    description: str = Field(
        description="Description of the source."
    )
    enabled: bool = Field(
        description="Whether the source is enabled.",
        default=True
    )

class ResearchQuestion(BaseModel):
    """Model representing a research question."""
    question: str = Field(
        description="The research question."
    )
    analyst: Analyst = Field(
        description="The analyst asking the question."
    )

class ResearchAnswer(BaseModel):
    """Model representing a research answer."""
    question: str = Field(
        description="The research question."
    )
    answer: str = Field(
        description="The answer to the research question."
    )
    sources: List[str] = Field(
        description="The sources used to answer the question."
    )

class Interview(BaseModel):
    """Model representing an interview between an analyst and an expert."""
    analyst: Analyst = Field(
        description="The analyst conducting the interview."
    )
    questions: List[str] = Field(
        description="The questions asked by the analyst."
    )
    answers: List[str] = Field(
        description="The answers provided by the expert."
    )
    
    @property
    def transcript(self) -> str:
        """Return a formatted transcript of the interview."""
        transcript = f"Interview with {self.analyst.name} ({self.analyst.role})\n\n"
        for i in range(len(self.questions)):
            transcript += f"Q: {self.questions[i]}\n"
            if i < len(self.answers):
                transcript += f"A: {self.answers[i]}\n\n"
        return transcript

# class Report(BaseModel):
#     """Model representing a research report."""
#     title: str = Field(
#         description="The title of the report."
#     )
#     summary: str = Field(
#         description="Executive summary of the report."
#     )
#     sections: List[Dict[str, str]] = Field(
#         description="Sections of the report, with headings and content."
#     )
#     conclusion: str = Field(
#         description="Conclusion of the report."
#     )
#     sources: List[str] = Field(
#         description="Sources used in the report."
#     )

class Report(BaseModel):
    """Model representing a research report."""
    title: str = Field(
        description="The title of the report."
    )
    summary: str = Field(
        description="Executive summary of the report."
    )
    sections: Optional[List[Dict[str, str]]] = Field(
        description="Sections of the report, with headings and content. Each item is a dictionary with one key-value pair where the key is the section heading and the value is the section content."
    )
    conclusion: str = Field(
        description="Conclusion of the report."
    )
    sources: List[str] = Field(
        description="Sources used in the report."
    )
# State TypedDicts for graph nodes
class GenerateAnalystsState(TypedDict):
    """State for the generate analysts node."""
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: Optional[str]  # Human feedback
    analysts: List[Analyst]  # Generated analysts

class PlanResearchState(TypedDict):
    """State for the plan research node."""
    topic: str  # Research topic
    analysts: List[Analyst]  # Analysts
    research_questions: List[ResearchQuestion]  # Research questions

class ConductInterviewsState(TypedDict):
    """State for the conduct interviews node."""
    topic: str  # Research topic
    analysts: List[Analyst]  # Analysts
    research_questions: List[ResearchQuestion]  # Research questions
    interviews: List[Interview]  # Interviews
    sources: List[Source]  # Sources to use

class GenerateReportState(TypedDict):
    """State for the generate report node."""
    topic: str  # Research topic
    analysts: List[Analyst]  # Analysts
    interviews: List[Interview]  # Interviews
    report: Report  # Generated report

class ResearchAssistantState(TypedDict):
    """Overall state for the research assistant."""
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    analysts: List[Analyst]  # Analysts
    research_questions: List[ResearchQuestion]  # Research questions
    interviews: List[Interview]  # Interviews
    sources: List[Source]  # Sources to use
    report: Optional[Report]  # Generated report
    human_feedback: Optional[str]  # Human feedback
    current_step: str  # Current step in the process
