from app.prompts.loader import PromptLoader
from app.prompts.prompt_name import PromptName

class VisionPromptBuilder:

    _PROMPT_PATH = PromptLoader.load(PromptName.VISION)

    @classmethod
    def build(cls) -> str:
        return cls._PROMPT_PATH.read_text(
            encoding="utf-8"
        )