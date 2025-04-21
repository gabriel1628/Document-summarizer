from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from modules.prompts import single_prompt, map_prompt, combine_prompt


def get_llm(provider, api_key, model):
    # fmt: off
    if provider == "OpenAI":
        from langchain_openai import ChatOpenAI 
        return ChatOpenAI(model=model, temperature=0.3, api_key=api_key)
    elif provider == "Mistral":
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(model=model, temperature=0.3, api_key=api_key)
    elif provider == "Hugging Face":
        from langchain_huggingface import HuggingFaceEndpoint
        return HuggingFaceEndpoint(repo_id=model, huggingfacehub_api_token=api_key)
    # Add logic for Claude, Gemini, Ollama, etc., using the selected model
    else:
        raise ValueError(
            f"Provider '{provider}' is not supported or missing dependencies."
        )


def summarize_text(
    text,
    api_key,
    st,
    provider="OpenAI",
    map_prompt=None,
    combine_prompt=None,
    model=None,
):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        docs = text_splitter.create_documents([text])
        llm = get_llm(provider, api_key, model)

        if len(docs) <= 1:
            print("Using single prompt for summarization.")
            prompt_template = single_prompt
            prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"text": text})
        else:
            print("Using map-reduce prompt for summarization.")
            map_prompt_template = map_prompt
            combine_prompt_template = combine_prompt
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
            result = summary_chain.invoke(docs)
            return result["output_text"]
    except Exception as e:
        st.error(f"Error in summarization: {str(e)}")
        return None
