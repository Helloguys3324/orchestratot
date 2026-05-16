"""
Model Registry — all available Google AI Studio models with real rate limits.
Categories: Text, Multimodal Generative, Embedding, Open Models.
"""

AVAILABLE_MODELS = {
    # ─── Gemini 3.x — Flagship (Text-out) ────────────────
    "gemini-3.1-pro": {
        "id": "gemini-3.1-pro",
        "name": "Gemini 3.1 Pro",
        "description": "Most advanced reasoning model. Complex agentic workflows & coding.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "premium",
        "icon": "👑",
        "rate_limits": {"rpm": 0, "tpm": 0, "rpd": 0},
        "notes": "Preview — limits may be 0 until GA",
    },
    "gemini-3-flash": {
        "id": "gemini-3-flash",
        "name": "Gemini 3 Flash",
        "description": "Complex multimodal understanding & agentic tasks. High performance.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "advanced",
        "icon": "🔥",
        "rate_limits": {"rpm": 5, "tpm": 250000, "rpd": 20},
    },
    "gemini-3.1-flash-lite": {
        "id": "gemini-3.1-flash-lite",
        "name": "Gemini 3.1 Flash Lite",
        "description": "Most cost-efficient & fastest. Low-latency, high-volume production.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "fast",
        "icon": "⚡",
        "rate_limits": {"rpm": 15, "tpm": 250000, "rpd": 500},
    },
    "gemini-3-flash-live": {
        "id": "gemini-3-flash-live",
        "name": "Gemini 3 Flash Live",
        "description": "UNLIMITED RPM/RPD! Real-time Live API. Best for multi-agent orchestration.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": False,
        "tier": "advanced",
        "icon": "\U0001f680",
        "rate_limits": {"rpm": "Unlimited", "tpm": 65000, "rpd": "Unlimited"},
        "live_api": True,
        "notes": "Uses Live API (WebSocket) — no rate limits!",
    },

    # ─── Gemini 2.5 — Stable ─────────────────────────────
    "gemini-2.5-pro": {
        "id": "gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "description": "Powerful thinking model. Excellent for complex coding & analysis.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "premium",
        "icon": "💎",
        "rate_limits": {"rpm": 10, "tpm": 250000, "rpd": 50},
    },
    "gemini-2.5-flash": {
        "id": "gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "description": "Fast thinking model with great reasoning. Best value.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "advanced",
        "icon": "🧠",
        "rate_limits": {"rpm": 15, "tpm": 250000, "rpd": 500},
    },
    "gemini-2.5-flash-lite": {
        "id": "gemini-2.5-flash-lite",
        "name": "Gemini 2.5 Flash Lite",
        "description": "Lightweight 2.5 model. Fast & cheap for simple tasks.",
        "category": "text",
        "max_output_tokens": 65536,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": False,
        "tier": "fast",
        "icon": "💨",
        "rate_limits": {"rpm": 10, "tpm": 250000, "rpd": 20},
    },

    # ─── Gemini 2.0 — Legacy Stable ─────────────────────
    "gemini-2.0-flash": {
        "id": "gemini-2.0-flash",
        "name": "Gemini 2.0 Flash",
        "description": "Reliable workhorse. Great speed/quality balance.",
        "category": "text",
        "max_output_tokens": 8192,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "standard",
        "icon": "✨",
        "rate_limits": {"rpm": 15, "tpm": 1000000, "rpd": 1500},
    },
    "gemini-2.0-flash-lite": {
        "id": "gemini-2.0-flash-lite",
        "name": "Gemini 2.0 Flash Lite",
        "description": "Ultra-fast legacy model. High volume tasks.",
        "category": "text",
        "max_output_tokens": 8192,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": False,
        "tier": "standard",
        "icon": "💫",
        "rate_limits": {"rpm": 30, "tpm": 1000000, "rpd": 1500},
    },

    # ─── Gemini 1.5 — Legacy ─────────────────────────────
    "gemini-1.5-pro": {
        "id": "gemini-1.5-pro",
        "name": "Gemini 1.5 Pro",
        "description": "Stable with up to 2M context window.",
        "category": "text",
        "max_output_tokens": 8192,
        "context_window": "2M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "legacy",
        "icon": "🌟",
        "rate_limits": {"rpm": 2, "tpm": 32000, "rpd": 50},
    },
    "gemini-1.5-flash": {
        "id": "gemini-1.5-flash",
        "name": "Gemini 1.5 Flash",
        "description": "Fast legacy model. Still reliable.",
        "category": "text",
        "max_output_tokens": 8192,
        "context_window": "1M",
        "supports_vision": True,
        "supports_tools": True,
        "tier": "legacy",
        "icon": "⭐",
        "rate_limits": {"rpm": 15, "tpm": 1000000, "rpd": 1500},
    },

    # ─── Multimodal Generative (TTS, Image) ──────────────
    "gemini-2.5-flash-tts": {
        "id": "gemini-2.5-flash-tts",
        "name": "Gemini 2.5 Flash TTS",
        "description": "Text-to-speech with natural voice generation.",
        "category": "multimodal",
        "max_output_tokens": 8192,
        "context_window": "32K",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "specialized",
        "icon": "🔊",
        "rate_limits": {"rpm": 3, "tpm": 10000, "rpd": 10},
    },
    "gemini-2.5-pro-tts": {
        "id": "gemini-2.5-pro-tts",
        "name": "Gemini 2.5 Pro TTS",
        "description": "Premium text-to-speech. Highest quality voices.",
        "category": "multimodal",
        "max_output_tokens": 8192,
        "context_window": "32K",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "premium",
        "icon": "🎙️",
        "rate_limits": {"rpm": 0, "tpm": 0, "rpd": 0},
        "notes": "Preview — limits TBD",
    },
    "imagen-4": {
        "id": "imagen-4",
        "name": "Imagen 4 Generate",
        "description": "High-quality photorealistic image generation.",
        "category": "multimodal",
        "max_output_tokens": 0,
        "context_window": "N/A",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "specialized",
        "icon": "🎨",
        "rate_limits": {"rpm": None, "tpm": None, "rpd": 25},
    },
    "imagen-4-ultra": {
        "id": "imagen-4-ultra",
        "name": "Imagen 4 Ultra Generate",
        "description": "Highest detail & prompt adherence. Up to 2K resolution.",
        "category": "multimodal",
        "max_output_tokens": 0,
        "context_window": "N/A",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "premium",
        "icon": "🖼️",
        "rate_limits": {"rpm": None, "tpm": None, "rpd": 25},
    },
    "imagen-4-fast": {
        "id": "imagen-4-fast",
        "name": "Imagen 4 Fast Generate",
        "description": "Rapid image generation for high-volume tasks.",
        "category": "multimodal",
        "max_output_tokens": 0,
        "context_window": "N/A",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "fast",
        "icon": "🏃",
        "rate_limits": {"rpm": None, "tpm": None, "rpd": 25},
    },

    # ─── Open Models (Gemma) ─────────────────────────────
    "gemma-4-26b": {
        "id": "gemma-4-26b",
        "name": "Gemma 4 26B (MoE)",
        "description": "Open model. 26B Mixture-of-Experts for server-grade reasoning.",
        "category": "open",
        "max_output_tokens": 8192,
        "context_window": "128K",
        "supports_vision": True,
        "supports_tools": False,
        "tier": "open",
        "icon": "💠",
        "rate_limits": {"rpm": 15, "tpm": "Unlimited", "rpd": 1500},
    },
    "gemma-4-31b": {
        "id": "gemma-4-31b",
        "name": "Gemma 4 31B Dense",
        "description": "Open model. 31B dense — frontier-level performance.",
        "category": "open",
        "max_output_tokens": 8192,
        "context_window": "128K",
        "supports_vision": True,
        "supports_tools": False,
        "tier": "open",
        "icon": "🔷",
        "rate_limits": {"rpm": 15, "tpm": "Unlimited", "rpd": 1500},
    },

    # ─── Embedding ───────────────────────────────────────
    "gemini-embedding-001": {
        "id": "gemini-embedding-001",
        "name": "Gemini Embedding 1",
        "description": "Text embedding model for semantic search & RAG.",
        "category": "embedding",
        "max_output_tokens": 0,
        "context_window": "8K",
        "supports_vision": False,
        "supports_tools": False,
        "tier": "utility",
        "icon": "🧲",
        "rate_limits": {"rpm": 100, "tpm": 30000, "rpd": 1000},
    },
}

