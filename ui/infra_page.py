import streamlit as st

def render_guide_page():
    # 1. 커스텀 CSS (화려하고 예쁜 UI를 위한 스타일링)
    st.markdown("""
        <style>
        /* 메인 타이틀 그라데이션 효과 */
        .main-title {
            font-size: 3rem;
            font-weight: 900;
            background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298, #00C9FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            text-align: center;
        }
        .sub-title {
            text-align: center;
            color: #666;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        /* 기능 설명 카드 UI */
        .feature-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #f0f2f6;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            border-color: #2a5298;
        }
        .card-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .card-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 10px;
        }
        .card-text {
            color: #4b5563;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        /* 스텝(단계) 강조 UI */
        .step-box {
            background: linear-gradient(135deg, #f6f8fb 0%, #f1f5f9 100%);
            border-left: 5px solid #00C9FF;
            padding: 15px 20px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. 메인 헤더
    st.markdown('<p class="main-title">✨ HR Analytics AI 솔루션 가이드</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">데이터 기반의 똑똑한 인사 관리, 지금 바로 시작해보세요!</p>', unsafe_allow_html=True)
    st.divider()

    # 3. 핵심 기능 소개 (카드 레이아웃 - 3열)
    st.markdown("### 🚀 핵심 기능 한눈에 보기")
    st.write("우리 조직의 퇴사율을 낮추고 핵심 인재를 지키기 위한 3단계 솔루션을 제공합니다.")
    st.write("") # 여백
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">🎯</div>
            <div class="card-title">1. 퇴사 위험도 예측</div>
            <div class="card-text">
                전/현직 직원의 데이터를 AI가 분석하여 <b>개별 직원의 퇴사 확률</b>을 정확하게 예측합니다. 어떤 요인이 가장 큰 영향을 미쳤는지 SHAP 분석을 통해 직관적으로 확인하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">📊</div>
            <div class="card-title">2. 전사 대시보드</div>
            <div class="card-text">
                조직 전체의 인력 현황과 AI 예상 퇴사율을 <b>시각화된 차트</b>로 제공합니다. 부서별 위험도를 비교하고 전사적인 HR 트렌드를 한눈에 파악할 수 있습니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="card-icon">💰</div>
            <div class="card-title">3. 예산 최적화 솔루션</div>
            <div class="card-text">
                한정된 예산과 승진 TO 안에서 <b>퇴사율을 가장 크게 낮출 수 있는 최적의 보상 조합</b>(연봉 인상, 승진, 야근 면제 등)을 AI가 자동으로 찾아 제안합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.divider()

    # 4. 단계별 사용 방법 (가독성을 높인 박스 UI)
    st.markdown("### 📖 3 Step 초간단 사용 방법")
    
    st.markdown("""
    <div class="step-box">
        <b>Step 1. 데이터 업로드 (Prediction 페이지)</b><br>
        인사 데이터가 담긴 CSV 파일을 업로드하세요. 시스템이 자동으로 데이터 유효성을 검사하고 안전하게 DB에 저장합니다.
    </div>
    <div class="step-box">
        <b>Step 2. 전사 현황 진단 (Dashboard 페이지)</b><br>
        데이터가 업로드되면 Dashboard로 이동하여 우리 회사의 현재 건강 상태(위험군 비율, 주요 퇴사 원인 등)를 진단합니다.
    </div>
    <div class="step-box">
        <b>Step 3. 최적의 보상안 도출 (Optimization 페이지)</b><br>
        이번 분기 가용 예산과 승진 가능 인원을 입력하고 실행 버튼을 누르세요. AI가 가성비 최고의 '집중 관리 리스트'를 뽑아드립니다.
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # 5. 자주 묻는 질문 (Expander 활용)
    st.markdown("### 💡 자주 묻는 질문 (FAQ)")
    
    with st.expander("Q. 업로드하는 데이터는 안전하게 보관되나요?"):
        st.write("네! 업로드하신 데이터는 암호화된 사내 데이터베이스(DB)에 안전하게 저장되며, 로그인한 사용자 본인의 데이터만 조회 및 분석할 수 있도록 철저하게 분리되어 있습니다.")
        
    with st.expander("Q. AI의 퇴사 예측은 어떤 원리로 이루어지나요?"):
        st.write("수많은 인사 데이터(나이, 근속년수, 워라밸, 월급, 야근 여부 등)를 바탕으로 학습된 머신러닝 알고리즘(RandomForest 등)을 사용합니다. 특정 직원의 패턴이 과거 퇴사자들의 패턴과 얼마나 유사한지 확률(%)로 수치화하여 보여줍니다.")
        
    with st.expander("Q. 최적화 결과에서 '야근 면제'만 너무 많이 나옵니다. 왜 그런가요?"):
        st.write("알고리즘은 적은 비용으로 최대의 효과를 내는 '가성비(ROI)'를 우선으로 찾습니다. 실제 실무 환경에 맞추어 제약 조건(예: 야근 면제 가능 인원 TO 설정)을 함께 입력해주시면 훨씬 현실적이고 유용한 솔루션을 얻을 수 있습니다.")

    # 6. 하단 배너 (Call to Action)
    st.write("")
    st.info("👋 **도움이 더 필요하신가요?** 좌측 사이드바의 각 메뉴를 클릭하여 AI HR 솔루션을 직접 체험해 보세요!")