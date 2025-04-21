provider_models = {
    "OpenAI": ["gpt-4o-mini", "gpt-4o", "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"],
    "Mistral": [
        "mistral-small-latest",
        "mistral-large-latest",
        "ministral-8b-latest",
        "ministral-3b-latest",
    ],
    "Claude": [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ],
    "Gemini": ["gemini-1.5-pro-latest", "gemini-1.0-pro-latest"],
    "Hugging Face": [
        "google/flan-t5-xxl",
        "facebook/bart-large-cnn",
        "bigscience/mt0-large",
    ],
    # "Ollama": ["llama2", "mistral", "phi3", "codellama"],
}

api_key_label = {
    "OpenAI": "OpenAI API Key",
    "Mistral": "Mistral API Key",
    "Claude": "Claude API Key",
    "Gemini": "Gemini API Key",
    "Hugging Face": "Hugging Face API Key",
    # "Ollama": "Ollama Endpoint (optional)",
}

api_key_help = {
    "OpenAI": "Your OpenAI API key is required.",
    "Mistral": "Your Mistral API key is required.",
    "Claude": "Your Claude API key is required.",
    "Gemini": "Your Gemini API key is required.",
    "Hugging Face": "Your Hugging Face API key is required.",
    # "Ollama": "Ollama usually runs locally. Enter endpoint if not default.",
}

provider_env_vars = {
    "OpenAI": "OPENAI_API_KEY",
    "Mistral": "MISTRAL_API_KEY",
    "Claude": "CLAUDE_API_KEY",
    "Gemini": "GEMINI_API_KEY",
    "Hugging Face": "HF_TOKEN",
    # "Ollama": "OLLAMA_ENDPOINT",
}
