import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_infra_page(conn=None):

    st.title("🏋️‍♂️ 회원 피트니스 데이터 분석 현황")
    st.markdown("### 📊 Gym Members Exercise Dataset Analysis")
    

    @st.cache_data
    def load_mock_data():
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'Age': np.random.randint(18, 65, n_samples),
            'Gender': np.random.choice(['Male', 'Female'], n_samples, p=[0.55, 0.45]),
            'Weight (kg)': np.random.normal(75, 15, n_samples).round(1),
            'Height (m)': np.random.normal(1.75, 0.1, n_samples).round(2),
            'Max_BPM': np.random.randint(160, 200, n_samples),
            'Avg_BPM': np.random.randint(120, 160, n_samples),
            'Resting_BPM': np.random.randint(50, 80, n_samples),
            'Session_Duration (hours)': np.random.uniform(0.5, 2.5, n_samples).round(1),
            'Workout_Frequency (days/week)': np.random.randint(1, 6, n_samples),
            'Fat_Percentage': np.random.uniform(10, 35, n_samples).round(1),
            'Water_Intake (liters)': np.random.uniform(1.5, 4.0, n_samples).round(1),
            'Workout_Type': np.random.choice(['Cardio', 'Strength', 'Yoga', 'HIIT'], n_samples),
            'Experience_Level': np.random.choice([1, 2, 3], n_samples) # 1:Beginner, 2:Intermediate, 3:Expert
        }
        
        df = pd.DataFrame(data)
        # 파생 변수 생성: BMI, Calories_Burned (상관관계가 있도록 수식 유도)
        df['BMI'] = (df['Weight (kg)'] / (df['Height (m)'] ** 2)).round(1)
        df['Calories_Burned'] = (
            df['Session_Duration (hours)'] * 400 + 
            (df['Avg_BPM'] - 100) * 5 + 
            np.random.normal(0, 50, n_samples)
        ).astype(int)
        
        return df

    df = load_mock_data()

    # -----------------------------------------------------------
    # 2. KPI 메트릭 섹션 (상단 요약)
    # -----------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 분석 회원 수", f"{len(df):,}명", "New +12")
    with col2:
        st.metric("평균 운동 시간", f"{df['Session_Duration (hours)'].mean():.1f} 시간", "+0.2h")
    with col3:
        st.metric("평균 소모 칼로리", f"{df['Calories_Burned'].mean():.0f} kcal", "▲ 150 kcal")
    with col4:
        st.metric("평균 BMI 지수", f"{df['BMI'].mean():.1f}", "-0.4")

    st.markdown("---")

    # -----------------------------------------------------------
    # 3. 그래프 시각화 섹션
    # -----------------------------------------------------------
    
    # [Row 1] 운동 유형별 분포 & BMI 분포
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🏃‍♂️ 운동 유형 선호도")
        fig_pie = px.pie(df, names='Workout_Type', values='Calories_Burned', 
                         hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(showlegend=True, height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("Workout Type Distribution based on Calorie Burn")

    with c2:
        st.subheader("📊 BMI(체질량지수) 분포")
        fig_hist = px.histogram(df, x="BMI", nbins=30, color="Gender",
                                marginal="box", # 상단에 박스플롯 추가
                                color_discrete_map={"Male": "#636EFA", "Female": "#EF553B"},
                                opacity=0.7)
        fig_hist.update_layout(bargap=0.1, height=350)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption("Distribution of Body Mass Index by Gender")

    st.markdown("---")

    # [Row 2] 상관관계 분석 (운동 시간 vs 칼로리 소모)
    c3, c4 = st.columns([2, 1])
    
    with c3:
        st.subheader("🔥 운동 시간과 칼로리 소모량 상관관계")
        fig_scatter = px.scatter(
            df, 
            x="Session_Duration (hours)", 
            y="Calories_Burned", 
            color="Workout_Type",
            size="Avg_BPM", 
            hover_data=["Age", "Weight (kg)"],
            template="plotly_white"
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with c4:
        st.subheader("💧 물 섭취량과 체지방률")
        # 3D 산점도 느낌의 버블 차트
        fig_bubble = px.scatter(
            df, x="Water_Intake (liters)", y="Fat_Percentage",
            color="Gender", size="Workout_Frequency (days/week)",
            size_max=15, opacity=0.6
        )
        fig_bubble.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_bubble, use_container_width=True)

    # -----------------------------------------------------------
    # 4. 데이터 그리드 (Raw Data 뷰)
    # -----------------------------------------------------------
    st.markdown("### 📋 상세 데이터 조회")
    with st.expander("원본 데이터셋 미리보기 (Click to expand)"):
        st.dataframe(df.style.highlight_max(axis=0, color='#fffdc1'), use_container_width=True)
        
    # 다운로드 버튼 (기능만 존재)
    st.download_button(
        label="📥 분석 리포트 다운로드 (CSV)",
        data=df.to_csv().encode('utf-8'),
        file_name='gym_members_analysis_report.csv',
        mime='text/csv',
    )