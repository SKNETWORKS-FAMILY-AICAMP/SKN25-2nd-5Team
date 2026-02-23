

def validate_uploaded_data(df):
    required_columns = [
    "name", "age", "business_travel", "department",
    "distance_from_home", "education", "education_field",
    "environment_satisfaction", "gender", "job_involvement",
    "job_level", "job_satisfaction", "marital_status",
    "monthly_income", "num_companies_worked", "overtime",
    "percent_salary_hike", "performance_rating",
    "relationship_satisfaction", "total_working_years",
    "work_life_balance", "years_at_company",
    "years_in_current_role", "years_since_last_promotion",
    "job_role"
] 

    # 1. 컬럼이 다 있는지 확인
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return False, f"누락된 컬럼이 있습니다: {missing_cols}"
    
    return True, "데이터 검증 통과"