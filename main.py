import streamlit as st
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
provider = st.selectbox(
    "Choose LLM Provider",
    ["OpenAI", "Mistral", "Claude", "Gemini", "Hugging Face", "Ollama"],
    index=0,
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

if "summary" not in st.session_state:
    st.session_state.summary = None

if st.button("Generate Summary"):
    if not api_key and provider != "Ollama":
        st.error(f"Please enter your {api_key_label[provider]}")
    elif text:
        with st.spinner("Generating summary..."):
            summary = summarize_text(text, api_key, st, provider)
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
