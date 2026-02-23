import streamlit as st
import pandas as pd
import os

from utils.data_loader import validate_uploaded_data
from utils.db import get_db
from utils.employee_repo import insert_employee, get_user_employees


def render_prediction_page():

    st.title("🎯 퇴사 위험 예측 및 분석")
    st.markdown("직원 데이터를 업로드하고 AI가 예측한 퇴사 위험도를 확인하세요.")

  
    # 1️. CSV 데이터 업로드 
 
    st.subheader("1. 데이터 업로드")

    uploaded_file = st.file_uploader("인사 데이터 (CSV) 파일을 업로드하세요", type=['csv'])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

        column_mapping = {
            "이름": "name",
            "나이": "age",
            "출장빈도": "business_travel",
            "부서": "department",
            "집과의거리": "distance_from_home",
            "교육수준": "education",
            "전공분야": "education_field",
            "근무환경만족도": "environment_satisfaction",
            "성별": "gender",
            "직무몰입도": "job_involvement",
            "직급": "job_level",
            "직무만족도": "job_satisfaction",
            "결혼상태": "marital_status",
            "월급": "monthly_income",
            "이전회사근무횟수": "num_companies_worked",
            "초과근무여부": "overtime",
            "급여인상률": "percent_salary_hike",
            "성과평가등급": "performance_rating",
            "대인관계만족도": "relationship_satisfaction",
            "총경력년수": "total_working_years",
            "워라밸수준": "work_life_balance",
            "현회사근속년수": "years_at_company",
            "현재직무근무년수": "years_in_current_role",
            "마지막승진후경과년수": "years_since_last_promotion",
            "직무분류": "job_role"
        }

        df.rename(columns=column_mapping, inplace=True)

        is_valid, message = validate_uploaded_data(df)

        if is_valid:

            conn = get_db()

            # 로그인 연결 시 사용
            user_id = st.session_state.get("user_id")

            # 테스트용
            # user_id = 1  

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


    # 2️. DB 기반 예측

    st.subheader("2. 개별 직원 퇴사 위험 분석 (SHAP)")

    conn = get_db()

    #  나중에 로그인 연결 시
    user_id = st.session_state.get("user_id")

    # 테스트용
    #user_id = 1

    df = get_user_employees(conn, user_id)

    if df.empty:
        st.warning("등록된 직원이 없습니다.")
        return

    selected_emp = st.selectbox("분석할 직원 선택", df["name"])

    if st.button("AI 분석 실행", type="primary"):

        selected_row = df[df["name"] == selected_emp]

        from core.predictor import AttritionPredictor
        predictor = AttritionPredictor()

        with st.spinner("AI가 데이터를 분석하고 있습니다..."):
            prob = predictor.predict_single(selected_row)

        if prob is not None:

            if prob > 0.4:
                st.metric(
                    label="AI 예측 퇴사 확률",
                    value=f"{prob * 100:.1f} %",
                    delta="🚨 퇴사 고위험군 (주의)",
                    delta_color="inverse"
                )
                st.error("이 직원은 퇴사할 확률이 높습니다. 원인 분석 및 면담이 필요합니다.")

            else:
                st.metric(
                    label="AI 예측 퇴사 확률",
                    value=f"{prob * 100:.1f} %",
                    delta="✅ 안정적",
                    delta_color="normal"
                )
                st.success("안정적인 상태입니다.")
                st.info("💡 여기에 SHAP 그래프가 들어갈 자리입니다.")

        else:
            st.error("🚨 모델 파일을 찾을 수 없거나 에러가 발생했습니다.")