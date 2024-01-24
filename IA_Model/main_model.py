import torch
import numpy as np
from model_constants import *
from ann_model.model import TabularModel


class ann_model():

    def __init__(self):

        self.model = TabularModel(EMB_SZS, CONTINUOUS, BINARIES, OUTPUT, LAYERS, p = DROPOUT)
        self.model.load_state_dict(torch.load(MODEL_FILE))
        self.model.eval()
        
    def load(self,values):
        
        # CREATE TENSORS
        bin_cols = ['Smoke', 'Drink', 'Stroke','Difficult_Walking', 'Gender','Diabetis', 
                    'Exercise', 'Asthma', 'Kidney_Disease', 'Skin_Cancer']
        cat_cols = ['Age','Race','General_Health']
        cont_cols = ['BMI','Physical_Health', 'Mental_Health','Sleep_Time']
        
        bins = np.stack([values[col] for col in bin_cols])
        self.bins = torch.tensor(bins, dtype=torch.int64)
        cats = np.stack([values[col] for col in cat_cols])
        self.cats = torch.tensor(cats, dtype=torch.int64)
        conts = np.stack([values[col] for col in cont_cols])
        self.conts = torch.tensor(conts, dtype=torch.float)
        
    def evaluate(self):
        with torch.no_grad():
            z = self.model(self.cats, self.conts, self.bins)
        return round(z.item(),2) # The predicted fare amount



