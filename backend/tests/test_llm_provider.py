import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from backend.llm.provider import call_live_api, call_llm

@pytest.mark.asyncio
async def test_call_live_api_success():
    api_key = "test_key"
    model = "gemini-3-flash-live"
    messages = [{"role": "system", "content": "You are helpful"}, {"role": "user", "content": "Hello"}]

    mock_client = MagicMock()
    mock_session = AsyncMock()
    mock_client.aio.live.connect.return_value.__aenter__.return_value = mock_session

    mock_response = MagicMock()
    mock_part = MagicMock()
    mock_part.text = "Hi there"
    mock_model_turn = MagicMock()
    mock_model_turn.parts = [mock_part]
    mock_response.server_content.model_turn = mock_model_turn
    mock_response.server_content.turn_complete = True

    async def mock_receive():
        yield mock_response

    mock_session.receive = mock_receive

    with patch("google.genai.Client", return_value=mock_client):
        result = await call_live_api(api_key, model, messages)
        assert result == "Hi there"

@pytest.mark.asyncio
async def test_call_live_api_exception():
    api_key = "test_key"
    model = "gemini-3-flash-live"
    messages = [{"role": "user", "content": "Hello"}]

    mock_client = MagicMock()
    mock_client.aio.live.connect.side_effect = Exception("Test Error")

    with patch("google.genai.Client", return_value=mock_client):
        result = await call_live_api(api_key, model, messages)
        assert "Live API error" in result
        assert "Test Error" in result

@pytest.mark.asyncio
async def test_call_llm_live_api():
    api_key = "test_key"
    base_url = "test_url"
    model = "gemini-3-flash-live"
    messages = [{"role": "user", "content": "Hello"}]

    mock_model_info = {"live_api": True}

    with patch("backend.llm.provider.get_model_info", return_value=mock_model_info, create=True):
        with patch("backend.llm.provider.call_live_api", new_callable=AsyncMock) as mock_call_live_api:
            mock_call_live_api.return_value = "Live response"
            # get_model_info is imported inside call_llm so we patch the module where it's called
            with patch("backend.models.registry.get_model", return_value=mock_model_info):
                result = await call_llm(api_key, base_url, model, messages)
                assert result == "Live response"
                mock_call_live_api.assert_called_once_with(api_key, model, messages, 0.7)

@pytest.mark.asyncio
async def test_call_llm_openai_compatible():
    api_key = "test_key"
    base_url = "test_url"
    model = "gpt-4o"
    messages = [{"role": "user", "content": "Hello"}]

    mock_model_info = {"live_api": False}

    mock_openai_client = MagicMock()
    mock_create = AsyncMock()

    mock_choice = MagicMock()
    mock_choice.message.content = "OpenAI response"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_create.return_value = mock_response
    mock_openai_client.chat.completions.create = mock_create

    with patch("backend.models.registry.get_model", return_value=mock_model_info):
        with patch("openai.AsyncOpenAI", return_value=mock_openai_client):
            result = await call_llm(api_key, base_url, model, messages)
            assert result == "OpenAI response"
            mock_create.assert_called_once_with(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=4096,
            )
