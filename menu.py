import streamlit as st

  def filter_places():
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.warning("조건에 맞는 장소가 없습니다.")

    region_count = df["지역"].value_counts()

  def show_charts():
    st.subheader("지역별 장소 개수")
    st.bar_chart(region_count)

    type_count = df["유형"].value_counts()

    st.subheader("유형별 장소 개수")
    st.bar_chart(type_count)

    avg_score = df.groupby("지역")["평점"].mean()

    st.subheader("지역별 평균 평점")
    st.bar_chart(avg_score)  
      
menu = st.sidebar.radio("원하는 기능 선택", ["데이터 확인", "조건검색"])

if menu == "데이터 확인" :
  filter_places()
  show_charts()
