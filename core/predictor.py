import pandas as pd
from core.loader import load_model_assets

class AttritionPredictor:
    def __init__(self):
        self.model = load_model_assets()

    def predict_probability(self, input_data: pd.DataFrame):
        if self.model is None:
            return []
        
        probs = self.model.predict_proba(input_data)[:, 1]
        return probs