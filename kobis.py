import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
# 1. import 추가
from dotenv import load_dotenv
from openai import OpenAI
from matplotlib.ticker import MaxNLocator
import numpy as np
import requests

# 페이지 설정
st.set_page_config(page_title="영화산업의 현재", page_icon="🎬", layout="wide")
st.title("🎬영화 시장 분석")
st.write("2008년 ~ 2026년 극장 개봉 영화 데이터를 분석")

# 데이터 불러오기 및 준비
@st.cache_data

def load_data(path, encoding="utf-8"):
    try:
        data = pd.read_csv(path, encoding=encoding)

    except UnicodeDecodeError:
        # cp949, utf-8-sig
        alternative_encoding = 'cp949' if encoding == 'utf-8' else 'utf-8'
        data = pd.read_csv(path, encoding=alternative_encoding)
        
    return data

# 영화일람
df_ticket = load_data("raw_data/kobis20260811.csv")

# 전국 인구수
df_pop = load_data("raw_data/도시지역_인구현황_시군구__20260811102832.csv")
condition = df_pop["세종특별자치시"].isna()
df_pop.loc[condition, "세종특별자치시"] = 0
df_pop["전국대비서울"] = df_pop["서울특별시"] / df_pop["전국"] * 100

# 평균티켓가격
year_ticket = df_ticket.groupby("개봉연도").agg(
    평균티켓가격 = ("예측티켓값", "mean")
).reset_index()

# 전국대비서울 영화 관람객수
year_percent = df_ticket.groupby("개봉연도").agg(
    전국대비서울 = ("전국대비서울", "mean")
).reset_index()
year_percent = year_percent[:-2]
year_percent["인구조사비율"] = df_pop["전국대비서울"]

# 사이드바
st.sidebar.header("🔍 데이터 필터링")

# 개봉연도 최소/최대값 추출
min_year = int(df_ticket["개봉연도"].min())
max_year = int(df_ticket["개봉연도"].max())

# 사이드바 슬라이더 생성
selected_years = st.sidebar.slider(
    "조회 연도 범위 선택",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 데이터 필터링 적용
filtered_df_ticket = df_ticket[(df_ticket["개봉연도"] >= selected_years[0]) & (df_ticket["개봉연도"] <= selected_years[1])]
filtered_year_percent = year_percent[(year_percent["개봉연도"] >= selected_years[0]) & (year_percent["개봉연도"] <= selected_years[1])]

# KPI?
st.subheader("개봉영화")

rankings = filtered_df_ticket.sort_values("전국관객수", ascending=False).head(10)
rankings = rankings[ ["영화명","영화형태", "국적", "전국관객수", "서울관객수",
                      "장르", "등급", "개봉연도", "개봉월"]]

top_movie_name = rankings.iloc[0, 0]
top_movie_year = rankings.iloc[0, 7]
top_movie_month = rankings.iloc[0, 8]
top_movie_audience = int(rankings.iloc[0, 3])

st.metric(
   "조회 기간 내 최고 인기 영화",
    f"{top_movie_name} ({top_movie_year})",
    delta=f"{top_movie_audience:,}명"
)

with st.expander("10위권 내 전체 정보"):

    st.dataframe(
        rankings,
        hide_index=True,
        use_container_width=True
    )


# 그래프 출력

col1, col2 = st.columns(2)

# 첫 번째 그래프
kor_movie = filtered_df_ticket.groupby("국내외구분").agg(
    합계 = ("국내외구분", "count")
).reset_index()

col1.subheader("한국영화 비율")

fig1, ax1 = plt.subplots(figsize=(3, 2))

plt.pie(
    kor_movie["합계"],
    labels=kor_movie["국내외구분"],
    autopct='%1.1f%%',
    startangle=90,
    counterclock=False
)

col1.pyplot(fig1, use_container_width=True)
plt.close(fig1)


# 두 번째 그래프
genre_movie = filtered_df_ticket.groupby("장르").agg(
    합계 = ("장르", "count")
).reset_index()

col2.subheader("장르영화 비율")

fig2, ax2 = plt.subplots(figsize=(5, 4))

sns.barplot(
    genre_movie.sort_values("합계", ascending=False).tail(10),
    x="장르",
    y="합계",
    color="green",
    ax=ax2
)

ax2.tick_params(axis='x', rotation=60, labelsize=10)


col2.pyplot(fig2, use_container_width=True)
plt.close(fig2)

col3, col4 = st.columns(2)

# 세 번째 그래프
col3.subheader("전국대비 서울 관객수")

fig3, ax3 = plt.subplots(figsize=(5, 3))

y_min = 15
y_max = 55
y_margin = (y_max - y_min) * 0.05
y_limit_range = (y_min - y_margin, y_max + y_margin)

sns.barplot(
    filtered_year_percent,
    x="개봉연도",
    y="전국대비서울",
    alpha = 0.6,
    ax=ax3
)
ax3.set_ylabel("전국대비 서울 관객수 비율 (%)", color="blue")
ax3.tick_params(axis='y', labelcolor="blue")
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))

ax4 = ax3.twinx()

sns.lineplot(
    filtered_year_percent,
    x= np.arange( len(filtered_year_percent) ),
    y= filtered_year_percent["인구조사비율"],
    color="red",
    marker="o",
    linestyle="--",
    linewidth=2,
    ax=ax4
)
ax4.set_ylabel("전국대비 서울 인구수 비율 (%)", color="red")
ax4.tick_params(axis='y', labelcolor="red")

ax3.set_ylim(y_limit_range)
ax4.set_ylim(y_limit_range)


col3.pyplot(fig3, use_container_width=True)
plt.close(fig3)

# 4번째 그래프
year_movie = filtered_df_ticket.groupby("개봉연도").agg(
    합계 = ("개봉연도", "count")
).reset_index()

col4.subheader("연도별 영화 개봉")
fig5, ax5 = plt.subplots(figsize=(5, 3))

sns.barplot(
    year_movie,
    x="개봉연도",
    y="합계",
    ax=ax5
)

ax5.tick_params(axis='x', rotation=60, labelsize=10)

col4.pyplot(fig5, use_container_width=True)
plt.close(fig5)
