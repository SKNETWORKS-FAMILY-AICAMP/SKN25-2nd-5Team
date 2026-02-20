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
            st.download_button(
                label="📄 샘플 인사데이터 양식 다운로드",
                data=file,
                file_name="HR_sample_template.csv",
                mime="text/csv"
            )


    # 1. 파일 업로드 영역
    st.subheader("1. 데이터 업로드")
    uploaded_file = st.file_uploader("인사 데이터 (CSV) 파일을 업로드하세요", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

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
        
        # 임시로 사번(EmployeeNumber) 리스트를 만든다고 가정 (실제 데이터에 맞게 수정 필요)
        if 'EmpID' in df.columns:
            emp_list = df['EmpID'].tolist()
        else:
            emp_list = df.index.tolist()

        selected_emp = st.selectbox("분석할 직원을 선택하세요 (사번)", emp_list)
        
        if st.button("AI 분석 실행", type="primary"):
            st.markdown(f"**직원 {selected_emp} 분석 결과**")
            
            # TODO: core.predictor에서 예측값 가져오기
            st.warning("⚠️ 여기에 AI 모델이 예측한 퇴사 확률 (예: 85%) 이 메트릭으로 뜹니다.")
            
            # TODO: core.explainer에서 SHAP 워터폴 차트 가져오기
            st.info("💡 여기에 SHAP Waterfall 차트가 뜹니다. (예: 야근 때문에 +20%, 월급이 낮아서 +10% 등 원인 설명)")