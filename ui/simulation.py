import streamlit as st
import pandas as pd
from core.predictor import AttritionPredictor
from utils.employee_repo import get_user_employees
from utils.db import get_db


def render_simulation_page():

    st.title("🕹️ 맞춤형 리텐션 시뮬레이션 (What-If)")
    st.markdown("특정 직원의 조건을 변경하여 퇴사 확률 변화를 예측합니다")

    conn = get_db()
    user_id = st.session_state.get("user_id")

    df = get_user_employees(conn, user_id)

    if df.empty:
        st.warning("등록된 직원이 없습니다.")
        return

    # 직원 선택

    selected_emp_id = st.selectbox(
    "시뮬레이션 대상 직원",
        df["emp_id"],
        format_func=lambda x: df[df["emp_id"] == x]["name"].values[0]
    )

    emp_id = selected_emp_id
    selected_row = df[df["emp_id"] == emp_id]

    model_input = selected_row.drop(columns=["emp_id", "user_id"])

    # 영어 → 한국어 (모델 기준)
    reverse_mapping = {
        "name": "이름",
        "age": "나이",
        "business_travel": "출장빈도",
        "department": "부서",
        "distance_from_home": "집과의거리",
        "education": "교육수준",
        "education_field": "전공분야",
        "environment_satisfaction": "근무환경만족도",
        "gender": "성별",
        "job_involvement": "직무몰입도",
        "job_level": "직급",
        "job_satisfaction": "직무만족도",
        "marital_status": "결혼상태",
        "monthly_income": "월급",
        "num_companies_worked": "이전회사근무횟수",
        "overtime": "초과근무여부",
        "percent_salary_hike": "급여인상률",
        "performance_rating": "성과평가등급",
        "relationship_satisfaction": "대인관계만족도",
        "total_working_years": "총경력년수",
        "work_life_balance": "워라밸수준",
        "years_at_company": "현회사근속년수",
        "years_in_current_role": "현재직무근무년수",
        "years_since_last_promotion": "마지막승진후경과년수",
        "job_role": "직무분류"
    }

    model_input = model_input.rename(columns=reverse_mapping)

    predictor = AttritionPredictor()


    # 현재 확률
    current_prob = predictor.predict_single(model_input)

    st.subheader("현재 상태")
    st.metric(
        label="현재 예측된 퇴사 확률",
        value=f"{current_prob * 100:.1f} %"
    )

    st.divider()

    # 직원 바뀌면 Best 재계산

    if (
        "last_emp_id" not in st.session_state
        or st.session_state["last_emp_id"] != emp_id
    ):

        st.session_state["last_emp_id"] = emp_id

        best_prob = current_prob
        best_config = {
            "salary": 0,
            "promote": False,
            "remove_overtime": False
        }

        salary_options = [0, 5, 10, 15, 20, 25, 30]

        for salary in salary_options:
            for promote_option in [False, True]:
                for overtime_option in [False, True]:

                    simulated = model_input.copy()

                    simulated["월급"] *= (1 + salary / 100)

                    if promote_option:
                        simulated["직급"] += 1

                    if overtime_option:
                        simulated["초과근무여부"] = "No"

                    prob = predictor.predict_single(simulated)

                    # 확률 최소화 기준
                    if prob < best_prob:
                        best_prob = prob
                        best_config = {
                            "salary": salary,
                            "promote": promote_option,
                            "remove_overtime": overtime_option
                        }

        st.session_state["best_salary"] = best_config["salary"]
        st.session_state["best_promote"] = best_config["promote"]
        st.session_state["best_overtime"] = best_config["remove_overtime"]
        st.session_state["best_prob"] = best_prob

    # Best 표시
    st.subheader("🔥 AI 추천 Best 조합")

    best_prob = st.session_state["best_prob"]
    delta_best = (best_prob - current_prob) * 100

    st.metric(
        "AI 추천 적용 시 예상 퇴사 확률",
        f"{best_prob * 100:.1f} %",
        delta=f"{delta_best:.1f}%p",
        delta_color="inverse" if delta_best < 0 else "normal"
    )

    st.write("### 📌 AI 추천 액션")

    if st.session_state["best_salary"] > 0:
        st.write(f"- 💰 연봉 {st.session_state['best_salary']}% 인상")

    if st.session_state["best_promote"]:
        st.write("- 🏆 승진 (직급 +1)")

    if st.session_state["best_overtime"]:
        st.write("- 🌙 야근 제거")

    if (
        st.session_state["best_salary"] == 0
        and not st.session_state["best_promote"]
        and not st.session_state["best_overtime"]
    ):
        st.write("- ⚠️ 현재 상태가 이미 최적입니다.")

    st.divider()

    # 사용자 직접 조정
    st.subheader("조건 변경 시뮬레이션")

    col1, col2, col3 = st.columns(3)

    with col1:
        salary_hike = st.slider("연봉 인상률 (%)", 0, 30, 0)

    with col2:
        promote = st.toggle("승진 (직급 +1)")

    with col3:
        remove_overtime = st.toggle("야근 면제")

    if st.button("시뮬레이션 실행", type="primary"):

        simulated = model_input.copy()

        simulated["월급"] *= (1 + salary_hike / 100)

        if promote:
            simulated["직급"] += 1

        if remove_overtime:
            simulated["초과근무여부"] = "No"

        new_prob = predictor.predict_single(simulated)
        delta_value = (new_prob - current_prob) * 100

        st.success("시뮬레이션 완료!")

        st.metric(
            "시뮬레이션 후 퇴사 확률",
            f"{new_prob * 100:.1f} %",
            delta=f"{delta_value:.1f}%p",
            delta_color="inverse" if delta_value < 0 else "normal"
        )