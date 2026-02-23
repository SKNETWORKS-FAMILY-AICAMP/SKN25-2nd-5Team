

def validate_uploaded_data(df):
    required_columns = ['나이','출장빈도'] # 필수 컬럼 일부
    
    # 1. 컬럼이 다 있는지 확인
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return False, f"누락된 컬럼이 있습니다: {missing_cols}"
    
    return True, "데이터 검증 통과"