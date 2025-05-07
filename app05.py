from typing import List, Dict
from langchain.tools import tool
from langchain_teddynote.tools import GoogleNews

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_teddynote.messages import AgentStreamParser

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.agent_toolkits import FileManagementToolkit

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

# 폴더 생성하고 시작.
if not os.path.exists('tmp'):   # tmp 라는 폴더가 없으면
    os.mkdir('tmp')             # tmp 라는 이름의 폴더를 만든다
