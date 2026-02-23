import os
import joblib
import streamlit as st
import xgboost

@st.cache_resource
def load_model_assets():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #model_path = os.path.join(r"C:\Users\playdata2\Desktop\미니프로젝트_예제\models","best_model.pkl")
    #features_path = os.path.join(r"C:\Users\playdata2\Desktop\미니프로젝트_예제\models", "feature_names.pkl")
    model_path = os.path.join(BASE_DIR, "models", "best_model.pkl")
    features_path = os.path.join(BASE_DIR, "models", "feature_names.pkl")


    print(f"👉 모델 찾는 경로: {model_path}")

    if not os.path.exists(model_path) or not os.path.exists(features_path):
        print("❌ 모델 파일을 찾을 수 없습니다!")
        return None,None
    
    try:
        model = joblib.load(model_path)
        feature_names = joblib.load(features_path)
        print("✅ 모델 로드 성공!")
        return model, feature_names
    except Exception as e:
        print(f"❌ 모델 로드 중 에러 발생: {e}")
        return None, None

