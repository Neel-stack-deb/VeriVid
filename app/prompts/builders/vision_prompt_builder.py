from app.prompts.loader import PromptLoader

class VisionPromptBuilder:

    _PROMPT_PATH = PromptLoader.load("vision_prompt.txt")

    @classmethod
    def build(cls) -> str:
        return cls._PROMPT_PATH.read_text(
            encoding="utf-8"
        )