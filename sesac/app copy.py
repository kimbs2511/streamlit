import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

st.title("매출 대시보드")

# 1. 데이터 만들기
df = pd.DataFrame({
    "직원": ["김민수", "이영희", "박철수", "최지수", "정하늘", "한유진"],
    "부서": ["영업부", "개발부", "영업부", "개발부", "영업부", "개발부"],
    "매출": [500, 300, 700, 400, 600, 800]
})

# 2. 사이드바 필터 2개
st.sidebar.header("조회 조건")

department = st.sidebar.selectbox("부서를 선택하세요.", ["전체", "영업부", "개발부"])
minimum_sales = st.sidebar.slider("최소 매출을 선택하세요.", min_value=0, max_value=800, value=0, step=100)

# 3. 데이터 필터링
result = df[df["매출"] >= minimum_sales]

if department != "전체":
    result = result[result["부서"] == department]

# 4. KPI 2개
# st.metric(label, value, delta) 지표의 이름, 현재 값, 이전 값과 비교한 증감 값
employee_count = len(result)
total_sales = result["매출"].sum()

col1, col2 = st.columns(2)

col1.metric(label="직원 수", value=f"{employee_count}명", delta="+1명")
col2.metric(label="총매출", value=f"{total_sales:,}만원", delta="-300만원")

# 5. 그래프 1: 직원별 매출
st.subheader("직원별 매출")

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(data=result, x="직원", y="매출", ax=ax1)
ax1.set_xlabel("직원")
ax1.set_ylabel("매출(만원)")
st.pyplot(fig1)

# 6. 그래프 2: 부서별 평균 매출
st.subheader("부서별 평균 매출")

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=result, x="부서", y="매출", ax=ax2)
ax2.set_xlabel("부서")
ax2.set_ylabel("평균 매출(만원)")
st.pyplot(fig2)

# 7. 그래프 subplots()
graph_col1, graph_col2 = st.columns(2)

graph_col1.subheader("직원별 매출")

fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.barplot(data=result, x="직원", y="매출", ax=ax1)
ax1.set_xlabel("직원")
ax1.set_ylabel("매출(만원)")
ax1.tick_params(axis="x", rotation=30)
graph_col1.pyplot(fig1)

graph_col2.subheader("부서별 평균 매출")

fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(data=result, x="부서", y="매출", ax=ax2)
ax2.set_xlabel("부서")
ax2.set_ylabel("평균 매출(만원)")
graph_col2.pyplot(fig2)

# table
st.write(result)

# table
st.table(result)