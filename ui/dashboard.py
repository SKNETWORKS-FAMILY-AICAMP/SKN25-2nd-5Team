import streamlit as st
import pandas as pd
from core.predictor import AttritionPredictor
import numpy as np
import shap
import plotly.express as px

from utils.db import get_db
from utils.employee_repo import get_user_employees

@st.cache_data(show_spinner=False)
def get_predicted_data(df):
    predictor = AttritionPredictor()
    df_copy = df.copy()
    df_copy['예측_퇴사확률'] = predictor.predict_dataframe(df_copy)
    df_copy['위험군'] = df_copy['예측_퇴사확률'].apply(lambda x: '고위험' if x > 0.7 else '안정')
    return df_copy

@st.cache_data(show_spinner=False)
def get_shap_data(df):
    predictor = AttritionPredictor()
    return predictor.get_global_shap(df)

def render_dashboard():
    st.title("📊 HR Analytics Dashboard")
    st.markdown("회사 전체의  인사 데이터와 AI 기반 퇴사 위험 현황을 한눈에 파악하세요.")
    st.divider()

    if 'user_id' not in st.session_state:
        st.warning("로그인이 필요합니다. 먼저 로그인을 해주세요.")
        return
    
    user_id = st.session_state['user_id']

    try:
        conn = get_db()
        df = get_user_employees(conn, user_id)
    except Exception as e:
        st.error(f"데이터베이스 연결 또는 데이터 로드 중 오류 발생: {e}")
        return
    
    if df.empty:
        st.info("현재 등록된 직원 데이터가 없습니다. Prediction 페이지에서 데이터를 업로드 해주세요.")
        return
    
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

    df = df.rename(columns=reverse_mapping)

    with st.spinner("AI가 전체 임직원의 퇴사 위험도를 분석하고 있습니다..."):
        df = get_predicted_data(df)
            
    #kpi 지표 계산
    total_emp = len(df)
    high_risk_emp = len(df[df['위험군'] == '고위험'])
    predicted_attrition_rate = (high_risk_emp / total_emp * 100) if total_emp > 0 else 0

    avg_tenure_col = '현회사근속년수' if '현회사근속년수' in df.columns else ('YearsAtCompany' if 'YearsAtCompany' in df.columns else ('years_at_company' if 'years_at_company' in df.columns else None))
    avg_income_col = '월급' if '월급' in df.columns else ('MonthlyIncome' if 'MonthlyIncome' in df.columns else ('monthly_income' if 'monthly_income' in df.columns else None))

    avg_tenure = df[avg_tenure_col].mean() if avg_tenure_col else 0
    avg_income = df[avg_income_col].mean() if avg_income_col else 0


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="총 임직원 수", value=f"{total_emp:,} 명")
    with col2:
        st.metric(label="AI 예상 퇴사율", value=f"{predicted_attrition_rate:.1f} %", delta=f"{high_risk_emp}명 위험", delta_color="inverse")
    with col3:
        st.metric(label="평균 근속 연수", value=f"{avg_tenure:.1f} 년" if avg_tenure else "N/A")
    with col4:
        st.metric(label="평균 월급", value=f"$ {avg_income:,.0f}" if avg_income else "N/A")

    st.markdown("---")

    # 차트 
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("부서별 예상 퇴사율")
        dept_col = '부서' if '부서' in df.columns else ('Department' if 'Department' in df.columns else None)
        
        if dept_col:
            # 부서별 고위험군 비율 계산
            dept_risk = df.groupby(dept_col)['예측_퇴사확률'].mean() * 100
            fig_dept = px.bar(
                dept_risk.reset_index(), 
                x=dept_col, 
                y='예측_퇴사확률',
                labels={'예측_퇴사확률': '예상 퇴사율 (%)'},
                color='예측_퇴사확률',
                color_continuous_scale='Blues'
            )
            fig_dept.update_layout(showlegend=False)
            st.plotly_chart(fig_dept, use_container_width=True)
        else:
            st.info("데이터에 '부서' 관련 컬럼이 없어 차트를 표시할 수 없습니다.")

    with col_chart2:
        st.subheader("퇴사 주요 원인 분석(Global SHAP)")

        with st.spinner("SHAP 분석 중..."):
            try:
                df_for_shap = df.drop(columns=['예측_퇴사확률', '위험군'], errors='ignore')
                shap_df = get_shap_data(df_for_shap)
                
                fig = px.bar(
                    shap_df, 
                    x='중요도 (Impact)', 
                    y='요인 (Feature)', 
                    orientation='h',
                    color='중요도 (Impact)', 
                    color_continuous_scale='Reds', 
                    text_auto='.3f' # 바 옆에 수치 표시
                )
                fig.update_layout(
                    xaxis_title="퇴사 확률에 미치는 영향력",
                    yaxis_title=None,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=30, b=0)
                )

                

                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"SHAP 분석 중 오류가 발생했습니다: {e}")

        
