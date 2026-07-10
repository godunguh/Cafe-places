!pip install streamlit
import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


def display_recommendation_details(df_results):
    """
    추천 결과 데이터프레임을 받아서 각 추천에 대한 상세 설명과 이유를 표시합니다.
    '장소명', '설명', '추천이유' 컬럼이 존재한다고 가정합니다.
    """
    if not df_results.empty:
        st.subheader("선택된 추천 장소 상세 정보")
        for index, row in df_results.iterrows():
            # '장소명' 컬럼이 존재하면 해당 이름을, 없으면 place_id를 사용
            place_name = row['장소명'] if '장소명' in row.index else f"Place ID: {row['place_id']}"
            st.write(f"### {place_name} 추천!")
            if '설명' in row.index:
                st.write(f"**설명:** {row['설명']}")
            if '추천이유' in row.index:
                st.write(f"**추천 이유:** {row['추천이유']}")
            st.markdown("---") # 각 추천 사이에 구분선 추가
    else:
        st.info("표시할 추천 상세 정보가 없습니다.")


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())
    selected_appoint = st.selectbox("예약여부 선택", df["예약필요"].unique())
    selected_inout = st.selectbox("실내여부 선택", df["실내여부"].unique())
    selected_time = st.number_input(
        "최대 소요시간",
        min_value=0,
        value=300,
        step=10
    )
    selected_good = st.number_input(
        "최대 평점",
        min_value=0,
        value=5,
        step=1
    )
    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget) &
        (df["예약필요"] == selected_appoint) &
        (df["실내여부"] == selected_inout) &
        (df["평점"] <= selected_good) &
        (df["평균소요시간(분)"] <= selected_time)


    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
        # 새로 추가된 기능: 추천 상세 정보 및 이유 표시
        display_recommendation_details(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)





'''import streamlit as st
import pandas as pd

st.title("강원생활도우미앱 3.0")


def load_data(uploaded_file):
    place_df = pd.read_excel(uploaded_file, sheet_name="장소정보")
    recommend_df = pd.read_excel(uploaded_file, sheet_name="추천정보")
    return place_df, recommend_df


def join_data(place_df, recommend_df):
    merged_df = pd.merge(
        recommend_df,
        place_df,
        on="place_id",
        how="left"
    )

    return merged_df


def show_original_data(place_df, recommend_df):
    st.subheader("장소정보 시트")
    st.dataframe(place_df)

    st.subheader("추천정보 시트")
    st.dataframe(recommend_df)


def show_joined_data(df):
    st.subheader("조인된 데이터")
    st.dataframe(df)


def search_recommendations(df):
    st.subheader("추천 장소 검색")

    selected_region = st.selectbox("지역 선택", df["지역"].unique())
    selected_purpose = st.selectbox("추천목적 선택", df["추천목적"].unique())
    selected_situation = st.selectbox("추천상황 선택", df["추천상황"].unique())
    selected_target = st.selectbox("추천대상 선택", df["추천대상"].unique())
    selected_appoint = st.selectbox("예약여부 선택", df["예약필요"].unique())
    selected_inout = st.selectbox("실내여부 선택", df["실내여부"].unique())
    selected_time = st.number_input(
        "최대 소요시간",
        min_value=0,
        value=300,
        step=10
    )
    selected_good = st.number_input(
        "최대 평점",
        min_value=0,
        value=5,
        step=1
    )
    selected_budget = st.number_input(
        "최대 예산",
        min_value=0,
        value=10000,
        step=1000
    )

    result = df[
        (df["지역"] == selected_region) &
        (df["추천목적"] == selected_purpose) &
        (df["추천상황"] == selected_situation) &
        (df["추천대상"] == selected_target) &
        (df["예산"] <= selected_budget) & 
        (df["예약필요"] == selected_appoint) &
        (df["실내여부"] == selected_inout) &
        (df["평점"] <= selected_good) &
        (df["평균소요시간(분)"] <= selected_time)

        
    ]

    st.subheader("검색 결과")

    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 추천 장소가 없습니다.")


def show_chart(df):
    st.subheader("데이터 시각화")

    chart_option = st.selectbox(
        "시각화 기준 선택",
        ["지역", "유형", "추천목적", "추천상황", "추천대상", "예약필요"]
    )

    chart_data = df[chart_option].value_counts()

    st.bar_chart(chart_data)


uploaded_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx"]
)

if uploaded_file is not None:
    place_df, recommend_df = load_data(uploaded_file)
    merged_df = join_data(place_df, recommend_df)

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["원본 데이터 보기", "조인 데이터 보기", "추천 검색", "데이터 시각화"]
    )

    if menu == "원본 데이터 보기":
        show_original_data(place_df, recommend_df)

    elif menu == "조인 데이터 보기":
        show_joined_data(merged_df)

    elif menu == "추천 검색":
        search_recommendations(merged_df)

    elif menu == "데이터 시각화":
        show_chart(merged_df)'''
