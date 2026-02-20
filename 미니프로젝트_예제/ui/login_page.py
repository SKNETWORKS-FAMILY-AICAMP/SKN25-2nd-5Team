import streamlit as st
from utils.auth_func import login_user, register_user
from time import sleep

def render_login_page(conn):
    st.title("🔐 HR Analytics SaaS")

    tab1, tab2 = st.tabs(["로그인", "회원가입"])

    with tab1:
        st.subheader("로그인")
        username = st.text_input("아이디", key="login_id")
        password = st.text_input("비밀번호",type="password", key="login_pw")

        if st.button("로그인 하기"):
            user = login_user(conn, username, password)
            if user:
                st.success(f"환영합니다, {username}님!")
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = username
                sleep(0.5)
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 잘못되었습니다")

    with tab2:
        st.subheader("회원가입")
        new_user = st.text_input("새 아이디", key="new_id")
        new_pass = st.text_input("새 비밀번호", type="password",key="new_pw")

        if st.button("회원가입 하기"):
            if register_user(conn, new_user, new_pass):
                st.success("회원가입 성공! 로그인 탭에서 로그인해주세요")
            else:
                st.warning("이미 존재하는 아이디입니다")
    