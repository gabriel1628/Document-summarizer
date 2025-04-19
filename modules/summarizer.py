from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

# Import providers as needed
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None
try:
    from langchain_mistralai import ChatMistralAI
except ImportError:
    ChatMistralAI = None
try:
    from langchain_community.llms import HuggingFaceEndpoint
except ImportError:
    HuggingFaceEndpoint = None
# Add imports for Claude, Gemini, Ollama, etc. as needed


def get_llm(provider, api_key):
    if provider == "OpenAI" and ChatOpenAI:
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
    elif provider == "Mistral" and ChatMistralAI:
        return ChatMistralAI(
            model="mistral-small-latest", temperature=0.3, api_key=api_key
        )
    elif provider == "Hugging Face" and HuggingFaceEndpoint:
        return HuggingFaceEndpoint(
            repo_id="google/flan-t5-xxl", huggingfacehub_api_token=api_key
        )
    # Add logic for Claude, Gemini, Ollama, etc.
    else:
        raise ValueError(
            f"Provider '{provider}' is not supported or missing dependencies."
        )


def summarize_text(text, api_key, st, provider="OpenAI"):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        docs = text_splitter.create_documents([text])
        llm = get_llm(provider, api_key)

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
