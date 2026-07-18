from pydantic import BaseModel


class InferenceRequest(BaseModel):
    model: str

    system_prompt: str

    user_prompt: str

    response_model: type[BaseModel]

    temperature: float = 0.2

    max_tokens: int = 4096