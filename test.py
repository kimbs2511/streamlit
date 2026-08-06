import streamlit as st

st.title("인사 앱")

name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name}님! 반갑습니다.")

# 버튼 동작
if st.button("인사하기"):
    st.write(f"{name}님, 좋은 하루 되세요!")


# 사이드바, 왼쪽 영역
st.sidebar.title("조회 조건")

dept = st.sidebar.selectbox("부서를 선택하세요",
                 ["전체", "인사팀", "영업팀", "개발팀"] )

st.write(f"선택한 부서: {dept}")

# 재미있는 기능
if st.button("재미있는 기능"):
    st.balloons() # 풍선 날리기
    st.snow()     # 눈 내리기

# 여러 종류의 안내 메시지
st.info("정보 안내 메시지")
st.success("성공 안내 메시지")
st.warning("경고 안내 메시지")
st.error("오류 안내 메시지")

# uv run streamlit run test.py