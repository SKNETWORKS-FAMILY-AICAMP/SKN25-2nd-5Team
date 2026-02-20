import streamlit as st
import pandas as pd
from core.predictor import AttritionPredictor
#from core.explainer import ShapExplainer

def render_simulation_page():
    st.title("🕹️ 맞춤형 리텐션 시뮬레이션 (What-If)")
    st.header("What-If 시뮬레이션")
    st.markdown("특정 직원의 조건을 변경하여 퇴사 확률 변화를 예측합니다")

    # 1. 대상 직원 선택
    if 'employee_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드 해주세요")
        return
    
    df = st.session_state['employee_data']
    emp_list = df['EmpID'].tolist() if 'EmpID' in df.columns else df.index.tolist()

    col_emp, col_blank = st.columns([1, 2])
    with col_emp:
        selected_emp = st.selectbox("시뮬레이션 대상 직원", emp_list)
    
    # 현재 상태 (가짜 데이터)
    st.subheader("현재 상태")
    st.metric(label="현재 예측된 퇴사 확률", value="75 %", help="AI가 예측한 현재 상태의 퇴사 확률입니다.")
    
    st.divider()

    # 시뮬레이션 조건 입력
    st.subheader("조건 변경 시뮬레이션")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        salary_hike = st.slider("연봉 인상률 (%)", min_value=0, max_value=30, value=0, step=1)
    with col2:
        promote = st.toggle("승진 시키기 (직급 +1)")
    with col3:
        remove_overtime = st.toggle("야근 면제 (OverTime = No)")
        
    if st.button("시뮬레이션 실행", type="primary"):
        # TODO: core.predictor 에 변경된 데이터를 넣고 확률 다시 계산하기
        with st.spinner("AI가 새로운 확률을 계산 중입니다..."):
            # 가짜 결과
            st.success("시뮬레이션 완료!")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric(label="시뮬레이션 후 퇴사 확률", value="42 %", delta="-33%p 감소", delta_color="inverse")
            with res_col2:
                st.write("#### 주요 변화 요인")
                st.write(f"- 연봉 {salary_hike}% 인상 적용됨")
                if promote: st.write("- 승진 적용됨")
                if remove_overtime: st.write("- 워라밸 개선(야근 면제) 적용됨")
    