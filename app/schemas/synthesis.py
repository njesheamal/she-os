from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class DecisionDraft(BaseModel):
    """Transient draft that is never persisted."""

    decision_summary: str = Field(
        min_length=1,
        examples=["Proceed with a pilot purchase only after supplier validation."],
    )
    reasoning: str = Field(
        min_length=1,
        examples=[
            "The existing observations show a reliable supplier base, moderate cost risk, and a clear upside from a controlled pilot."
        ],
    )
    confidence: Literal["low", "medium", "high"] = Field(
        examples=["medium"],
    )
    source_observation_ids: list[UUID] = Field(
        examples=[["123e4567-e89b-12d3-a456-426614174000"]],
    )


class SynthesisResponse(BaseModel):
    """Draft synthesis returned to a human reviewer."""

    initiative_id: UUID = Field(
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    observation_count: int = Field(
        ge=0,
        examples=[2],
    )
    draft: DecisionDraft = Field(
        examples=[{
            "decision_summary": "Proceed with a limited pilot.",
            "reasoning": "The observations support a phased approach with manageable trade-offs.",
            "confidence": "medium",
            "source_observation_ids": ["123e4567-e89b-12d3-a456-426614174000"],
        }],
    )
