import pandas as pd
import numpy as np
from mp_api.client import MPRester
from key import API_KEY # keep API key off github!
import re


class Ranker():
    def __init__(self, model, initial_prompt):
        self.model = model
        self.initial_prompt = initial_prompt

    def answer(self, material_ids):
        '''TODO get model response. Investigate langchain or llamaindex tools.'''
        df = self.create_table(material_ids)
        prompt = f"{self.initial_prompt}\n{df.to_csv()}"


        return prompt

    def create_table(self, material_ids):
        df = pd.DataFrame(index=material_ids, columns=["experimentally_observed", "papers"])
        df.index.name = "material_id"

        for material_id in material_ids:
            df.loc[material_id, "experimentally_observed"] = self.get_experimentally_observed(material_id)
            df.loc[material_id, "papers"] = ";".join(self.get_paper_titles(material_id))
            
        return df
    

    def get_experimentally_observed(self, material_id: str):
        with MPRester(API_KEY) as mpr:
            data = mpr.materials.summary.search(material_ids=material_id, fields=["theoretical"])
        return not data[0].theoretical


    def get_paper_titles(self, material_id: str):
        with MPRester(API_KEY) as mpr:

            docs = mpr.materials.provenance.search(fields="references", material_ids=material_id)
            bibtexs = docs[0].references


        pattern = r'title\s*=\s*"([^"]+)"'

        titles = []

        for bibtex in bibtexs: 

            match = re.search(pattern, bibtex)
            if match:
                titles.append(match.group(1))

        return titles
    
    def get_theoretical_list(self, material_ids: list):
        '''Unused and untested'''
        with MPRester(API_KEY) as mpr:

            data = mpr.materials.summary.search(material_ids=material_ids, fields=["item.material_id", "theoretical"])

        is_theoretical = {}

        for item in data:
            is_theoretical[item.material_id](item.theoretical)

        return is_theoretical

