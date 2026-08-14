import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import koreanize_matplotlib

df = pd.read_csv("HR Data.csv")

candidate_columns = [
    '퇴직여부', '나이', '성별', '출장빈도', '부서', '집과의거리', '전공',
    '업무환경만족도', '업무참여도', '업무만족도', '결혼여부', '월급여',
    '일한회사수', '야근정도', '급여증가분백분율', '스톡옵션정도',
    '근속연수', '현재역할년수', '마지막승진년수'
]

hr = df[candidate_columns].copy()

hr["퇴직"] = hr["퇴직여부"].map({'Yes': 1, 'No': 0})
hr["연령대"] = pd.cut(
    hr["나이"],
    bins=[0, 20, 30, 40, 50, 60, 100],
    labels=["20 이하", "20대", "30대", "40대", "50대", "60이상"]
)
hr["근속구간"] = pd.cut(
    hr["근속연수"],
    bins=[-1, 2, 5, 10, 100],
    labels=["2년 이하", "3~5년", "6~10년", "11년 이상"]
)

# KPI 3개
total_employees = len(hr)
total_attritions = len( hr[ hr[ "퇴직여부" ] == "Yes" ] )
overall_rate = total_attritions / total_employees

col1, col2, col3 = st.columns(3)

col1.metric(label="전체 직원 수", value=f"{total_employees:,}명")
col2.metric(label="퇴직자 수", value=f"{total_attritions:,}명")
col3.metric(label="전체 퇴직률", value=f"{overall_rate:.1f}%")

age_overtime = hr.groupby( ["연령대", "야근정도"], observed=True).agg(
    직원수 = ("퇴직", "size"),
    퇴직자수 = ("퇴직", "sum"),
    퇴직률 = ("퇴직", "mean")
).reset_index()

age_overtime["퇴직률"] = (age_overtime["퇴직률"] * 100).round(1)
age_overtime.sort_values("퇴직률", ascending=False)

year_overtime = hr.groupby( ["근속구간", "야근정도"], observed=True).agg(
    직원수 = ("퇴직", "size"),
    퇴직자수 = ("퇴직", "sum"),
    퇴직률 = ("퇴직", "mean")
).reset_index()

year_overtime["퇴직률"] = (year_overtime["퇴직률"] * 100).round(1)
year_overtime.sort_values("퇴직률", ascending=False)

# 그래프 1: 20대 이하이면서 야근을 하는 집단
st.subheader("연령과 야근정도에 따른 퇴직률")

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(data=age_overtime, x="연령대", y="퇴직률", hue="야근정도", ax=ax1)
ax1.set_xlabel("연령대")
ax1.set_ylabel("퇴직률(%)")
st.pyplot(fig1)

# 그래프 2: 근속 2년 이하이면서 야근을 하는 집단
st.subheader("근속연수와 야근정도에 따른 퇴직률")

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=year_overtime, x="근속구간", y="퇴직률", hue="야근정도", ax=ax2)
ax1.set_xlabel("근속구간")
ax1.set_ylabel("퇴직률(%)")
st.pyplot(fig2)




# HR 퇴직현황 대시보드 KPI 3개, 그래프 2개 (필수)
# (도전) 사이드바(필터) , 그래프 추가
# 참고 : 04_데이터분석/R_직원퇴사분석_exercise.ipynb/6.1 