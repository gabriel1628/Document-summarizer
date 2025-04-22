import streamlit as st
from langchain_core.prompts import PromptTemplate


def chat_about_summary(summary, llm):
    st.markdown("### Ask questions about the summary")
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("Ask a question about the summary"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_question)
        # Simple prompt template for Q&A over the summary
        qa_prompt = PromptTemplate(
            template=(
                "Given the following summary:\n\n{summary}\n\n"
                "Answer the user's question:\n{question}\n\nAnswer:"
            ),
            input_variables=["summary", "question"],
        )
        prompt = qa_prompt.format(summary=summary, question=user_question)
        # Add Q&A prompt to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        result = llm.invoke(prompt)
        response = result.content
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
