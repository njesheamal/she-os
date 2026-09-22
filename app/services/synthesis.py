from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories import observation as observation_repo
from app.schemas.synthesis import DecisionDraft, SynthesisResponse


class SynthesisError(Exception):
    """Base error for AI synthesis failures."""


class NoObservationsError(SynthesisError):
    """The initiative has no observations to synthesize from."""


class MalformedDraftError(SynthesisError):
    """The model response was missing or had an invalid tool-use payload."""


DECISION_TOOL = {
    "name": "draft_decision",
    "description": "Draft one decision grounded only in the given observations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "decision_summary": {"type": "string"},
            "reasoning": {"type": "string"},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["decision_summary", "reasoning", "confidence"],
    },
}

SYSTEM_PROMPT = (
    "You are drafting a decision for a human reviewer. Ground every recommendation and rationale only in the observations provided. "
    "Do not speculate beyond the evidence. Be explicit about uncertainty and set confidence based on how strongly the observations support the recommendation."
)


def synthesize_decision(
    db: Session,
    initiative_id: UUID,
    client,
    *,
    model: str,
    max_tokens: int = 1024,
) -> SynthesisResponse:
    observations = observation_repo.list_by_initiative(db, initiative_id)
    if not observations:
        raise NoObservationsError(
            f"No observations found for initiative {initiative_id}"
        )

    prompt_lines = ["Here are the initiative observations:"]
    for observation in observations:
        prompt_lines.append(f"[{observation.id}] {observation.details}")
    prompt = "\n\n".join(prompt_lines)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        tools=[DECISION_TOOL],
        tool_choice={"type": "tool", "name": "draft_decision"},
        messages=[{"role": "user", "content": prompt}],
    )

    tool_use = next(
        (block for block in getattr(message, "content", []) if getattr(block, "type", None) == "tool_use"),
        None,
    )
    if tool_use is None:
        raise MalformedDraftError("Model returned no tool_use block.")

    data = getattr(tool_use, "input", None)
    if not isinstance(data, dict):
        raise MalformedDraftError("Model returned malformed draft content.")

    decision_summary = data.get("decision_summary")
    reasoning = data.get("reasoning")
    raw_confidence = data.get("confidence")
    confidence = (
        raw_confidence.strip().lower() if isinstance(raw_confidence, str) else ""
    )
    if not isinstance(decision_summary, str) or not decision_summary.strip():
        raise MalformedDraftError("Decision summary is missing or empty.")
    if not isinstance(reasoning, str) or not reasoning.strip():
        raise MalformedDraftError("Reasoning is missing or empty.")
    if confidence not in {"low", "medium", "high"}:
        raise MalformedDraftError(
            f"Confidence must be low, medium, or high; model returned {raw_confidence!r}."
        )

    draft = DecisionDraft(
        decision_summary=decision_summary,
        reasoning=reasoning,
        confidence=confidence,
        source_observation_ids=[observation.id for observation in observations],
    )

    return SynthesisResponse(
        initiative_id=initiative_id,
        observation_count=len(observations),
        draft=draft,
    )
