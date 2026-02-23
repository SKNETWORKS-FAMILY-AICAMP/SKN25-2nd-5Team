import streamlit as st

def render_sidebar():
    st.markdown("""
        <style>
            /* 상단 버튼 영역 스타일 */
            div.stButton > button {
                width: 100%;
                border-radius: 10px;
                border: 1px solid #f0f2f6;
                font-weight: bold;
                transition: all 0.3s ease;
                height: 3em; /* 버튼 높이 고정 */
            }
            
            /* 버튼 호버 효과 */
            div.stButton > button:hover {
                background-color: #e6f3ff;
                border-color: #4ECDC4;
                color: #4ECDC4;
                transform: translateY(-2px); /* 살짝 위로 떠오르는 효과 */
            }
            
            /* 메인 컨텐츠 영역 상단 여백 조정 (메뉴바와 간격) */
            .block-container {
                padding-top: 5rem !important;
                padding-bottom: 2rem !important;
            }
                
            /* (선택사항) Streamlit 기본 햄버거 메뉴와 헤더 간소화가 필요하면 아래 주석 해제 */
            /* header {visibility: hidden;} */
        </style>
    """, unsafe_allow_html=True)
    
    pages = {
        "Dashboard": "menu_dashboard",
        "Prediction": "menu_prediction",
        "Employee 관리": "menu_employee",
        "Simulation": "menu_simulation",
        "Optimization": "menu_optimization",
        "HrRetention": "menu_hr_retention"
    }
    # -----상단: 사용자 정보 및 로그아웃-----
    with st.sidebar:
        st.write(f"👤 **{st.session_state.get('username', 'User')}**님 접속 중")
        if st.button("로그아웃", type="primary"):
            st.session_state['is_logged_in'] = False
            st.session_state['username'] = None
            if 'employee_data' in st.session_state:
                del st.session_state['employee_data']
            st.rerun()
        st.divider() #구분선
        
    # -----메인 상단 메뉴바-----
    #메뉴바 렌더링 
    cols = st.columns(len(pages))

    # 각 컬럼에 버튼 배치
    for i, (page_name, key) in enumerate(pages.items()):
        with cols[i]:
            btn_type = "primary" if st.session_state.current_page == page_name else "secondary"
            if st.button(page_name, key=key, type=btn_type, use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()  