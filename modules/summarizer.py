from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from modules.prompts import single_prompt, map_prompt, combine_prompt


def get_llm(provider, api_key):
    # fmt: off
    if provider == "OpenAI":
        from langchain_openai import ChatOpenAI 
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
    elif provider == "Mistral":
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(
            model="mistral-small-latest", temperature=0.3, api_key=api_key
        )
    elif provider == "Hugging Face":
        from langchain_huggingface import HuggingFaceEndpoint
        return HuggingFaceEndpoint(
            repo_id="google/flan-t5-xxl", huggingfacehub_api_token=api_key
        )
    # Add logic for Claude, Gemini, Ollama, etc.
    # fmt: on
    else:
        raise ValueError(
            f"Provider '{provider}' is not supported or missing dependencies."
        )


def summarize_text(
    text,
    api_key,
    st,
    provider="OpenAI",
    user_prompt=None,
    map_prompt=None,
    combine_prompt=None,
):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        docs = text_splitter.create_documents([text])
        llm = get_llm(provider, api_key)

        if len(docs) <= 1 or user_prompt:
            prompt_template = user_prompt or single_prompt
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"text": text})

        map_prompt_template = map_prompt or map_prompt
        combine_prompt_template = combine_prompt or combine_prompt
        map_prompt_obj = PromptTemplate(
            template=map_prompt_template, input_variables=["text"]
        )
        combine_prompt_obj = PromptTemplate(
            template=combine_prompt_template, input_variables=["text"]
        )
        summary_chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_obj,
            combine_prompt=combine_prompt_obj,
            verbose=False,
        )
        return summary_chain.run(docs)
    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        return None
