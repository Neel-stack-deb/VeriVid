from enum import Enum


class AIModel(str, Enum):
    VISION = "vision"
    DEBATE = "debate"
    STYLE = "style"
    CHAT = "chat"