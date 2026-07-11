from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    whisper_model: str = "openai/whisper-base"
    app_name: str = "VeriVid"
    
settings = Settings()