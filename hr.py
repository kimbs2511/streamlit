import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

hr = pd.read_csv("C:/Users/SBA/Downloads/HR Data.csv")
# st.write(hr.shape)

print(f'전체 직원 수: {total_employees:,}명')
print(f'퇴직자 수: {total_attritions:,}명')
print(f'전체 퇴직률: {overall_rate:.1f}%')


# HR 퇴직현황 대시보드 KPI 3개, 그래프 2개 (필수)
# (도전) 사이드바(필터) , 그래프 추가
# 참고 : 04_데이터분석/R_직원퇴사분석_exercise.ipynb/6.1 