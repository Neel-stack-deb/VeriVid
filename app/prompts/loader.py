from pathlib import Path


class PromptLoader:
    _PROMPT_DIR = Path(__file__).parent.__truediv__("templates")

    @classmethod
    def load(cls, filename: str) -> str:
        path = cls._PROMPT_DIR / filename
        return path.read_text(encoding="utf-8")