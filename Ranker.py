import pandas as pd
import numpy as np


class Ranker():
    def __init__(self, model, initial_prompt):
        self.model = model
        self.initial_prompt = initial_prompt

    def answer(self, material_ids):
        '''TODO get model response. Investigate langchain or llamaindex tools.'''
        df = self.create_table(material_ids)
        prompt = f"{self.initial_prompt}\n{df.to_csv()}"

    def create_table(self, material_ids):
        df = pd.DataFrame(index=material_ids, columns=["synthesizability"])
        df.index.name = "material_id"
        
        for material_id in material_ids:
            df.loc[material_id, "synthesizability"] = self.get_synthesizability(material_id)
            
        return df
    
    def get_synthesizability(self, material_id):
        '''TODO implement'''
        return 0.5