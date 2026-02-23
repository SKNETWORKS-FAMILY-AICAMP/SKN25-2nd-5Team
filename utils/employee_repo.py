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
    return cursor.lastrowid

def update_employee(conn, emp_id, values):
    cursor = conn.cursor()

    query = """
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

    cursor.execute(query, (*values, emp_id))
    conn.commit()

def update_attrition(conn, emp_id, prob):
    cursor = conn.cursor()
    query = """
        UPDATE employees
        SET attrition = %s
        WHERE emp_id = %s
    """
    cursor.execute(query, (prob, emp_id))
    conn.commit()