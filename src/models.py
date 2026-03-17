"""
Pydantic models for structured, type-safe responses
from the F1 Regulations Assistant.
"""

from pydantic import BaseModel, Field


class RegulationReference(BaseModel):
    """A specific clause or article from the regularions."""

    article: str = Field(description="Article or clause number, e.g, '3.2.1'")
    title: str = Field(description="Title or short description of the article")
    excerpt: str = Field(description="Relevant excerpt from the regulation text")


class RegulationAnswer(BaseModel):
    """Structured answer to a question about the F1 Technical Regulations."""

    answer: str = Field(
        description="Clear and direct answer to the user's question",
    )
    references: list[RegulationReference] = Field(
        description="List of regulation articles that support this answer",
        min_length=1,
    )
    confidence: float = Field(
        description="Confidence level in the answer, from 0.0 to 1.0",
        ge=0.0,
        le=1.0,
    )
    disclaimer: str | None = Field(
        description=(
            "Optional disclaimer if the question is ambiguos, "
            "outside the regulations scope, or requires official interpretation"
        )
    )
