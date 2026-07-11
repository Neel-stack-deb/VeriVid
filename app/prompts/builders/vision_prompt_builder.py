from pathlib import Path


class VisionPromptBuilder:

    _PROMPT_PATH = (
        Path(__file__).parent.parent
        / "templates"
        / "vision_prompt.txt"
    )

    @classmethod
    def build(cls) -> str:
        return cls._PROMPT_PATH.read_text(
            encoding="utf-8"
        )