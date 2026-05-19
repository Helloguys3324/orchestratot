async def call_live_api(api_key: str, model: str, messages: list[dict], temperature: float = 0.7) -> str:
    """Call Gemini via the Live API (WebSocket) — unlimited RPM/RPD."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Extract system prompt and build conversation text
    system_text = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
    conversation = "\n\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in messages if msg["role"] in ("user", "assistant")
    ) + ("\n\n" if any(msg["role"] in ("user", "assistant") for msg in messages) else "")

    config = types.LiveConnectConfig(
        response_modalities=[types.Modality.TEXT],
        system_instruction=types.Content(
            parts=[types.Part(text=system_text)]
        ) if system_text else None,
        temperature=temperature,
    )

    full_response = ""
    try:
        async with client.aio.live.connect(
            model="gemini-3-flash-live",
            config=config,
        ) as session:
            await session.send(input=conversation.strip(), end_of_turn=True)
            async for response in session.receive():
                if response.server_content:
                    model_turn = response.server_content.model_turn
                    if model_turn:
                        for part in model_turn.parts:
                            if part.text:
                                full_response += part.text
                    # Check if turn is complete
                    if response.server_content.turn_complete:
                        break
    except Exception as e:
        return f"Live API error: {type(e).__name__}: {str(e)}"

    return full_response or "(empty response)"


async def call_llm(api_key: str, base_url: str, model: str, messages: list[dict], temperature: float = 0.7, max_tokens: int = 4096) -> str:
    """Async call to Gemini. Auto-routes to Live API for live models."""
    from backend.models.registry import get_model as get_model_info
    model_info = get_model_info(model)

    # Use Live API for live models (unlimited rate limits!)
    if model_info and model_info.get("live_api"):
        return await call_live_api(api_key, model, messages, temperature)

    # Standard OpenAI-compatible API
    import openai
    client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""
