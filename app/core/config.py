from pydantic import BaseModel, Field
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