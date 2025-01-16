import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_teddynote.prompts import load_prompt

from dotenv import load_dotenv
import os

load_dotenv(verbose=True)
key = os.getenv('OPENAI_API_KEY')

st.title('나만의 chatGPT')

# 처음 1번만 실행
if 'messages' not in st.session_state:
    st.session_state['messages'] = []       # 대화 기록을 저장하기 위한 용도

with st.sidebar:                            
    clear_btn = st.button('대화다시')       
    
    selected_prompt = st.selectbox(
        '프롬프트를 선택해 주세요.', 
        ('기본모드','게시글'), index=0
    )


# 저장된 대화를 화면에 출력(이전 대화를 출력)
def print_messages():
    for chat_message in st.session_state['messages']:
        with st.chat_message(chat_message.role):          # 이모티콘(assistant, 사용자)
            st.write(chat_message.content)                # 내용(시스템 답변, 사용자 입력)

# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

# 체인
def create_chain(prompt_type):       
    if prompt_type=='기본모드':           
        prompt = ChatPromptTemplate.from_messages(
            [
                ('system', '당신은 친절한 AI 어시스턴트입니다. 다음의 질문에 간결하게 답변해 주세요.'), 
                ('user', '#Questin:\n{question}'),
            ]
        )
    elif prompt_type=='게시글':
        prompt = load_prompt('prompts/blog.yaml', encoding='utf-8')
    
    llm = ChatOpenAI(                     # llm
        api_key=key, 
        model_name='gpt-4o-mini',
        temperature=0,			    
        max_tokens=2048,			
    )
    
    output_parser = StrOutputParser()     # 출력 파서    
    chain = prompt | llm | output_parser  # 체인
    return chain


if clear_btn:                                              # 버튼이 눌러지면
    st.session_state['messages'] = []
        
print_messages()                                           # 저장된 대화를 화면에 출력

user_input = st.chat_input('궁금한 내용을 물어보세요')     # 사용자 입력


if user_input:                                             # 사용자 입력이 들어있으면

    with st.chat_message('user'):                          # 사용자 아이콘
        st.write(user_input)                               # 사용자가 입력한 내용 출력


    chain = create_chain(selected_prompt)                  # 위에서 선택한 프롬프트를 인자로 넘긴다
    response = chain.stream({'question': user_input})      # 질문을 넣어 호출한다


    with st.chat_message('assistant'):                     # assistant 아이콘
        container = st.empty()                             # 빈공간에 토큰을 스트리밍 출력한다.

        answer = ''                                        # 문자열을 저장할 변수

        for token in response:
            answer += token
            container.markdown(answer)
            
    
    add_message('user', user_input)                         # 대화 내용을 기록한다
    add_message('assistant', answer)                        # 대화 내용을 기록한다    