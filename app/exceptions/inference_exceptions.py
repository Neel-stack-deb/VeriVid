class InferenceError(Exception):
    """Base inference exception."""


class AuthenticationError(InferenceError):
    """Authentication with provider failed."""


class ProviderConnectionError(InferenceError):
    """Provider could not be reached."""


class ProviderTimeoutError(InferenceError):
    """Provider timed out."""


class StructuredOutputError(InferenceError):
    """Structured output parsing failed."""