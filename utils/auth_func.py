import streamlit as st
import  hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(conn, username, password):
    try:
        hashed_pw = hash_password(password)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query,(username,hashed_pw))
        user = cursor.fetchone()
        return user
    except Exception as e:
        st.error(f"로그인 오류:{e}")
        return None

def register_user(conn, username, password):
    try:
        cursor = conn.cursor()
        check_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(check_query,(username,))
        if cursor.fetchone():
            return False
        
        hashed_pw = hash_password(password)
        
        insert_query = "INSERT INTO users (username,password) VALUES (%s, %s)"
        cursor.execute(insert_query,(username, hashed_pw))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"회원가입 오류 : {e}")
        return False
    