# Category display order and labels
CATEGORIES = {
    "text": {"label": "Text / Chat Models", "icon": "💬"},
    "multimodal": {"label": "Multimodal Generative", "icon": "🎭"},
    "open": {"label": "Open Models (Gemma)", "icon": "🔓"},
    "embedding": {"label": "Embedding", "icon": "🧲"},
}

# Tier styling
TIER_STYLES = {
    "premium": {"color": "#EC4899", "label": "Premium"},
    "advanced": {"color": "#8B5CF6", "label": "Advanced"},
    "fast": {"color": "#10B981", "label": "Fast"},
    "standard": {"color": "#06B6D4", "label": "Standard"},
    "legacy": {"color": "#64748B", "label": "Legacy"},
    "specialized": {"color": "#F59E0B", "label": "Specialized"},
    "open": {"color": "#6366F1", "label": "Open Source"},
    "utility": {"color": "#94A3B8", "label": "Utility"},
}


def list_models() -> list[dict]:
    return list(AVAILABLE_MODELS.values())


def list_models_by_category() -> dict:
    result = {}
    for cat_id, cat_info in CATEGORIES.items():
        models = [m for m in AVAILABLE_MODELS.values() if m.get("category") == cat_id]
        if models:
            result[cat_id] = {"info": cat_info, "models": models}
    return result


def get_model(model_id: str) -> dict | None:
    return AVAILABLE_MODELS.get(model_id)


def get_chat_models() -> list[dict]:
    """Return only models suitable for agent chat (text category)."""
    return [m for m in AVAILABLE_MODELS.values() if m.get("category") == "text"]


def get_config_list(api_key: str, model_id: str = "gemini-2.5-flash", base_url: str = None) -> list[dict]:
    if base_url is None:
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    return [{
        "model": model_id,
        "api_key": api_key,
        "base_url": base_url,
        "api_type": "openai",
    }]
