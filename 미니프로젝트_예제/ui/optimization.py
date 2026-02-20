import streamlit as st

def render_optimization_page():
    st.title("💰 예산 대비 최적화 솔루션")
    st.markdown("한정된 예산으로 조직 전체의 퇴사율을 가장 크게 낮출 수 있는 **최적의 보상 배분안**을 AI가 제안합니다.")

    if 'employee_data' not in st.session_state:
        st.warning("Prediction 페이지에서 먼저 데이터를 업로드해주세요.")
        return

    # 제약 조건 설정
    st.subheader("1. 제약 조건 입력")
    
    with st.form("optimize_form"):
        col1, col2 = st.columns(2)
        with col1:
            budget = st.number_input("가용 연봉 인상 예산 (총합, 만원 단위)", min_value=0, value=10000, step=1000)
        with col2:
            max_promotions = st.number_input("최대 승진 가능 인원 (명)", min_value=0, value=5, step=1)
            
        target_rate = st.slider("목표 조직 퇴사율 (%)", min_value=1, max_value=20, value=10)
        
        submitted = st.form_submit_button("최적화 알고리즘 실행")

    # 최적화 결과
    if submitted:
        st.divider()
        st.subheader("2. AI 최적화 제안")
        
        # TODO: core.optimizer 호출하여 결과 받아오기
        st.info("진행 중... (실제 로직 연결 전)")
        
        # 가짜 결과 보여주기
        st.metric("예상 조직 퇴사율 변화", value="9.8 %", delta="-6.3%p", delta_color="inverse")
        
        st.write("#### 🎯 집중 관리 대상 및 추천 액션 (가성비 TOP 5)")
        # 표 데이터 가짜로 생성
        result_data = {
            "사번": ["RM102", "RM341", "RM005", "RM899", "RM210"],
            "현재 위험도": ["88%", "82%", "79%", "75%", "70%"],
            "추천 액션": ["연봉 8% 인상", "승진", "야근 면제 + 연봉 3% 인상", "승진", "연봉 10% 인상"],
            "투입 비용(예상)": ["400만원", "0원", "150만원", "0원", "500만원"],
            "조치 후 예상 위험도": ["20%", "30%", "25%", "40%", "15%"]
        }
        st.table(result_data)