import streamlit as st
import pandas as pd
import os
import shap
import plotly.express as px

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

        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"파일을 읽는 중 오류 발생:{e}")
            df = None

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

        # 영어 → 한국어 (모델이 한국어 기준이므로 필요)
        reverse_mapping = {
            "name": "이름",
            "age": "나이",
            "business_travel": "출장빈도",
            "department": "부서",
            "distance_from_home": "집과의거리",
            "education": "교육수준",
            "education_field": "전공분야",
            "environment_satisfaction": "근무환경만족도",
            "gender": "성별",
            "job_involvement": "직무몰입도",
            "job_level": "직급",
            "job_satisfaction": "직무만족도",
            "marital_status": "결혼상태",
            "monthly_income": "월급",
            "num_companies_worked": "이전회사근무횟수",
            "overtime": "초과근무여부",
            "percent_salary_hike": "급여인상률",
            "performance_rating": "성과평가등급",
            "relationship_satisfaction": "대인관계만족도",
            "total_working_years": "총경력년수",
            "work_life_balance": "워라밸수준",
            "years_at_company": "현회사근속년수",
            "years_in_current_role": "현재직무근무년수",
            "years_since_last_promotion": "마지막승진후경과년수",
            "job_role": "직무분류"
        }

        selected_row = selected_row.rename(columns=reverse_mapping)

        from core.predictor import AttritionPredictor
        predictor = AttritionPredictor()

        with st.spinner("AI가 데이터를 분석하고 있습니다..."):

            # 예측
            prob = predictor.predict_single(selected_row)

            if prob is None:
                st.error("모델 예측 중 오류 발생")
                return

            # SHAP 계산용 (predictor 내부와 동일 처리)
            df_processed = selected_row.copy()

            if '퇴사여부' in df_processed.columns:
                df_processed = df_processed.drop('퇴사여부', axis=1)

            if '초과근무여부' in df_processed.columns:
                df_processed['초과근무여부'] = df_processed['초과근무여부'].map({'Yes': 1, 'No': 0})

            if '성별' in df_processed.columns:
                df_processed['성별'] = df_processed['성별'].map({'Male': 1, 'Female': 0})

            df_processed = pd.get_dummies(df_processed)

            final_features = pd.DataFrame(columns=predictor.feature_name)

            for col in predictor.feature_name:
                if col in df_processed.columns:
                    final_features[col] = df_processed[col].values
                else:
                    final_features[col] = 0

            explainer = shap.TreeExplainer(predictor.model)
            shap_values = explainer.shap_values(final_features)

            if isinstance(shap_values, list):
                shap_values = shap_values[1]

            person_shap = shap_values[0]

            shap_df = pd.DataFrame({
                'Feature': final_features.columns,
                'SHAP Value': person_shap
            }).sort_values(by='SHAP Value', key=abs, ascending=True).tail(10)

    
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