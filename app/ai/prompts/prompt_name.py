from enum import Enum


class PromptName(str, Enum):
    VISION = "vision_prompt.md"
    KNOWLEDGE = "knowledge_prompt.md"

    CONTEXT = "context_prompt.md"
    VERIFICATION = "verification_prompt.md"
    RISK = "risk_prompt.md"
    CONSENSUS = "consensus_prompt.md"

    STYLE = "style_prompt.md"