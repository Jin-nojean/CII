import streamlit as st
import requests
import pandas as pd


# ============================================================
# Page Config
# ============================================================
st.set_page_config(
    page_title="Supabase Insert 테스트",
    page_icon="🚢",
    layout="wide"
)


# ============================================================
# Supabase 설정
# ============================================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


# ============================================================
# Supabase 조회 함수
# ============================================================
def load_ships():
    url = f"{SUPABASE_URL}/rest/v1/ships?select=*&order=id.asc"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        st.error("Supabase 조회 실패")
        st.write("Status Code:", response.status_code)
        st.write("Response:", response.text)
        return []

    except requests.exceptions.RequestException as e:
        st.error("Supabase 연결 중 오류가 발생했습니다.")
        st.write(e)
        return []


# ============================================================
# Supabase Insert 함수
# ============================================================
def insert_ship(ship_name, ship_type, dwt, gt):
    url = f"{SUPABASE_URL}/rest/v1/ships"

    payload = {
        "ship_name": ship_name,
        "ship_type": ship_type,
        "dwt": dwt,
        "gt": gt,
    }

    try:
        response = requests.post(
            url,
            headers={
                **HEADERS,
                "Prefer": "return=representation"
            },
            json=payload,
            timeout=10
        )

        return response

    except requests.exceptions.RequestException as e:
        st.error("Supabase 저장 중 오류가 발생했습니다.")
        st.write(e)
        return None


# ============================================================
# 화면 구성
# ============================================================
st.title("🚢 Supabase Insert 테스트")
st.caption("Streamlit에서 입력한 선박 정보를 Supabase ships 테이블에 저장하는 테스트입니다.")

st.divider()


# ============================================================
# 입력 영역
# ============================================================
st.subheader("선박 정보 입력")

with st.form("ship_insert_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        ship_name = st.text_input(
            "선박명",
            placeholder="예: GLOVIS TEST"
        )

        ship_type = st.selectbox(
            "선종",
            ["PCTC", "Bulk", "Tanker", "Container", "LNGC", "Other"]
        )

    with col2:
        dwt = st.number_input(
            "DWT",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

        gt = st.number_input(
            "GT",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

    submitted = st.form_submit_button("Supabase에 저장")


if submitted:
    if not ship_name.strip():
        st.warning("선박명을 입력해주세요.")
    else:
        response = insert_ship(
            ship_name=ship_name.strip(),
            ship_type=ship_type,
            dwt=dwt,
            gt=gt
        )

        if response is not None:
            if response.status_code in [200, 201]:
                st.success("Supabase에 선박 정보가 저장되었습니다.")
                st.write(response.json())
            else:
                st.error("Supabase 저장 실패")
                st.write("Status Code:", response.status_code)
                st.write("Response:", response.text)


st.divider()


# ============================================================
# 조회 영역
# ============================================================
st.subheader("Supabase 저장 데이터")

ships_data = load_ships()

if ships_data:
    df = pd.DataFrame(ships_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("요약")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("등록 선박 수", len(df))

    with col2:
        st.metric("선종 수", df["ship_type"].nunique())

    with col3:
        st.metric("총 DWT", f"{df['dwt'].sum():,.0f}")

    with col4:
        st.metric("총 GT", f"{df['gt'].sum():,.0f}")

else:
    st.info("아직 저장된 선박 데이터가 없습니다.")