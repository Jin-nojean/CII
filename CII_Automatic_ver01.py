import streamlit as st
import pandas as pd
from supabase import create_client

url = "https://ocoxpucmzmhkjuzclpfd.supabase.co"

# 개발자 수정 시  service_role 키로 변경
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jb3hwdWNtem1oa2p1emNscGZkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDk3NzIzMCwiZXhwIjoyMDY2NTUzMjMwfQ.RLObk3wkecXeiuOZCoiCkW1jIsHn8or5pHBh6XinKnU"

# Streamlit 배포 전환 시 anon 키로 변경
#key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jb3hwdWNtem1oa2p1emNscGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5NzcyMzAsImV4cCI6MjA2NjU1MzIzMH0.bSD1xe1Fc8Vbo6DfHEQ6kieR5hVFXaEmCuf8aKfZRx0"
supabase = create_client(url, key)

# 페이지 설정
st.set_page_config(page_title="CII 자동화 시스템", layout="wide")

# 사이드바 메뉴
menu = st.sidebar.selectbox("📌 메뉴를 선택하세요", ["개요", "데이터 업로드"])

# ----------------------------------
# 1️⃣ 개요 화면
# ----------------------------------
if menu == "개요":
    st.title("📊 CII 자동화 개요")
    st.markdown("""
    이 시스템은 다음 데이터를 기반으로 CII 등급을 자동 계산 및 예측합니다:

    - 🚢 `ships`: 선박 기본 정보  
    - 📅 `fuel_consumption_monthly`: 월별 연료 사용량  
    - 🛢️ `fuel_consumption_noon`: 노운 리포트 연료 사용량  
    - ⚙️ `ship_speed_consumptions`: 속도별 FOC 데이터  
    - 📈 `cii_info`: CII 등급 기록 및 요구 기준  
    - 📐 `cii_reference_values`: 선종별 기준 벡터값 (a, c, d1~d4 등)

    ---  

    사이드 메뉴에서 `데이터 업로드`를 통해 엑셀 파일을 업로드할 수 있습니다.
    """)

# ----------------------------------
# 2️⃣ 데이터 업로드 화면
# ----------------------------------
elif menu == "데이터 업로드":
    st.title("📤 데이터 업로드")

    uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요 (시트: 'monthly', 'ships')", type=["xlsx"])

    if uploaded_file:
        try:
            xls = pd.read_excel(uploaded_file, sheet_name=None)
            st.success(f"✅ {len(xls)}개 시트 불러옴: {list(xls.keys())}")

            if "monthly" in xls:
                st.subheader("📅 월별 연료 사용량 미리보기")
                st.dataframe(xls["monthly"].head())

            if "ships" in xls:
                st.subheader("🚢 선박 정보 미리보기")
                st.dataframe(xls["ships"].head())

        except Exception as e:
            st.error(f"❌ 엑셀 처리 중 오류: {e}")