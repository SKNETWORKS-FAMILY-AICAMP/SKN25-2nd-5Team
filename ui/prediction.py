import streamlit as st
import pandas as pd
import os
import shap
import plotly.express as px

from utils.data_loader import validate_uploaded_data
from utils.db import get_db
from utils.employee_repo import insert_employee, get_user_employees
from utils.column_mapper import KOR_TO_ENG, ENG_TO_KOR


def render_prediction_page():

    st.title("🎯 퇴사 위험 예측 및 분석")
    st.markdown("직원 데이터를 업로드하고 AI가 예측한 퇴사 위험도를 확인하세요.")

  
    # 1️. CSV 데이터 업로드 
    st.subheader("1. 데이터 업로드")
    uploaded_file = st.file_uploader("인사 데이터 (CSV) 파일을 업로드하세요", type=['csv'])

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"파일을 읽는 중 오류 발생:{e}")
            df = None

        df = df.rename(columns=KOR_TO_ENG)

        is_valid, message = validate_uploaded_data(df)

        if is_valid:

            conn = get_db()

            # 로그인 연결
            user_id = st.session_state.get("user_id")

            for _, row in df.iterrows():

                values = (
                    user_id,
                    row["name"],
                    row["age"],
                    row["business_travel"],
                    row["department"],
                    row["distance_from_home"],
                    row["education"],
                    row["education_field"],
                    row["environment_satisfaction"],
                    row["gender"],
                    row["job_involvement"],
                    row["job_level"],
                    row["job_satisfaction"],
                    row["marital_status"],
                    row["monthly_income"],
                    row["num_companies_worked"],
                    row["overtime"],
                    row["percent_salary_hike"],
                    row["performance_rating"],
                    row["relationship_satisfaction"],
                    row["total_working_years"],
                    row["work_life_balance"],
                    row["years_at_company"],
                    row["years_in_current_role"],
                    row["years_since_last_promotion"],
                    row["job_role"],
                )

                insert_employee(conn, values)

            st.success("✅ 데이터가 저장되었습니다.")

        else:
            st.error("❌ " + message)

    st.divider()


 
    # 2️. 개별 직원 예측 
    st.subheader("2. 개별 직원 퇴사 위험 분석")

    conn = get_db()
    user_id = st.session_state.get("user_id")

    df = get_user_employees(conn, user_id)

    if df.empty:
        st.warning("등록된 직원이 없습니다.")
        return

    selected_emp = st.selectbox("분석할 직원 선택", df["name"])

    if st.button("AI 분석 실행", type="primary"):

        # 1행만 가져오기
        selected_row = df[df["name"] == selected_emp]

        if selected_row.empty:
            st.error("선택된 직원 데이터를 찾을 수 없습니다.")
            return

        selected_row = selected_row.iloc[[0]]

        # 영어 → 한국어 
        selected_row = selected_row.rename(columns=ENG_TO_KOR)

        from core.predictor import AttritionPredictor
        predictor = AttritionPredictor()

        with st.spinner("AI가 데이터를 분석하고 있습니다..."):

            # 예측
            prob = predictor.predict_single(selected_row)

            if prob is None:
                st.error("모델 예측 중 오류 발생")
                return
            
            shap_df = predictor.get_shap_values(selected_row)
    
        # 결과 출력
        st.metric(
            label="AI 예측 퇴사 확률",
            value=f"{prob * 100:.1f} %",
            delta="🚨 고위험" if prob > 0.4 else "✅ 안정",
            delta_color="inverse" if prob > 0.4 else "normal"
        )

        st.subheader("🔍 퇴사 원인 분석 (SHAP)")

        fig = px.bar(
            shap_df,
            x='SHAP Value',
            y='Feature',
            orientation='h',
            color='SHAP Value',
            color_continuous_scale='RdBu',
            text_auto='.3f'
        )

        fig.update_layout(
            xaxis_title="퇴사 확률에 미치는 영향 (양수=위험 증가, 음수=위험 감소)",
            yaxis_title=None,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)