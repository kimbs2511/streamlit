import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

## .env 파일에서 OPENAI_API_KEY를 부분 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

## client 객체 생성
client = OpenAI(api_key=api_key)

st.title("💬 간단한 챗봇")

# 1. [추가] 화면에 표시할 전체 대화 기록을 저장하는 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 응답 ID 저장
if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

# 2. [추가] 앱이 새로고침될 때마다 이전에 저장된 대화 기록을 화면에 순서대로 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("질문을 입력하세요.")

if question:
    # user: 사용자가 입력한 질문
    with st.chat_message("user"):
        st.write(question)
    st.session_state.messages.append({"role": "user", "content": question})
    # AI 모델에 질문을 보내고 답변을 받는 부분
    # 첫 질문인지 이후 질문인지 구분
    if st.session_state.previous_response_id is None:
        response = client.responses.create(
            model=MODEL,
            input=question,
        )

    else:
        response = client.responses.create(
            model=MODEL,
            previous_response_id=st.session_state.previous_response_id,
            input=question,
        )

    st.session_state.previous_response_id = response.id

    # assistant: AI가 생성한 답변
    with st.chat_message("assistant"):
        ## AI 모델의 답변을 출력하는 부분
        st.write(response.output_text)
    st.session_state.messages.append({"role": "assistant", "content": response.output_text})
