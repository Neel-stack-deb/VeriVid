from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderCredentials(BaseModel):
  """OpenAI-compatible endpoint credentials for a single provider."""

  base_url: str = ""
  api_key: str = ""


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  whisper_model: str = "openai/whisper-base"
  app_name: str = "VeriVid"

  fireworks_base_url: str = Field(default="", validation_alias="FIREWORKS_BASE_URL")
  fireworks_api_key: str = Field(default="", validation_alias="FIREWORKS_API_KEY")
  amd_base_url: str = Field(default="", validation_alias="AMD_BASE_URL")
  amd_api_key: str = Field(default="", validation_alias="AMD_API_KEY")

  cors_origins: list[str] = Field(
    default_factory=list,
    validation_alias="CORS_ORIGINS",
  )

  @field_validator("cors_origins", mode="before")
  @classmethod
  def _parse_cors_origins(cls, value: str | list[str] | None) -> list[str]:
    if value is None:
      return []
    if isinstance(value, list):
      return value
    text = value.strip()
    if not text:
      return []
    return [part.strip() for part in text.split(",") if part.strip()]

  @property
  def fireworks(self) -> ProviderCredentials:
    return ProviderCredentials(
      base_url=self.fireworks_base_url,
      api_key=self.fireworks_api_key,
    )

  @property
  def amd(self) -> ProviderCredentials:
    return ProviderCredentials(
      base_url=self.amd_base_url,
      api_key=self.amd_api_key,
    )


settings = Settings()