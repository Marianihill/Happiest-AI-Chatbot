import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.llms import ollama


st.set_page_config(page_title="Happiest AI ChatBot")


st.markdown("""
    <style>
        body {
            background-color: #e6f7ff;
        }
        .stApp {
            background-color: #e6f7ff;
        }
        .stChatMessage {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


st.title("Happiest AI ChatBot")


if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Hello! I'm Happiest AI Assistant 😊 Created by Marianihill. How can I help you today?")
    ]


for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Your name is Happy Assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

llm = ollama.Ollama(model="llama2")  
output_parser = StrOutputParser()
chain = prompt | llm | output_parser


user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

  
    response = chain.invoke({
        "input": user_input,
        "chat_history": st.session_state.messages
    })

    st.session_state.messages.append(AIMessage(content=response))
    with st.chat_message("assistant"):
        st.markdown(response)
