import streamlit as st
st.title("카페")

places = [
    {"이름": "칠성조선소", "지역": "속초", "실내여부": "실내외", "평점": 4.4, "대표메뉴": "메이플 마롱 밀크"},
    {"이름": "감자밭", "지역": "춘천", "실내여부": "실내외", "평점": 4.5, "대표메뉴": "강원도 감자빵"},
    {"이름": "커피공장", "지역": "강릉", "실내여부": "실내외", "평점": 4.6, "대표메뉴": "핸드드립 커피"},
    {"이름": "갤러리밥스", "지역": "강릉", "실내여부": "실내", "평점": 4.5, "대표메뉴": "초옥이커피"}
]

def get_recommendations(places, region, indoor):
    result = []
    for place in places:
        if place["지역"] == region and place["실내여부"] == indoor:
            result.append(place)
    return result

st.title("강원 청소년 생활 도우미(카페)")
selected_region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
selected_indoor = st.radio("실내 여부를 선택하세요", ["실내", "실내외"])


if st.button("추천 보기"):
    recommendations = get_recommendations(places, selected_region, selected_indoor)

    if len(recommendations) == 0:
        st.write("해당하는 장소 없음")
    else:
        for place in recommendations:
            st.write(place["이름"])
            st.write(place["지역"])
            st.write(place["실내여부"])
            st.write(place["평점"])
            st.write(place["대표메뉴"])
            st.write("---")

