import pandas as pd
from core.loader import load_model_assets
import shap

class AttritionPredictor:
    def __init__(self):
        self.model, self.feature_name = load_model_assets()

    def predict_single(self, employee_row: pd.DataFrame):
        if self.model is None or self.feature_name is None:
            return None
    
        df_processed = employee_row.copy() # 원본 복사

        if '퇴사여부' in df_processed.columns:
            df_processed = df_processed.drop('퇴사여부', axis=1)

        if '초과근무여부' in df_processed.columns:
                df_processed['초과근무여부'] = df_processed['초과근무여부'].map({'Yes': 1, 'No': 0})
        if '성별' in df_processed.columns:
                df_processed['성별'] = df_processed['성별'].map({'Male': 1, 'Female': 0})
                
        df_processed = pd.get_dummies(df_processed) #원핫인코딩

        final_features = pd.DataFrame(columns=self.feature_name)
        for col in self.feature_name:
             if col in df_processed.columns:
                  final_features[col] = df_processed[col].values
             else:
                  final_features[col] = 0
    
        prob = self.model.predict_proba(final_features)[0][1]

        return prob
             
    def get_shap_values(self, employee_row: pd.DataFrame):
        df_processed = employee_row.copy()   

        if '퇴사여부' in df_processed.columns:
                df_processed = df_processed.drop('퇴사여부', axis=1)

        if '초과근무여부' in df_processed.columns:
                df_processed['초과근무여부'] = df_processed['초과근무여부'].map({'Yes': 1, 'No': 0})

        if '성별' in df_processed.columns:
                df_processed['성별'] = df_processed['성별'].map({'Male': 1, 'Female': 0})

        df_processed = pd.get_dummies(df_processed)


        final_features = pd.DataFrame(columns=self.feature_name)

        for col in self.feature_name:
            if col in df_processed.columns:
                final_features[col] = df_processed[col].values
            else:
                final_features[col] = 0

        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(final_features)

        if isinstance(shap_values, list):
             shap_values = shap_values[1]

        person_shap = shap_values[0]

        shap_df = pd.DataFrame({
            'Feature': final_features.columns,
            'SHAP Value': person_shap
        }).sort_values(by='SHAP Value', key=abs, ascending=True).tail(10)


        return shap_df
