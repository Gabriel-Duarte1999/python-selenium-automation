import pytest
from portal_automation.utils.config import Config

def test_config_target_url_exists():
    assert hasattr(Config, "TARGET_URL")
    assert isinstance(Config.TARGET_URL, str)

def test_config_email_exists():
    assert hasattr(Config, "EMAIL")
    assert isinstance(Config.EMAIL, str)

def test_config_password_exists():
    assert hasattr(Config, "PASSWORD")
    assert isinstance(Config.PASSWORD, str)
