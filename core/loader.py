import os
import joblib
import streamlit as st

@st.cache_resource
def load_model_assets():
    #모델, 스케일러 로드, 메모리에 캐싱
    model_path = os.path.join("models","")
    
    try:
        model = joblib.load(model_path)
        return model
    except FileExistsError:
        return None