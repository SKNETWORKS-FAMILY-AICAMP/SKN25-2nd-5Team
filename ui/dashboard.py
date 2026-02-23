import streamlit as st
import pandas as pd
from core.predictor import AttritionPredictor
import numpy as np
import shap
import matplotlib.pyplot as plt
import plotly.express as px


def render_dashboard():
    st.title("📊 HR Analytics Dashboard")
    st.markdown("회사 전체의  인사 데이터와 AI 기반 퇴사 위험 현황을 한눈에 파악하세요.")

    st.divider()

    if 'employee_data' not in st.session_state:
        st.warning("데이터가 로드되지 않았습니다. 데이터를 먼저 업로드 해 주세요")
        return
    
    df = st.session_state['employee_data'].copy()
    predictor = AttritionPredictor()

    if '예측_퇴사확률' not in df.columns:
        with st.spinner("AI가 전체 임직원의 퇴사 위험도를 분석하고 있습니다..."):
            probs = []
            for i in range(len(df)):
                prob = predictor.predict_single(df.iloc[[i]])
                probs.append(prob if prob is not None else 0.0)

            df['예측_퇴사확률'] = probs
            df['위험군'] = df['예측_퇴사확률'].apply(lambda x: '고위험' if x> 0.4 else '안정')
            st.session_state['employee_data'] = df 
    #kpi 지표 계산
    total_emp = len(df)
    high_risk_emp = len(df[df['위험군'] == '고위험'])
    predicted_attrition_rate = (high_risk_emp / total_emp * 100) if total_emp > 0 else 0

    avg_tenure = df['현회사근속년수'].mean() if '현회사근속년수' in df.columns else (df['YearsAtCompany'].mean() if 'YearsAtCompany' in df.columns else 0)
    avg_income = df['월급'].mean() if '월급' in df.columns else (df['MonthlyIncome'].mean() if 'MonthlyIncome' in df.columns else 0)

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

        if 'shap_fig' not in st.session_state:
            with st.spinner("전체 데이터 SHAP 요인 분석 중..."):
                try:
                    df_processed = df.copy()
                    if '퇴사여부' in df_processed.columns:
                        df_processed = df_processed.drop('퇴사여부', axis=1)
                    if '초과근무여부' in df_processed.columns:
                        df_processed['초과근무여부'] = df_processed['초과근무여부'].map({'Yes': 1, 'No': 0})
                    if '성별' in df_processed.columns:
                        df_processed['성별'] = df_processed['성별'].map({'Male': 1, 'Female': 0})
                    df_processed = pd.get_dummies(df_processed)

                    final_features = pd.DataFrame(columns=predictor.feature_name)
                    for col in predictor.feature_name:
                        final_features[col] = df_processed[col].values
                    else:
                        final_features[col] = 0
                    
                    explainer = shap.TreeExplainer(predictor.model)
                    shap_values = explainer.shap_values(final_features)

                    if isinstance(shap_values, list):
                        shap_values = shap_values[1]
                    mean_abs_shap = np.abs(shap_values).mean(axis=0)

                    shap_df = pd.DataFrame({
                        '요인 (Feature)': final_features.columns,
                        '중요도 (Impact)': mean_abs_shap
                    }).sort_values(by='중요도 (Impact)', ascending=True).tail(10) 

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

                    st.session_state['shap_plotly_fig'] = fig
                except Exception as e:
                    st.error(f"SHAP 분석 중 오류가 발생했습니다: {e}")

        if 'shap_plotly_fig' in st.session_state:
            st.plotly_chart(st.session_state['shap_plotly_fig'], use_container_width=True)
