from pydantic import BaseModel


class InferenceResponse(BaseModel):
    model: str

    content: str