import pandas as pd
import numpy as np
from bibtexparser import parse_string
import pandas as pd

from mp_api.client import MPRester
from key import API_KEY # keep API key off github!

def get_titles(material_ids: list)
    with MPRester(API_KEY) as mpr:
        docs = mpr.materials.provenance.search(fields=["material_id", "references"], material_ids=material_id)

    title_dict = {}
    title_ignored_dict = {}
    
    for material in docs:
        titles = []
        titles_ignored = []

        for reference in material_references:
            parsed = parse_string(reference)
            title = parsed[0]["title"]

            if "materials project" in title.lower():
                titles_ignored.append(title)
            else:
                titles.append(title)



        
        title_dict[material.material_id] = titles
        title_ignored_dict[material.material_id] = titles_ignored

    return title_dict, title_ignored_dict

def get_experimentally_observed(material_ids: list):
    with MPRester(API_KEY) as mpr:
        data = mpr.materials.summary.search(material_ids=material_ids, fields=["material_id", "theoretical"])
    
    output = {}
    for material in data:
        output[material.material_id] = not material.theoretical
    
    return output
    
def get_band_gap(material_id: list):
    with MPRester(API_KEY) as mpr:
        data = mpr.materials.summary.search(material_ids=material_ids, fields=["material_id", "band_gap"])
    
    band_gaps = {}
    for material in data:
        data[material.material_id] = material.band_gap
    
    return band_gaps

def create_table(material_ids):
        #col_names = ["experimentally_observed", "papers"]
        col_names = ["experimentally_observed", "band_gap"]
        
        df = pd.DataFrame(index=material_ids, columns=col_names)
        df.index.name = "material_id"

        for material_id in material_ids:
            df.loc[material_id, "experimentally_observed"] = self.get_experimentally_observed(material_id)
            df.loc[material_id, "band_gap"] = self.get_band_gap(material_id)
            #df.loc[material_id, "papers"] = ";".join(self.get_paper_titles(material_id))
            
        return df
    


