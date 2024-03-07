import pandas as pd
import numpy as np
from bibtexparser import parse_string
import pandas as pd

from mp_api.client import MPRester
from key import API_KEY # keep API key off github!

def get_titles_from_mp(mp_ids)
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