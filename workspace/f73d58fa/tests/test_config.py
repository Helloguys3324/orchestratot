import os
import pytest
from dotenv import load_dotenv

def test_token_exists():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    assert token is not None and token != "ваш_токен_здесь", "Токен не найден или не изменен в .env"