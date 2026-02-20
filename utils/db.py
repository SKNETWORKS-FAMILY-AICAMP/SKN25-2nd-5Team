import pymysql
import streamlit as st
import MySQLdb


# pymysql.install_as_MySQLdb()


@st.cache_resource
def get_db():
    return MySQLdb.connect(
        #host='175.196.76.209',
        host='172.30.199.82',
        user='play',
        passwd='123',
        #db='team2',
        db='encore',
        autocommit=True
    )
