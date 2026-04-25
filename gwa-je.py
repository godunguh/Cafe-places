import streamlit as st

if "places" not in st.session_state:
    st.session_state.places = [
    {"이름": "칠성조선소", "지역": "속초", "실내여부": "실내외", "평점": 4.4, "대표메뉴": "메이플 마롱 밀크"},
    {"이름": "감자밭", "지역": "춘천", "실내여부": "실내외", "평점": 4.5, "대표메뉴": "강원도 감자빵"},
    {"이름": "커피공장", "지역": "강릉", "실내여부": "실내외", "평점": 4.6, "대표메뉴": "핸드드립 커피"},
    {"이름": "갤러리밥스", "지역": "강릉", "실내여부": "실내", "평점": 4.5, "대표메뉴": "초옥이커피"}
]


def show_all_places(places):
    st.subheader("전체 장소 보기")
    for place in places:
        # 아래 빈칸을 완성하세요
        st.write("이름:",place["이름"])
        st.write("지역:", place["지역"])
        st.write("실내여부:", place["실내여부"])
        st.write("평점:", place["평점"])
        st.write("대표메뉴:", place["대표메뉴"])
        st.write("---")


def find_places(places, region, inout, point, menu):
    result = []
    for place in st.session_state.places:
        # 아래 조건문을 완성하세요
        if (place["지역"] == region and
            place["실내여부"] == inout and 
            place["평점"] >= point ):
            result.append(place)
    return result


def add_place(places, name, region, inout, point, menu):
    new_place = {
        "이름": name,
        "지역": region,
        "실내여부": inout,
        "평점": point,
        "대표메뉴": menu
    }
    st.session_state.places.append(new_place)


st.title("강원카페추천앱")

menu = st.selectbox("기능을 선택하세요", ["전체 보기", "추천 받기", "장소 추가"])

if menu == "전체 보기":
    show_all_places(st.session_state.places)

elif menu == "추천 받기":
    region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
    inout = st.selectbox("실내여부를 선택하세요", ["실내", "실내외"])
    point = st.number_input("평점을 입력하세요", min_value=0, step=1, value=5)

    result_places = find_places(st.session_state.places, region, inout, point, menu)

    st.subheader("추천 결과")

    # 아래 빈칸을 완성하세요
    if len(result_places) != 0:
        for place in result_places:
            st.write("이름:",place["이름"])
            st.write("지역:", place["지역"])
            st.write("실내여부:", place["실내여부"])
            st.write("평점:", place["평점"])
            st.write("대표메뉴:", place["대표메뉴"])
            st.write("---")
    else:
        st.write("조건에 맞는 장소가 없습니다")

elif menu == "장소 추가":
    name = st.text_input("이름을 입력하세요")
    region = st.selectbox("지역을 선택하세요", ["강릉", "속초", "춘천"])
    inout = st.selectbox("실내여부를 선택하세요", ["실내", "실내외"])
    point = st.number_input("평점을 입력하세요", min_value=0, step=5)
    menu = st.text_input("대표메뉴를 입력하세요")

    if st.button("장소 추가"):
        # 아래 함수 호출을 완성하세요
        add_place(st.session_state.places, name, region, inout, point, menu)
        st.success("새 장소가 추가되었습니다")
