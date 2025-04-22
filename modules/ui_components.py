import streamlit as st
from modules.provider_config import (
    provider_models,
    api_key_label,
    api_key_help,
)


def set_page_config():
    st.set_page_config(page_title="Document Summarizer", layout="wide")


def add_custom_css():
    st.markdown(
        """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #1E88E5;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            color: #0D47A1;
        }
        .info-text {
            font-size: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def main_header():
    st.markdown(
        '<p class="main-header">Document Summarizer</p>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="info-text">Upload a file or enter a URL to get a detailed summary.</p>',
        unsafe_allow_html=True,
    )


def sidebar_title():
    with st.sidebar:
        st.markdown("### Document Summarizer")
        st.markdown("A Streamlit app powered by LangChain")
        st.markdown("---")


def sidebar_info():
    with st.sidebar:
        with st.expander("How to use"):
            # st.markdown("### How to use:")
            st.markdown(
                """
            1. Select either "Upload File" or "Enter URL" tab
            2. Provide your document or URL
            3. Enter your API key
            4. Click "Generate Summary"
            5. View and download your summary
            """
            )


def choose_llm():
    with st.sidebar:
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
            f'<p class="sub-header">{api_key_label[provider]}</p>',
            unsafe_allow_html=True,
        )
        api_key = st.text_input(
            f"Enter your {api_key_label[provider]}",
            type="password",
            help=api_key_help[provider],
        )
        return provider, model, api_key


def about_expander():
    with st.expander("About this App"):
        st.write(
            """
        This application uses LangChain to provide detailed summaries of documents and web articles. 

        ### Features:
        - Upload documents in various formats (PDF, DOCX, TXT, CSV, XLSX)
        - Summarize web content by providing a URL
        - Generate comprehensive, well-structured summaries
        - Download summaries for later reference

        ### How it works:
        1. The app extracts text from your document or URL
        2. For longer documents, the text is split into manageable chunks
        3. GPT-4o-mini processes each chunk and creates a summary
        4. For multi-chunk documents, individual summaries are combined into a coherent final summary

        ### Privacy Note:
        Your API key is used only for making requests to OpenAI and is not stored or logged anywhere.
        """
        )
