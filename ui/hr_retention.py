import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utils.db import get_db


def save_memo_to_db(emp_id, content):
    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO employee_memos (emp_id, content)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (emp_id, content))
        conn.commit()

        cursor.close()
        #conn.close()

        #load_memos_from_db.clear()

        return True

    except Exception as e:
        print("INSERT ERROR:", e)
        st.error(f"❌ 메모 저장 오류: {e}")
        return False

#@st.cache_data
def load_memos_from_db(emp_id):
    try:
        conn = get_db()
        
        query = """
        SELECT content, created_at 
        FROM employee_memos 
        WHERE emp_id = %s
        ORDER BY created_at DESC
        """
        memos_df = pd.read_sql(query, conn, params=(emp_id,))
        #conn.close()
        return memos_df
    except Exception as e:
        st.error(f"❌ 메모 로드 오류: {e}")
        return pd.DataFrame()
    
def hr_retention_dashboard():
    st.title("🚨 핵심 인재(High-Po) 집중 관리 시스템")

    @st.cache_data(ttl=600)
    def load_data_from_db():
        try:
            conn = get_db()
            id = st.session_state["user_id"] 
            query = f"""
                    SELECT *
                    FROM employees e
                    WHERE e.user_id = {id}
                    """
            df = pd.read_sql(query, conn)
            #conn.close()
            df['attrition'] = pd.to_numeric(df['attrition'], errors='coerce')
            #df['attrition'] = (df['attrition'] * 100).fillna(0).astype(int)
            return df
        except Exception as e:
            st.error(f"❌ DB 연결 오류: {e}")
            return pd.DataFrame()

    df = load_data_from_db()

    if df.empty:
        st.warning("표시할 데이터가 없습니다. DB 연결 상태를 확인해주세요.")
        return

    # --- 1. 사이드바 필터 ---
    st.sidebar.header("🔍 필터 설정")
    risk_threshold = st.sidebar.slider("퇴사 위험 임계치 (%)", 0, 100, 70)  # 0~100%

    # --- 2. attrition 컬럼을 숫자(float)로 변환하고 0~1 범위라고 가정 ---
    df['attrition_numeric'] = pd.to_numeric(df['attrition'], errors='coerce').fillna(0)

    # --- 3. 사이드바 기준 필터링 (0~100% 기준으로 맞춤) ---
    priority_df = df[
        (df['performance_rating'] >= 3) &
        ((df['attrition_numeric']*100) <= risk_threshold)
    ].sort_values(by='attrition_numeric', ascending=False)

    # --- 4. 메인 화면 출력 ---
    col_list, col_manage = st.columns([1.3, 1])

    with col_list:
        st.subheader(f"📍 긴급 면담 대상 ({len(priority_df)}명)")
        if not priority_df.empty:
            display_cols = {
                'emp_id': '사번',
                'name': '이름',
                'department': '부서',
                'attrition_numeric': '퇴사확률',
                'overtime': '야근여부',
                'performance_rating':'성과등급'
            }
            st.dataframe(
                priority_df[list(display_cols.keys())].rename(columns=display_cols)
                .style.format({'퇴사확률': '{:.1%}'})
                .background_gradient(subset=['퇴사확률'], cmap='Reds'),
                use_container_width=True, hide_index=True
            )
        else:
            st.success("✅ 관리 기준 내에 위험 인재가 없습니다.")
    with col_manage:
        st.subheader("📝 상세 정보 및 기록")
        if not priority_df.empty:
            selected_name = st.selectbox("직원 선택", priority_df['name'].tolist())
            emp = priority_df[priority_df['name'] == selected_name].iloc[0]
            eid = int(emp['emp_id'])

            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**사번:** {eid}")
                    st.write(f"**부서:** {emp['department']}")
                    st.write(f"**야근 여부:** `{emp['overtime']}`")
                with c2:
                    st.write(f"**성과 등급:** {emp['performance_rating']}")
                    st.write(f"**직무 만족도:** {'⭐' * int(emp['job_satisfaction'])}")
                    st.write(f"**급여:** ${emp['monthly_income']:,}")
                st.divider()
                st.progress(emp['attrition'], text=f"이탈 위험도: {emp['attrition']:.1%}")

            # --- [메모 탭: DB 연동] ---
            t_input, t_history = st.tabs(["✍️ 메모 입력", "📚 관리 이력"])

            with t_input:
                # key값에 eid를 넣어 직원 변경 시 입력창 초기화 유도
                memo_text = st.text_area("내용 입력", key=f"input_{eid}", placeholder="면담 내용을 입력하세요.")
                if st.button("저장하기", use_container_width=True, type="primary"):
                    if memo_text.strip():
                        # DB에 저장 시도
                        if save_memo_to_db(eid, memo_text):
                            st.success("저장 완료!")
                    else:
                        st.warning("내용을 입력해주세요.")

            with t_history:
                # DB에서 실시간으로 해당 직원의 메모 이력 가져오기
                history_df = load_memos_from_db(eid)
                if not history_df.empty:
                    for _, row in history_df.iterrows():
                        with st.chat_message("user", avatar="🏢"):
                            # DB의 created_at 시간을 포맷
                            if pd.notnull(row['created_at']):
                                st.caption(f"📅 {row['created_at'].strftime('%Y-%m-%d %H:%M')}")
                            st.write(row['content'])
                else:
                    st.info("기록된 메모 이력이 없습니다.")
        else:
            st.info("대상자를 선택해주세요.")