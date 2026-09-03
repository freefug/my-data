import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜와 평균기온을 숫자/날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


# 데이터 불러오기
df = load_data()

# 연도별 평균기온 계산
annual_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

annual_temp.columns = ["연도", "연평균기온"]

# 연도순으로 정렬
annual_temp = annual_temp.sort_values("연도")

# 최근 100년 데이터 선택
annual_temp = annual_temp.tail(100)


# -------------------------
# 화면
# -------------------------

st.title("🌡️ 서울의 100년간 연평균 기온 변화")

st.write(
    "서울의 일별 평균기온 데이터를 연도별로 평균하여 "
    "100년 동안 연평균 기온이 어떻게 변해 왔는지 나타낸 그래프입니다."
)

# 분석 기간
start_year = int(annual_temp["연도"].min())
end_year = int(annual_temp["연도"].max())

st.info(f"📅 분석 기간: {start_year}년 ~ {end_year}년")


# 그래프
st.subheader("📈 연도별 연평균 기온")

chart_data = annual_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="연평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)",
    use_container_width=True
)


# 통계
col1, col2, col3 = st.columns(3)

with col1:
    min_temp = annual_temp["연평균기온"].min()
    min_year = annual_temp.loc[
        annual_temp["연평균기온"].idxmin(), "연도"
    ]

    st.metric(
        "가장 낮은 연평균 기온",
        f"{min_temp:.1f} ℃",
        f"{int(min_year)}년"
    )

with col2:
    max_temp = annual_temp["연평균기온"].max()
    max_year = annual_temp.loc[
        annual_temp["연평균기온"].idxmax(), "연도"
    ]

    st.metric(
        "가장 높은 연평균 기온",
        f"{max_temp:.1f} ℃",
        f"{int(max_year)}년"
    )

with col3:
    change = (
        annual_temp.iloc[-1]["연평균기온"]
        - annual_temp.iloc[0]["연평균기온"]
    )

    st.metric(
        "처음과 마지막 연도의 차이",
        f"{change:+.1f} ℃"
    )


# 연도별 데이터 확인
with st.expander("📋 연도별 연평균 기온 데이터 보기"):
    display_data = annual_temp.copy()
    display_data["연평균기온"] = display_data["연평균기온"].round(2)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


st.caption("데이터 출처: seoul.csv (greatsong/modudata)")
