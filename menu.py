import streamlit as st
import pandas as pd

def load_data():
    uploaded_file = st.file_uploader(
        "장소 데이터 엑셀 파일을 업로드하세요",
        type=["xlsx"]
    )

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # 업로드한 데이터를 session_state에 저장
        st.session_state["df"] = df

        st.success("엑셀 파일이 업로드되었습니다.")
        st.subheader("업로드한 장소 데이터")
        st.dataframe(df)

    else:
        st.info("엑셀 파일을 업로드하면 데이터가 표시됩니다.")


# 저장된 데이터 가져오기 함수
def get_data():
    if "df" not in st.session_state:
        st.warning("먼저 '엑셀 입력' 메뉴에서 엑셀 파일을 업로드하세요.")
        return None

    return st.session_state["df"]

def get_user_input():
    selected_region = st.selectbox("지역을 선택하세요", df["지역"].unique())
    selected_budget = st.number_input("사용 가능한 예산을 입력하세요", min_value=0, value=10000, step=1000)

    result = df[
        (df["지역"] == selected_region) &
        (df["예산"] <= selected_budget)
    ]


def filter_places():
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다.")

    region_count = df["지역"].value_counts()

def show_charts(df):
    st.subheader("지역별 장소 개수")
    st.bar_chart(region_count)

    type_count = df["유형"].value_counts()

    st.subheader("유형별 장소 개수")
    st.bar_chart(type_count)

    avg_score = df.groupby("지역")["평점"].mean()

    st.subheader("지역별 평균 평점")
    st.bar_chart(avg_score)
      
menu = st.sidebar.radio("원하는 기능 선택", ["엑셀 입력", "데이터 확인", "조건검색"])

if menu == "엑셀 입력" :
    load_data()
    
elif menu == "데이터 확인" :
    show_charts(df)

elif menu == "조건검색" :
    get_user_input()
    filter_places()

