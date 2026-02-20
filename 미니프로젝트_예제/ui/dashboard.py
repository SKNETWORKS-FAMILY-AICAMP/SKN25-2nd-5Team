import streamlit as st
import pandas as pd
import numpy as np

def render_dashboard():
    st.title("📊 HR Analytics Dashboard")
    st.markdown("회사 전체의 인사 데이터와 퇴사 현황을 한눈에 파악하세요.")

    st.divider()

    # 상단 KPI 지표 임시 가짜 데이터
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="총 임직원 수", value="1,470 명", delta="12명 증가")
    with col2:
        st.metric(label="현재 퇴사율", value="16.1 %", delta="-1.2%p 감소", delta_color="inverse")
    with col3:
        st.metric(label="평균 근속 연수", value="7.0 년")
    with col4:
        st.metric(label="평균 월급", value="$ 6,502")

    st.markdown("---")

    # 차트 영역 (빈 껍데기)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("부서별 퇴사율 (예시)")
        # 나중에 실제 데이터 기반 st.bar_chart() 나 plotly 차트로 교체할 자리
        dummy_data1 = pd.DataFrame({
            "부서": ["R&D", "Sales", "HR"],
            "퇴사율(%)": [13.8, 20.6, 19.0]
        }).set_index("부서")
        st.bar_chart(dummy_data1)

    with col_chart2:
        st.subheader("퇴사자 주요 특징 (예시)")
        st.info("💡 나중에 여기에 모델의 Global SHAP (전체 특성 중요도) 그래프가 들어갈 자리입니다. 어떤 요인이 퇴사에 가장 큰 영향을 미치는지 보여줍니다.")
        # 예시 텍스트
        st.write("1. 야근 (OverTime) 여부")
        st.write("2. 월 급여 (Monthly Income)")
        st.write("3. 총 경력 연수 (Total Working Years)")