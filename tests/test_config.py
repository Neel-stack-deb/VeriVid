from app.core.ai_settings import ai_settings
from app.core.config import settings


def test_application_settings_load_without_credentials():
  assert settings.app_name == "VeriVid"
  assert settings.fireworks.base_url == ""
  assert settings.amd.api_key == ""


def test_ai_settings_optional_credentials():
  assert ai_settings.base_url == ""
  assert ai_settings.api_key == ""
  assert "debate" in ai_settings.models


def test_main_app_imports_without_credentials():
  from main import app

  assert app.title == "VeriVid"