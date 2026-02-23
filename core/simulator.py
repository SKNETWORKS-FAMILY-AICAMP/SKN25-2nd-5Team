# 조건 적용
def apply_simulation(model_input, salary=0, promote=False, remove_overtime=False):
    simulated = model_input.copy()

    # 연봉 인상
    simulated["월급"] *= (1 + salary / 100)

    # 승진
    if promote:
        simulated["직급"] += 1

    # 야근 제거
    if remove_overtime:
        simulated["초과근무여부"] = "No"

    return simulated

# 단일 시뮬레이션 실행
def calculate_single(model_input, predictor, salary, promote, overtime):
    simulated = apply_simulation(model_input, salary, promote, overtime)
    return predictor.predict_single(simulated)

# 퇴사 확률 최소화하는 Best 조합 탐색
def calculate_best(model_input, predictor):
    current_prob = predictor.predict_single(model_input)

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

                simulated = apply_simulation(
                    model_input,
                    salary,
                    promote_option,
                    overtime_option
                )

                prob = predictor.predict_single(simulated)

                if prob < best_prob:
                    best_prob = prob
                    best_config = {
                        "salary": salary,
                        "promote": promote_option,
                        "remove_overtime": overtime_option
                    }

    return best_config, best_prob