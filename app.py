import streamlit as st
from utils.db import get_db
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.prediction import render_prediction_page
from ui.simulation import render_simulation_page
from ui.optimization import render_optimization_page
from ui.infra_page import render_infra_page
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
            st.session_state.current_page = "피트니스 데이터 분석"

        

    def run(self):
        if not st.session_state['is_logged_in']:
            render_login_page(self.conn)
        else:
            render_sidebar()
            # 페이지 라우팅
            page = st.session_state.current_page
            if page == "피트니스 데이터 분석":
                render_infra_page(self.conn)
            elif page == "Dashboard":
                render_dashboard()
            elif page == "Prediction":
                render_prediction_page()
            elif page == "Simulation":
                render_simulation_page()
            elif page == "Optimization":
                render_optimization_page()
            elif page =="HrRetention":
                hr_retention_dashboard()


