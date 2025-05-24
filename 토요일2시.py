import streamlit as st

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import ChatMessage
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')

st.title('문서 검색 GPT')

if not os.path.exists('.cache'):
    os.mkdir('.cache')

if not os.path.exists('.cache/files'):
    os.mkdir('.cache/files')

if not os.path.exists('.cache/embeddings'):
    os.mkdir('.cache/embeddings')

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'chain' not in st.session_state:
    st.session_state['chain'] = None


with st.sidebar:
    clear_btn = st.button('대화 다시')
    upload_file = st.file_uploader('파일 업로드', type=['pdf'])


def print_message():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):
            st.write(chat_message.content)


def add_message(role, message):
    st.session_state['messages'].append(
        ChatMessage(role=role, content=message)
    )

@st.cache_resource(show_spinner='업로드 한 파일을 처리중...')
def embed_file(file):
    file_content = file.read()
    file_path = f'./.cache/files/{file.name}'

    with open(file_path, 'wb') as f:
        f.write(file_content)

    # 1단계 : 문서 불러 오기
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()

    # 2단계 : 문서 자르기
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # 3단계 : 임베딩 생성
    embeddings = OpenAIEmbeddings(api_key=key, model='text-embedding-3-small')

    # 4단계 : DB 생성 및 저장
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    # 5단계 : 검색기
    retriever = vectorstore.as_retriever()

    return retriever


def create_chain(retriever):
    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say you don't know.
        Answer in Korean.

        #Context:
        {context}

        #Question:
        {question}

        #Answer:"""
    )

    llm = ChatOpenAI(
        api_key=key,
        model='gpt-4o-mini'
    )

    chain = (
        {'context': retriever, 'question': RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if upload_file:
    retriever = embed_file(upload_file)
    chain = create_chain(retriever)
    st.session_state['chain'] = chain


print_message()

user_input = st.chat_input('무엇을 도와드릴까요?')

if user_input:

    chain = st.session_state['chain']

    if chain is not None:
        with st.chat_message('user'):
            st.write(user_input)

        response = chain.stream(user_input)

        with st.chat_message('assistant'):
            container = st.empty()

            answer = ''

            for token in response:
                answer += token
                container.markdown(answer)

        add_message('user', user_input)
        add_message('assistant', answer)
