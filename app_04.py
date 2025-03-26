from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(
    api_key=key,
    model='gpt-4o-mini',
    temperature=0
)

qusetion = HumanMessage(content='대한민국의 수도는 어디야?', id='1')
answer = llm.invoke(qusetion.content)
print(answer)
