import pandas as pd

def get_user_employees(conn, user_id):
    query = "SELECT * FROM employees WHERE user_id = %s"
    return pd.read_sql(query, conn, params=(user_id,))


def insert_employee(conn, values):
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

    cursor.execute(query, values)
    conn.commit()