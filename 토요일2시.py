import streamlit as st

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import ChatMessage
from langchain_teddynote.prompts import load_prompt

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

