from enum import Enum


class PromptName(str, Enum):
    VISION = "vision_prompt.md"
    KNOWLEDGE = "knowledge_prompt.md"
    ANALYST = "analyst_prompt.md"
    CRITIC = "critic_prompt.md"
    VERIFIER = "verifier_prompt.md"
    STYLE = "style_prompt.md"
    CONTEXT = "context_prompt.md"