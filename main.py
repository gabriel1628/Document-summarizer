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
from modules.provider_config import (
    provider_models,
    api_key_label,
    api_key_help,
    provider_env_vars,
)

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
    # If API key not provided, try to fetch from .env
    if not api_key:
        st.warning(f"API key not provided. Attempting to fetch from the `.env` file.")
        env_var = provider_env_vars.get(provider)
        api_key = env_variables.get(env_var, "")
    if text:
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
