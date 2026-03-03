import streamlit as st
import pandas as pd
from core.optimizer import HROptimizer
from utils.db import get_db
from utils.employee_repo import get_user_employees
from utils.column_mapper import ENG_TO_KOR


def render_optimization_page():
    st.title("💰 예산 대비 최적화 솔루션")
    st.markdown("한정된 예산으로 조직 전체의 퇴사율을 가장 크게 낮출 수 있는 **최적의 보상 배분안**을 AI가 제안합니다.")

    if 'user_id' not in st.session_state:
        st.warning("로그인이 필요합니다.")
        return
    
    user_id = st.session_state['user_id']
    
    conn = None
    try:
        conn = get_db()
        df = get_user_employees(conn, user_id)
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return
    
    if df.empty:
        st.info("등록된 직원 데이터가 없습니다. 먼저 직원 데이터를 등록해주세요.")
        return
    
    '''
    reverse_mapping = {
        "name": "이름", "age": "나이", "business_travel": "출장빈도", "department": "부서",
        "distance_from_home": "집과의거리", "education": "교육수준", "education_field": "전공분야",
        "environment_satisfaction": "근무환경만족도", "gender": "성별", "job_involvement": "직무몰입도",
        "job_level": "직급", "job_satisfaction": "직무만족도", "marital_status": "결혼상태",
        "monthly_income": "월급", "num_companies_worked": "이전회사근무횟수", "overtime": "초과근무여부",
        "percent_salary_hike": "급여인상률", "performance_rating": "성과평가등급",
        "relationship_satisfaction": "대인관계만족도", "total_working_years": "총경력년수",
        "work_life_balance": "워라밸수준", "years_at_company": "현회사근속년수",
        "years_in_current_role": "현재직무근무년수", "years_since_last_promotion": "마지막승진후경과년수",
        "job_role": "직무분류"
    }
    '''
    df = df.rename(columns=ENG_TO_KOR)

    st.subheader("1. 제약 조건 입력")

    with st.form("optimize_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.number_input("가용 연봉 인상 예산 (총합, 단위 임의설정)", min_value=0, value=10000, step=1000)
        with col2:
            max_promotions = st.number_input("최대 승진 가능 인원 (명)", min_value=0, value=5, step=1)
        with col3:
            max_no_overtime = st.number_input("야근 면제 가능 인원 (명)", min_value=0, value=30, step=1)
            
        # target_rate = st.slider("목표 조직 퇴사율 (%)", min_value=1, max_value=20, value=10) # 이 기능은 MVP 이후 고도화때 적용 권장
        
        submitted = st.form_submit_button("최적화 알고리즘 실행", type="primary")

    # 최적화 결과
    if submitted:
        st.divider()
        st.subheader("2. AI 최적화 제안")
        
        with st.spinner("AI가 수만 가지 경우의 수를 계산하여 최적의 보상안을 탐색 중입니다..."):
            optimizer = HROptimizer()
            result_df, total_drop, total_employees = optimizer.optimize(df, budget, max_promotions, max_no_overtime)
            
        if result_df.empty:
            st.info("현재 예산/조건에서 추천할 만한 효과적인 액션이 없거나, 고위험군 직원이 없습니다.")
        else:
            # 조직 전체 퇴사율 감소량 추정 (단순 평균 기준)
            avg_drop_rate = (total_drop / total_employees) * 100
            
            st.metric(
                label="조직 전체 평균 퇴사율 예상 변화", 
                value="개선됨", 
                delta=f"-{avg_drop_rate:.2f}%p 감소 효과", 
                delta_color="inverse"
            )
            
            st.write("#### 🎯 집중 관리 대상 및 추천 액션 (가성비 TOP)")
            #st.table(result_df)
            def highlight_after_risk(val):
                return 'color: #0056b3; font-weight: bold; background-color: #e6f2ff;'
            
            try:
                styled_df = result_df.style.map(highlight_after_risk, subset=['조치 후 예상 위험도'])
            except AttributeError:
                styled_df = result_df.style.applymap(highlight_after_risk, subset=['조치 후 예상 위험도'])

            # st.table 대신 st.dataframe을 사용하여 스타일이 적용된 표 출력 (인덱스 숨김 처리)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)