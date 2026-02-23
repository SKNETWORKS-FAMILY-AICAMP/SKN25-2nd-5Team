import streamlit as st
import pandas as pd
from utils.db import get_db


def render_management():

    st.title("👥 Employee Management")
    st.markdown("직원 데이터를 추가하고 관리합니다.")


    #if "user_id" not in st.session_state:
    #    st.warning("로그인이 필요합니다.")
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = 1  # 테스트용 유저
        #return

    conn = get_db()
    user_id = st.session_state["user_id"]

    tab1, tab2 = st.tabs(["➕ 직원 추가", "📋 직원 수정"])

   
    # 1. 직원 추가 탭
    with tab1:

        with st.form("employee_form"):

            st.subheader("① 기본 정보")
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("이름")
                age = st.number_input("나이", 18, 60)
                gender = st.selectbox("성별", ["Male", "Female"])
                marital_status = st.selectbox("결혼 여부", ["Single", "Married", "Divorced"])

            with col2:
                education = st.selectbox("교육 수준 (1~5)", [1,2,3,4,5])
                education_field = st.selectbox(
                    "전공 분야",
                    ["생명과학", "의학", "마케팅", "공학/기술", "인사", "기타"]
                )
                distance_from_home = st.number_input("집과의 거리", 0)

            st.divider()
            st.subheader("② 직무 정보")

            col3, col4 = st.columns(2)

            with col3:
                department = st.selectbox(
                    "부서",
                    ["영업부", "연구개발부", "인사부"]
                )
                job_role = st.selectbox(
                    "직무 분류",
                    [
                        "전문직",
                        "인사직",
                        "연구/기술직",
                        "연구/관리직",
                        "생산/관리직",
                        "관리직",
                        "영업직"
                    ]
                )
                job_level = st.number_input("직급 (1~5)", 1, 5)

            with col4:
                business_travel = st.selectbox(
                    "출장 빈도",
                    ["Travel_Rarely", "Travel_Frequently", "Non-Travel"]
                )
                overtime = st.selectbox("초과근무 여부", ["Yes", "No"])
                job_involvement = st.slider("직무 몰입도 (1~4)", 1, 4)

            st.divider()
            st.subheader("③ 만족도 및 성과")

            col5, col6 = st.columns(2)

            with col5:
                job_satisfaction = st.slider("직무 만족도 (1~4)", 1, 4)
                environment_satisfaction = st.slider("근무환경 만족도 (1~4)", 1, 4)
                relationship_satisfaction = st.slider("대인관계 만족도 (1~4)", 1, 4)

            with col6:
                work_life_balance = st.slider("워라밸 (1~4)", 1, 4)
                performance_rating = st.slider("성과 평가 등급 (1~4)", 1, 4)
                percent_salary_hike = st.number_input("연봉 인상률 (%)", 0)

            st.divider()
            st.subheader("④ 경력 및 급여")

            col7, col8 = st.columns(2)

            with col7:
                monthly_income = st.number_input("월급", 0)
                total_working_years = st.number_input("총 근무 연수", 0)
                years_at_company = st.number_input("현 회사 근속 연수", 0)

            with col8:
                years_in_current_role = st.number_input("현 직무 근속 연수", 0)
                years_since_last_promotion = st.number_input("마지막 승진 후 연수", 0)
                num_companies_worked = st.number_input("이전 근무 회사 수", 0)

            submitted = st.form_submit_button("💾 저장")

        # 저장 로직
        if submitted:
            try:
                cursor = conn.cursor()
                query = """
                INSERT INTO employees (
                    user_id, name, age, business_travel, department,
                    distance_from_home, education, education_field,
                    environment_satisfaction, gender, job_involvement,
                    job_level, job_satisfaction, marital_status,
                    monthly_income, num_companies_worked, overtime,
                    percent_salary_hike, performance_rating,
                    relationship_satisfaction, total_working_years,
                    work_life_balance, years_at_company,
                    years_in_current_role, years_since_last_promotion,
                    job_role
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    user_id, name, age, business_travel, department,
                    distance_from_home, education, education_field,
                    environment_satisfaction, gender, job_involvement,
                    job_level, job_satisfaction, marital_status,
                    monthly_income, num_companies_worked, overtime,
                    percent_salary_hike, performance_rating,
                    relationship_satisfaction, total_working_years,
                    work_life_balance, years_at_company,
                    years_in_current_role, years_since_last_promotion,
                    job_role
                )

                cursor.execute(query, values)
                conn.commit()

                st.success("직원 정보가 저장되었습니다.")

            except Exception as e:
                conn.rollback()
                st.error(f"저장 오류: {e}")

  
    # 2️. 직원 목록 탭

    with tab2:

        query = "SELECT * FROM employees WHERE user_id = %s"
        df = pd.read_sql(query, conn, params=(user_id,))

        if df.empty:
            st.info("등록된 직원이 없습니다.")
            return

        selected_name = st.selectbox("수정할 직원 선택", df["name"])
        selected_row = df[df["name"] == selected_name].iloc[0]

        st.divider()

        with st.form("edit_form"):

            st.subheader("① 기본 정보")
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("이름", value=selected_row["name"])
                age = st.number_input("나이", 18, 60, value=int(selected_row["age"]))
                gender = st.selectbox("성별", ["Male", "Female"],
                                    index=["Male","Female"].index(selected_row["gender"]))
                marital_status = st.selectbox("결혼 여부",
                                            ["Single", "Married", "Divorced"],
                                            index=["Single","Married","Divorced"].index(selected_row["marital_status"]))

            with col2:
                education = st.selectbox("교육 수준 (1~5)",
                                        [1,2,3,4,5],
                                        index=[1,2,3,4,5].index(selected_row["education"]))
                education_field_options = ["생명과학", "의학", "마케팅", "공학/기술", "인사", "기타"]
                education_field = st.selectbox("전공 분야",
                                            education_field_options,
                                            index=education_field_options.index(selected_row["education_field"]))
                distance_from_home = st.number_input("집과의 거리",
                                                    value=int(selected_row["distance_from_home"]))

            st.divider()
            st.subheader("② 직무 정보")

            col3, col4 = st.columns(2)

            department_options = ["영업부", "연구개발부", "인사부"]
            job_role_options = [
                "전문직","인사직","연구/기술직",
                "연구/관리직","생산/관리직",
                "관리직","영업직"
            ]

            with col3:
                department = st.selectbox("부서",
                                        department_options,
                                        index=department_options.index(selected_row["department"]))
                job_role = st.selectbox("직무 분류",
                                        job_role_options,
                                        index=job_role_options.index(selected_row["job_role"]))
                job_level = st.number_input("직급 (1~5)",
                                            1, 5,
                                            value=int(selected_row["job_level"]))

            with col4:
                business_travel_options = ["Travel_Rarely","Travel_Frequently","Non-Travel"]
                business_travel = st.selectbox("출장 빈도",
                                            business_travel_options,
                                            index=business_travel_options.index(selected_row["business_travel"]))
                overtime = st.selectbox("초과근무 여부",
                                        ["Yes","No"],
                                        index=["Yes","No"].index(selected_row["overtime"]))
                job_involvement = st.slider("직무 몰입도 (1~4)",
                                            1,4,
                                            value=int(selected_row["job_involvement"]))

            st.divider()
            st.subheader("③ 만족도 및 성과")

            col5, col6 = st.columns(2)

            with col5:
                job_satisfaction = st.slider("직무 만족도 (1~4)",1,4,value=int(selected_row["job_satisfaction"]))
                environment_satisfaction = st.slider("근무환경 만족도 (1~4)",1,4,value=int(selected_row["environment_satisfaction"]))
                relationship_satisfaction = st.slider("대인관계 만족도 (1~4)",1,4,value=int(selected_row["relationship_satisfaction"]))

            with col6:
                work_life_balance = st.slider("워라밸 (1~4)",1,4,value=int(selected_row["work_life_balance"]))
                performance_rating = st.slider("성과 평가 등급 (1~4)",1,4,value=int(selected_row["performance_rating"]))
                percent_salary_hike = st.number_input("연봉 인상률 (%)",
                                                    value=int(selected_row["percent_salary_hike"]))

            st.divider()
            st.subheader("④ 경력 및 급여")

            col7, col8 = st.columns(2)

            with col7:
                monthly_income = st.number_input("월급",
                                                value=int(selected_row["monthly_income"]))
                total_working_years = st.number_input("총 근무 연수",
                                                    value=int(selected_row["total_working_years"]))
                years_at_company = st.number_input("현 회사 근속 연수",
                                                value=int(selected_row["years_at_company"]))

            with col8:
                years_in_current_role = st.number_input("현 직무 근속 연수",
                                                        value=int(selected_row["years_in_current_role"]))
                years_since_last_promotion = st.number_input("마지막 승진 후 연수",
                                                            value=int(selected_row["years_since_last_promotion"]))
                num_companies_worked = st.number_input("이전 근무 회사 수",
                                                    value=int(selected_row["num_companies_worked"]))

            submitted_edit = st.form_submit_button("수정 저장")

        # 저장로직 
        if submitted_edit:
            cursor = conn.cursor()

            update_query = """
            UPDATE employees
            SET name=%s, age=%s, business_travel=%s, department=%s,
                distance_from_home=%s, education=%s, education_field=%s,
                environment_satisfaction=%s, gender=%s, job_involvement=%s,
                job_level=%s, job_satisfaction=%s, marital_status=%s,
                monthly_income=%s, num_companies_worked=%s, overtime=%s,
                percent_salary_hike=%s, performance_rating=%s,
                relationship_satisfaction=%s, total_working_years=%s,
                work_life_balance=%s, years_at_company=%s,
                years_in_current_role=%s, years_since_last_promotion=%s,
                job_role=%s
            WHERE emp_id=%s
            """

            cursor.execute(update_query, (
                name, age, business_travel, department,
                distance_from_home, education, education_field,
                environment_satisfaction, gender, job_involvement,
                job_level, job_satisfaction, marital_status,
                monthly_income, num_companies_worked, overtime,
                percent_salary_hike, performance_rating,
                relationship_satisfaction, total_working_years,
                work_life_balance, years_at_company,
                years_in_current_role, years_since_last_promotion,
                job_role,
                selected_row["emp_id"]
            ))

            conn.commit()
            st.success("수정 완료!")
            st.rerun()