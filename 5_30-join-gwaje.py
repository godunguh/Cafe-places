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


def generate_recommend_reason(row):
    """
    주어진 데이터프레임 행(row)에서 추천 이유 문자열을 생성합니다.
    """
    reason_parts = []
    place_name = row.get('장소명', '알 수 없는 장소')

    reason_parts.append(f"이 장소 '{place_name}'는 ")

    if '실내여부' in row.index:
        if row['실내여부'] == '실내':
            reason_parts.append("실내에서 즐길 수 있으며")
        elif row['실내여부'] == '실외':
            reason_parts.append("야외에서 즐길 수 있으며")

    if '예산' in row.index:
        if pd.notna(row['예산']) and row['예산'] > 0:
            reason_parts.append(f"예산이 {row['예산']:,}원으로")
            if row['예산'] < 10000: # 예산 범위에 따라 '저렴' 또는 '적당' 판단
                reason_parts.append("비교적 저렴하고")
            else:
                reason_parts.append("적당하며")

    if '평점' in row.index and pd.notna(row['평점']) and row['평점'] >= 4.0:
        reason_parts.append("평점이 높아")
    elif '평점' in row.index and pd.notna(row['평점']) and row['평점'] > 0:
        reason_parts.append(f"평점이 {row['평점']}이고")

    if '평균소요시간(분)' in row.index and pd.notna(row['평균소요시간(분)']):
        if row['평균소요시간(분)'] <= 60:
            reason_parts.append("평균 소요시간이 짧아")
        else:
            reason_parts.append(f"평균 소요시간이 {row['평균소요시간(분)']}분으로")

    if '추천목적' in row.index and pd.notna(row['추천목적']):
        reason_parts.append(f"{row['추천목적']}에 적합하여")

    if '추천상황' in row.index and pd.notna(row['추천상황']):
        reason_parts.append(f"{row['추천상황']}에 잘 어울리며")

    if '추천대상' in row.index and pd.notna(row['추천대상']):
        reason_parts.append(f"{row['추천대상']}에게 좋은 곳이라")

    # 마지막 '그리고' 또는 '하며' 연결 제거 및 마침표 추가
    if reason_parts and len(reason_parts) > 1:
        # 마지막 두 요소를 합치고 '추천합니다.' 추가
        final_reason = " ".join(reason_parts[1:])
        final_reason = final_reason.strip()
        if final_reason.endswith('이고'):
            final_reason = final_reason[:-2] + '기 때문에'
        elif final_reason.endswith('하며'):
            final_reason = final_reason[:-2] + '기에'
        elif final_reason.endswith('하고'):
            final_reason = final_reason[:-2] + '므로'
        elif final_reason.endswith('이라'):
            final_reason = final_reason[:-2] + '입니다.'
        elif final_reason.endswith('고'):
            final_reason = final_reason[:-1] + '며'

        return f"{reason_parts[0]}{final_reason} 추천합니다."
    else:
        return f"이 장소 '{place_name}'에 대한 추천 이유를 생성하기 어렵습니다."


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
    ].copy() # 기존 DataFrame을 직접 수정하지 않고 copy() 사용

    st.subheader("검색 결과")

    if not result.empty:
        st.dataframe(result)
        st.subheader("추천 이유")
        for index, row in result.iterrows():
            reason = generate_recommend_reason(row)
            st.write(reason)
            st.markdown("----") # 각 추천 이유 사이에 구분선 추가
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
