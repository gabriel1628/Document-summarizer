import streamlit as st
from dotenv import dotenv_values
from modules.text_extraction import extract_text_from_file
from modules.web_content_loader import extract_text_from_url
from modules.summarizer import summarize_text
from modules.ui_components import (
    set_page_config,
    add_custom_css,
    main_header,
    sidebar_info,
    about_expander,
)
from modules.prompts import single_prompt, map_prompt, combine_prompt

env_variables = dotenv_values(".env")
set_page_config()
add_custom_css()
main_header()
sidebar_info()

tab1, tab2 = st.tabs(["Upload File", "Enter URL"])
text = None

with tab1:
    st.markdown('<p class="sub-header">Upload Document</p>', unsafe_allow_html=True)
    st.write("Supported formats: PDF, DOCX, TXT, CSV, XLSX")
    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx"]
    )
    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            text = extract_text_from_file(uploaded_file, st)
            if text:
                st.success(f"Successfully processed {uploaded_file.name}")
                with st.expander("Text Preview (first 500 characters)"):
                    st.write(text[:500] + ("..." if len(text) > 500 else ""))

with tab2:
    st.markdown('<p class="sub-header">Enter URL</p>', unsafe_allow_html=True)
    url = st.text_input("Web Page URL", placeholder="https://example.com/article")
    if url:
        with st.spinner("Fetching content from URL..."):
            text = extract_text_from_url(url, st)
            if text:
                st.success(f"Successfully fetched content from URL")
                with st.expander("Text Preview (first 500 characters)"):
                    st.write(text[:500] + ("..." if len(text) > 500 else ""))

# Add provider selection
st.markdown('<p class="sub-header">LLM Provider</p>', unsafe_allow_html=True)

# Map provider to available models
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
    "Ollama": ["llama2", "mistral", "phi3", "codellama"],
}

provider = st.selectbox(
    "Choose LLM Provider",
    list(provider_models.keys()),
    index=0,
)

# Model selection based on provider
model = st.selectbox(
    f"Choose model for {provider}",
    provider_models[provider],
    index=0,
    key="model_select",
)

# Show API key input for the selected provider
api_key_label = {
    "OpenAI": "OpenAI API Key",
    "Mistral": "Mistral API Key",
    "Claude": "Claude API Key",
    "Gemini": "Gemini API Key",
    "Hugging Face": "Hugging Face API Key",
    "Ollama": "Ollama Endpoint (optional)",
}
api_key_help = {
    "OpenAI": "Your OpenAI API key is required.",
    "Mistral": "Your Mistral API key is required.",
    "Claude": "Your Claude API key is required.",
    "Gemini": "Your Gemini API key is required.",
    "Hugging Face": "Your Hugging Face API key is required.",
    "Ollama": "Ollama usually runs locally. Enter endpoint if not default.",
}
st.markdown(
    f'<p class="sub-header">{api_key_label[provider]}</p>', unsafe_allow_html=True
)
api_key = st.text_input(
    f"Enter your {api_key_label[provider]}",
    type="password",
    help=api_key_help[provider],
)

# Map provider to environment variable names
provider_env_vars = {
    "OpenAI": "OPENAI_API_KEY",
    "Mistral": "MISTRAL_API_KEY",
    "Claude": "CLAUDE_API_KEY",
    "Gemini": "GEMINI_API_KEY",
    "Hugging Face": "HF_TOKEN",
    "Ollama": "OLLAMA_ENDPOINT",
}

if "summary" not in st.session_state:
    st.session_state.summary = None

if st.button("Generate Summary"):
    # If API key not provided, try to fetch from .env
    if not api_key:
        st.warning(f"API key not provided. Attempting to fetch from the `.env` file.")
        # Check if the environment variable for the selected provider is set
        if provider == "Ollama":
            api_key = env_variables.get("OLLAMA_ENDPOINT", "")
        else:
            # Get the environment variable name for the selected provider
            env_var = provider_env_vars.get(provider)
            api_key = env_variables.get(env_var, "")
    if not api_key and provider != "Ollama":
        st.error(f"Please enter your {api_key_label[provider]}")
    elif text:
        with st.spinner("Generating summary..."):
            summary = summarize_text(
                text,
                api_key,
                st,
                provider,
                map_prompt=map_prompt,
                combine_prompt=combine_prompt,
                model=model,
            )
            if summary:
                st.session_state.summary = summary
    else:
        st.warning("Please upload a file or enter a valid URL first")

if st.session_state.summary:
    st.markdown('<p class="sub-header">Summary</p>', unsafe_allow_html=True)
    st.markdown(st.session_state.summary)
    st.download_button(
        label="Download Summary",
        data=st.session_state.summary,
        file_name="document_summary.txt",
        mime="text/plain",
    )

about_expander()
