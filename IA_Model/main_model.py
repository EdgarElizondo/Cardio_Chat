import torch
import numpy as np
import pandas as pd
from .model_constants import *
from .ann_model.model import TabularModel


class ann_model():
    # Dictionaries use to replace the categorical values to numerical values
    _age_code = {
            '18-24':0, '25-29':1, '30-34':2, '35-39':3, '40-44':4, '45-49':5, '50-54':6,
            '55-59':7, '60-64':8, '65-69':9, '70-74':10, '75-79':11, '80+':12,
        }
    _ethnic_code = {
            'Navive American': 0, 'Asian': 1, 
            'Black': 2, 'Latin': 3, 'Other': 4, 'White': 5
    }
    _health_code = {
        'Excelente':0 , 'Regular': 1, 'Buena': 2, 'Mala': 3, 'Muy buena': 4
    }

    def __init__(self):

        self.model = TabularModel(EMB_SZS, CONTINUOUS, BINARIES, OUTPUT, LAYERS, p = DROPOUT)
        self.model.load_state_dict(torch.load(MODEL_FILE))
        self.model.eval()
        
    def load(self,values):
        
        # Replace Categorical values for their respective code value
        values["Age"] = self._age_code[values["Age"]]
        values["Race"] = self._ethnic_code[values["Race"]]
        values["General_Health"] = self._health_code[values["General_Health"]]
        
        # Selecting the key values to implement in the Neural Network
        bin_cols = ['Smoke', 'Drink', 'Stroke','Difficult_Walking', 'Gender','Diabetis', 
                    'Exercise', 'Asthma', 'Kidney_Disease', 'Skin_Cancer']
        cat_cols = ['Age','Race','General_Health']
        cont_cols = ['BMI','Physical_Health', 'Mental_Health','Sleep_Time']
        
        # Create tensors
        df = pd.DataFrame(values, index=[0])
        bins = np.stack([df[col].values for col in bin_cols],1)
        self.bins = torch.tensor(bins, dtype=torch.int64)
        cats = np.stack([df[col].values for col in cat_cols],1)
        self.cats = torch.tensor(cats, dtype=torch.int64)
        conts = np.stack([df[col].values for col in cont_cols],1)
        self.conts = torch.tensor(conts, dtype=torch.float)
        
    def evaluate(self):
        with torch.no_grad():
            z = self.model(self.cats, self.conts, self.bins)
        return round(z.item(),2) # The predicted fare amount



