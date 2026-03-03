import streamlit as st
import pandas as pd

from core.predictor import AttritionPredictor
from utils.db import get_db
from utils.employee_repo import get_user_employees, insert_employee, update_employee, update_attrition
from utils.column_mapper import ENG_TO_KOR

class EmployeeManagementUI:
    def __init__(self):
        self.conn = get_db()
        self.predictor = AttritionPredictor()

        self.gender_options = ["Male", "Female"]
        self.marital_options = ["Single", "Married", "Divorced"]
        self.edu_options = [1, 2, 3, 4, 5]
        self.edu_field_options = ["생명과학", "의학", "마케팅", "공학/기술", "인사", "기타"]
        self.dept_options = ["영업부", "연구개발부", "인사부"]
        self.job_role_options = ["전문직", "인사직", "연구/기술직", "연구/관리직", "생산/관리직", "관리직", "영업직"]
        self.travel_options = ["Travel_Rarely", "Travel_Frequently", "Non-Travel"]
        self.overtime_options = ["Yes", "No"]

    def render(self):
        st.title("👥 Employee Management")
        st.markdown("직원 데이터를 추가하고 관리합니다.")

        if "user_id" not in st.session_state:
            st.warning("로그인이 필요합니다.")
            return
        
        self.user_id = st.session_state["user_id"]

        tab1, tab2 = st.tabs(["➕ 직원 추가", "📋 직원 수정"])

        with tab1:
            self._render_add_tab()
   
        with tab2:
            self._render_edit_tab()

    def _render_add_tab(self):
        with st.form("employee_add__form"):
            form_data = self._render_form_fields()
            submitted = st.form_submit_button("💾 저장")

            if st.session_state.get("add_success"):
                st.success("직원 정보가 추가되었습니다!")
                del st.session_state["add_success"]

        if submitted:
            self._process_and_save(form_data, action="add")

    def _render_edit_tab(self):
        df = get_user_employees(self.conn, self.user_id)

        if df.empty:
            st.info("등록된 직원이 없습니다.")
            return
        
        selected_emp_id = st.selectbox(
            "수정할 직원 선택",
            df["emp_id"],
            format_func=lambda x: f"{x} - {df[df['emp_id']==x]['name'].values[0]}"
        )

        selected_row = df[df["emp_id"]==selected_emp_id].iloc[0]

        with st.form("employee_edit_form"):
            form_data = self._render_form_fields(default_data=selected_row)
            submitted_edit = st.form_submit_button("💾 수정")

            if st.session_state.get("edit_success"):
                st.success("직원 정보가 수정되었습니다.")
                del st.session_state["edit_success"]

        if submitted_edit:
            self._process_and_save(form_data, action="edit", emp_id=selected_emp_id)

    def _render_form_fields(self, default_data=None):
        def get_val(key, fallback):
            if default_data is not None and key in default_data:
                if isinstance(fallback, int):
                    return int(default_data[key])
                return default_data[key]
            return fallback
        
        def get_idx(options_list, key):
            val = get_val(key, options_list[0])
            return options_list.index(val) if val in options_list else 0

        data = {}

        st.subheader("① 기본 정보")
        col1, col2 = st.columns(2)
        with col1:
            data['name'] = st.text_input("이름", value=get_val("name", ""))
            data['age'] = st.number_input("나이", 18, 60, value=get_val("age", 30))
            data['gender'] = st.selectbox("성별", self.gender_options, index=get_idx(self.gender_options, "gender"))
            data['marital_status'] = st.selectbox("결혼 여부", self.marital_options, index=get_idx(self.marital_options, "marital_status"))

        with col2:
            data['education'] = st.selectbox("교육 수준 (1~5)", self.edu_options, index=get_idx(self.edu_options, "education"))
            data['education_field'] = st.selectbox("전공 분야", self.edu_field_options, index=get_idx(self.edu_field_options, "education_field"))
            data['distance_from_home'] = st.number_input("집과의 거리", value=get_val("distance_from_home", 0))

        st.divider()
        st.subheader("② 직무 정보")
        col3, col4 = st.columns(2)
        with col3:
            data['department'] = st.selectbox("부서", self.dept_options, index=get_idx(self.dept_options, "department"))
            data['job_role'] = st.selectbox("직무 분류", self.job_role_options, index=get_idx(self.job_role_options, "job_role"))
            data['job_level'] = st.number_input("직급 (1~5)", 1, 5, value=get_val("job_level", 1))

        with col4:
            data['business_travel'] = st.selectbox("출장 빈도", self.travel_options, index=get_idx(self.travel_options, "business_travel"))
            data['overtime'] = st.selectbox("초과근무 여부", self.overtime_options, index=get_idx(self.overtime_options, "overtime"))
            data['job_involvement'] = st.slider("직무 몰입도 (1~4)", 1, 4, value=get_val("job_involvement", 3))

        st.divider()
        st.subheader("③ 만족도 및 성과")
        col5, col6 = st.columns(2)
        with col5:
            data['job_satisfaction'] = st.slider("직무 만족도 (1~4)", 1, 4, value=get_val("job_satisfaction", 3))
            data['environment_satisfaction'] = st.slider("근무환경 만족도 (1~4)", 1, 4, value=get_val("environment_satisfaction", 3))
            data['relationship_satisfaction'] = st.slider("대인관계 만족도 (1~4)", 1, 4, value=get_val("relationship_satisfaction", 3))

        with col6:
            data['work_life_balance'] = st.slider("워라밸 (1~4)", 1, 4, value=get_val("work_life_balance", 3))
            data['performance_rating'] = st.slider("성과 평가 등급 (1~4)", 1, 4, value=get_val("performance_rating", 3))
            data['percent_salary_hike'] = st.number_input("연봉 인상률 (%)", value=get_val("percent_salary_hike", 0))

        st.divider()
        st.subheader("④ 경력 및 급여")
        col7, col8 = st.columns(2)
        with col7:
            data['monthly_income'] = st.number_input("월급", value=get_val("monthly_income", 0))
            data['total_working_years'] = st.number_input("총 근무 연수", value=get_val("total_working_years", 0))
            data['years_at_company'] = st.number_input("현 회사 근속 연수", value=get_val("years_at_company", 0))

        with col8:
            data['years_in_current_role'] = st.number_input("현 직무 근속 연수", value=get_val("years_in_current_role", 0))
            data['years_since_last_promotion'] = st.number_input("마지막 승진 후 연수", value=get_val("years_since_last_promotion", 0))
            data['num_companies_worked'] = st.number_input("이전 근무 회사 수", value=get_val("num_companies_worked", 0))

        return data

    def _process_and_save(self, form_data, action="add", emp_id=None):
        try:
            # DB 쿼리에 맞게 튜플 생성 (순서 주의: 원본 코드의 순서 유지)
            values_tuple = (
                form_data['name'], form_data['age'], form_data['business_travel'], form_data['department'],
                form_data['distance_from_home'], form_data['education'], form_data['education_field'],
                form_data['environment_satisfaction'], form_data['gender'], form_data['job_involvement'],
                form_data['job_level'], form_data['job_satisfaction'], form_data['marital_status'],
                form_data['monthly_income'], form_data['num_companies_worked'], form_data['overtime'],
                form_data['percent_salary_hike'], form_data['performance_rating'],
                form_data['relationship_satisfaction'], form_data['total_working_years'],
                form_data['work_life_balance'], form_data['years_at_company'],
                form_data['years_in_current_role'], form_data['years_since_last_promotion'],
                form_data['job_role']
            )

            if action == "add":
                # 추가 시 user_id가 맨 앞에 필요함 (원본 코드 기준)
                insert_values = (self.user_id,) + values_tuple
                target_emp_id = insert_employee(self.conn, insert_values)
                st.session_state["add_success"] = True
            else:
                update_employee(self.conn, emp_id, values_tuple)
                target_emp_id = emp_id
                st.session_state["edit_success"] = True

            # 예측 실행
            row_df = pd.DataFrame([form_data])
            row_df = row_df.rename(columns=ENG_TO_KOR)
            prob = self.predictor.predict_single(row_df)

            if prob is not None:
                update_attrition(self.conn, target_emp_id, float(prob))

            st.rerun()

        except Exception as e:
            st.error(f"저장/수정 오류: {e}")


def render_management():
    ui = EmployeeManagementUI()
    ui.render()