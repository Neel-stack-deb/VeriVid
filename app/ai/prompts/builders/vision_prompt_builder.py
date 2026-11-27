from app.ai.prompts.loader import PromptLoader
from app.ai.prompts.prompt_name import PromptName

class VisionPromptBuilder:

    @classmethod
    def build(cls) -> str:
        return PromptLoader.load(PromptName.VISION)