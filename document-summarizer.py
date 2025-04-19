import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
import os
import tempfile
import io
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd

# Set the page title and layout
st.set_page_config(page_title="Document Summarizer", layout="wide")

# Add custom CSS
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

# Create the main page title
st.markdown('<p class="main-header">Document Summarizer</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="info-text">Upload a file or enter a URL to get a detailed summary.</p>',
    unsafe_allow_html=True,
)

# Set up tabs for file upload and URL
tab1, tab2 = st.tabs(["Upload File", "Enter URL"])


# Function to extract text from different file types
def extract_text_from_file(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()
    text = ""

    try:
        if file_extension == "txt":
            text = uploaded_file.getvalue().decode("utf-8")
        elif file_extension == "pdf":
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file_extension in ["docx", "doc"]:
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_extension in ["xlsx", "xls", "csv"]:
            if file_extension in ["xlsx", "xls"]:
                df = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
            else:
                df = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))
            text = df.to_string()
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None

        return text
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


# Function to summarize text using LangChain
def summarize_text(text, api_key):
    try:
        # Create a text splitter to handle long texts
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )

        # Split the text into chunks
        docs = text_splitter.create_documents([text])

        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)

        # If the text is short enough, use a simple prompt
        if len(docs) <= 1:
            prompt_template = """
            Write a comprehensive summary of the following text. The summary should:
            1. Highlight the main points and key ideas
            2. Include important details and supporting evidence
            3. Maintain the original meaning and intent
            4. Be well-structured and coherent
            
            Text to summarize:
            {text}
            
            Comprehensive Summary:
            """

            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"text": text})

        # For longer texts, use a map-reduce summarization approach
        map_prompt_template = """
        Write a concise summary of the following text, focusing on the key points:
        {text}
        
        Concise Summary:
        """

        combine_prompt_template = """
        You are provided with multiple summaries from different sections of a document or article.
        Your task is to create a comprehensive, well-structured final summary that:
        1. Integrates all the important information from the individual summaries
        2. Presents a coherent overview of the entire content
        3. Organizes the information logically with appropriate headings and structure
        4. Eliminates redundancy while preserving important details
        
        Individual summaries:
        {text}
        
        Comprehensive Final Summary:
        """

        map_prompt = PromptTemplate(
            template=map_prompt_template, input_variables=["text"]
        )
        combine_prompt = PromptTemplate(
            template=combine_prompt_template, input_variables=["text"]
        )

        # Create and run the summarization chain
        summary_chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt,
            combine_prompt=combine_prompt,
            verbose=False,
        )

        return summary_chain.run(docs)

    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        return None


# Tab 1: File Upload
with tab1:
    st.markdown('<p class="sub-header">Upload Document</p>', unsafe_allow_html=True)
    st.write("Supported formats: PDF, DOCX, TXT, CSV, XLSX")

    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "txt", "csv", "xlsx"]
    )

    if uploaded_file is not None:
        with st.spinner("Processing file..."):
            text = extract_text_from_file(uploaded_file)
            if text:
                st.success(f"Successfully processed {uploaded_file.name}")
                # Show a preview of the extracted text
                with st.expander("Text Preview (first 500 characters)"):
                    st.write(text[:500] + ("..." if len(text) > 500 else ""))

# Tab 2: URL Input
with tab2:
    st.markdown('<p class="sub-header">Enter URL</p>', unsafe_allow_html=True)
    url = st.text_input("Web Page URL", placeholder="https://example.com/article")

    if url:
        with st.spinner("Fetching content from URL..."):
            try:
                # Load the web page
                loader = WebBaseLoader(url)
                docs = loader.load()
                text = " ".join([doc.page_content for doc in docs])

                st.success(f"Successfully fetched content from URL")
                # Show a preview of the extracted text
                with st.expander("Text Preview (first 500 characters)"):
                    st.write(text[:500] + ("..." if len(text) > 500 else ""))
            except Exception as e:
                st.error(f"Error fetching URL: {str(e)}")
                text = None

# Common section for API key and summarization
st.markdown('<p class="sub-header">OpenAI API Key</p>', unsafe_allow_html=True)
api_key = st.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Your API key is required. It is not stored anywhere.",
)

# Initialize the session state if it doesn't exist
if "summary" not in st.session_state:
    st.session_state.summary = None

# Summarize button
if st.button("Generate Summary"):
    if not api_key:
        st.error("Please enter your OpenAI API Key")
    elif "text" in locals() and text:
        with st.spinner("Generating summary..."):
            summary = summarize_text(text, api_key)
            if summary:
                st.session_state.summary = summary
    else:
        st.warning("Please upload a file or enter a valid URL first")

# Display the summary if available
if st.session_state.summary:
    st.markdown('<p class="sub-header">Summary</p>', unsafe_allow_html=True)
    st.markdown(st.session_state.summary)

    # Add a download button for the summary
    st.download_button(
        label="Download Summary",
        data=st.session_state.summary,
        file_name="document_summary.txt",
        mime="text/plain",
    )

# Display information about the app
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

# GitHub link in the sidebar
st.sidebar.markdown("### Document Summarizer")
st.sidebar.markdown("A Streamlit app powered by LangChain")
st.sidebar.markdown("---")
st.sidebar.markdown("### How to use:")
st.sidebar.markdown(
    """
1. Select either "Upload File" or "Enter URL" tab
2. Provide your document or URL
3. Enter your OpenAI API key
4. Click "Generate Summary"
5. View and download your summary
"""
)
