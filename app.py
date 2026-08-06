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

st.write(hr)

# uv run streamlit run app.py  
total_employees = 1
# print(f'전체 직원 수: {total_employees:,}명')
# print(f'퇴직자 수: {total_attritions:,}명')
# print(f'전체 퇴직률: {overall_rate:.1f}%')


# HR 퇴직현황 대시보드 KPI 3개, 그래프 2개 (필수)
# (도전) 사이드바(필터) , 그래프 추가
# 참고 : 04_데이터분석/R_직원퇴사분석_exercise.ipynb/6.1 