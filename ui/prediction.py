import streamlit as st
import pandas as pd
import os
from utils.data_loader import validate_uploaded_data

def render_prediction_page():
    st.title("🎯 퇴사 위험 예측 및 분석")
    st.markdown("직원 데이터를 업로드하고 AI가 예측한 퇴사 위험도를 확인하세요.")

    #  샘플 데이터 다운로드 버튼
    sample_file_path = r"C:\Users\playdata2\Downloads\archive\HR_Analytics.csv" # 
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "rb") as file:
            csv_data = file.read()
            st.download_button(
                label="📄 샘플 인사데이터 양식 다운로드",
                data=csv_data,
                file_name="HR_sample_template.csv",
                mime="text/csv"
            )


    # 1. 파일 업로드 영역
    st.subheader("1. 데이터 업로드")
    uploaded_file = st.file_uploader("인사 데이터 (CSV) 파일을 업로드하세요", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"파일을 읽는 중 오류 발생:{e}")
            #df = None

        is_vaild, message = validate_uploaded_data(df)

        if is_vaild:
            st.session_state['employee_data'] = df
            st.success("✅ " + message)
        
            with st.expander("데이터 미리보기"):
                st.dataframe(df.head())
        else:
            st.error("❌ " + message)
    else:
        st.info("먼저 데이터를 업로드해주세요. (예: HR_Analytics.csv)")

    st.divider()

    # 2. 개별 예측 및 SHAP 분석 영역
    st.subheader("2. 개별 직원 퇴사 위험 분석 (SHAP)")
    if 'employee_data' in st.session_state:
        df = st.session_state['employee_data']
        
        # 사번 선택 박스 로직
        emp_list = df.index.tolist()
        selected_emp_idx = st.selectbox("분석할 직원을 선택하세요(데이터 행 번호)",emp_list)

        if st.button("AI 분석 실행", type="primary"):
            st.markdown(f"**선택된 직원(Index: {selected_emp_idx}) 분석 결과**")

            from core.predictor import AttritionPredictor
            predictor = AttritionPredictor()

            emp_row = df.loc[[selected_emp_idx]]

            with st.spinner("AI가 데이터를 분석하고 있습니다..."):
                prob = predictor.predict_single(emp_row)

            if prob is not None:
                if prob > 0.4:
                    st.metric(label="AI 예측 퇴사 확률", value=f"{prob * 100:.1f} %", delta="🚨 퇴사 고위험군 (주의)", delta_color="inverse")
                    st.error("이 직원은 퇴사할 확률이 높습니다. 원인 분석 및 면담이 필요합니다.")
                else:
                    st.metric(label="AI 예측 퇴사 확률", value=f"{prob * 100:.1f} %", delta="✅ 안정적", delta_color="normal")
                    st.success("안정적인 상태입니다.")

                    st.info("💡 [다음 스텝] 여기에 이 직원이 '왜' 이런 확률이 나왔는지 이유를 설명하는 SHAP 그래프가 들어갈 자리입니다.")
            else:
                st.error("🚨 모델 파일을 찾을 수 없거나 에러가 발생했습니다.")
