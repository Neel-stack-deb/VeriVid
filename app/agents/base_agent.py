from app.ai.clients.base.inference_client import InferenceClient


class BaseAgent:

    def __init__(
        self,
        reasoning_client: InferenceClient,
    ):
        self._reasoning_client = reasoning_client