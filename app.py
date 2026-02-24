import streamlit as st
from utils.db import get_db
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.prediction import render_prediction_page
from ui.management import render_management
from ui.simulation import render_simulation_page
from ui.optimization import render_optimization_page
from ui.infra_page import render_guide_page
from ui.login_page import render_login_page
from ui.hr_retention import hr_retention_dashboard

class App:
    def __init__(self):

        st.set_page_config(
            page_title="SK25 2번째 프로젝트!!",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        # DB
        try:
            self.conn = get_db()
        except Exception as e:
            print(e)
            self.conn = None
            print("db연결 실패")

        # 세션 상태 초기화 (로그인 상태 관리)
        if 'is_logged_in' not in st.session_state:
            st.session_state['is_logged_in'] = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "소       개"

        

    def run(self):
        if not st.session_state['is_logged_in']:
            render_login_page(self.conn)
        else:
            render_sidebar()
            # 페이지 라우팅
            page = st.session_state.current_page
            if page == "소       개":
                render_guide_page()
            elif page == "대 시 보 드":
                render_dashboard()
            elif page == "직원 퇴사 예측":
                render_prediction_page()
            elif page == "사 원 관 리":
                render_management()
            elif page == "인사 시뮬레이션":
                render_simulation_page()
            elif page == "인사 최적화":
                render_optimization_page()
            elif page =="인사 유지 관리":
                hr_retention_dashboard()


