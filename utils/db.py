import pymysql
import streamlit as st
import MySQLdb


# pymysql.install_as_MySQLdb()


@st.cache_resource
def _get_cached_db():
    return MySQLdb.connect(
        #host='175.196.76.209',
        host='172.30.199.82',
        user='play',
        passwd='123',
        #db='team2',
        db='encore',
        autocommit=True
    )

def get_db():
    conn = _get_cached_db()

    try:
        conn.ping(True)
    except Exception as e:
        st.warning("데이터베이스 연결이 끊어졌습니다. 재연결을 시도합니다...")
        _get_cached_db.clear()
        conn = _get_cached_db()
    
    return conn