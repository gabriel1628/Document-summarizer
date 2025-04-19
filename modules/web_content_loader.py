from langchain_community.document_loaders import WebBaseLoader


def extract_text_from_url(url, st):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        text = " ".join([doc.page_content for doc in docs])
        return text
    except Exception as e:
        st.error(f"Error fetching URL: {str(e)}")
        return None
