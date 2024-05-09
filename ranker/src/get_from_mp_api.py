import pandas as pd
import numpy as np
#from bibtexparser import parse_string
import pandas as pd

from pymatgen.core import Structure 
from mp_api.client import MPRester
from key import API_KEY # keep API key off github!

MAX_MATERIAL_IDS_LENGTH = 10000

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def get_titles(material_ids: list):
    
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    docs = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            docs += mpr.materials.provenance.search(material_ids=chunk, fields=["material_id", "references"])

    title_dict = {}
    title_ignored_dict = {}
    
    for material in docs:
        titles = []
        titles_ignored = []

        for reference in material.references:
            parsed = parse_string(reference)
            try:
                title = parsed.blocks[0]["title"]
            except:
                print("A", material.material_id, "reference has no title:")
                print(reference)

            if "materials project" in title.lower():
                titles_ignored.append(title)
            else:
                titles.append(title)



        
        title_dict[material.material_id] = titles
        title_ignored_dict[material.material_id] = titles_ignored

    return title_dict, title_ignored_dict

def get_experimentally_observed(material_ids: list):
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "theoretical"])
    
    output = {}
    for material in data:
        output[material.material_id] = not material.theoretical
    
    return output
    
def get_band_gap(material_ids: list):
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "band_gap"])
    
    band_gaps = {}
    for material in data:
        band_gaps[material.material_id] = material.band_gap
    
    return band_gaps


def get_structure_info(material_ids: list):
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "symmetry"])
    
    space_group_symbol = {}
    space_group_number = {}
    crystal_system = {}
    point_group = {}

    for material in data:
        space_group_symbol[material.material_id] = material.symmetry.symbol
        space_group_number[material.material_id] = material.symmetry.number
        crystal_system[material.material_id] = material.symmetry.crystal_system
        point_group[material.material_id] = material.symmetry.point_group
    
    return pd.Series(space_group_symbol), pd.Series(space_group_number), pd.Series(crystal_system), pd.Series(point_group)


def truncate_structure(full_struct, matid, sub_elem):
    #print(type(aa['sites']))
    sites=[]
    for n in full_struct['sites']:
        #print(n)
        if n['label']==sub_elem:
            #print(n)
            sites.append(n)
        #else:
         #   aa['sites'].remove(n)
    #print(sites)
    full_struct['sites']=sites
    #print(aa)
    #############################################
    structure = Structure.from_dict(full_struct)
    #print(structure)
    return structure

def get_sub_structure(material_ids: list, sub_elems):
    #print(sub_elems)
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "structure"])
    
    sublattice_structure = {}
    i=0
    for material in data:
        #print(material.material_id)
        truncated_structure = truncate_structure(material.structure.as_dict(), material.material_id, sub_elems.loc[material.material_id])
        sublattice_structure[material.material_id] = truncated_structure.as_dict()
        i+=1
    return sublattice_structure

def get_structure(material_ids: list):
    #print(sub_elems)
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "structure"])
    
    lattice_structure = {}
    i=0
    for material in data:
        #print(material.material_id)
        lattice_structure[material.material_id] = material.structure.as_dict()
        i+=1
    return lattice_structure

def get_chg_den(material_id):
    with MPRester(API_KEY) as mpr:
        charge_density = mpr.get_charge_density_from_material_id(material_id)
    return charge_density

# def create_table(material_ids):
#         #col_names = ["experimentally_observed", "papers"]
#         col_names = ["experimentally_observed", "band_gap"]
        
#         df = pd.DataFrame(index=material_ids, columns=col_names)
#         df.index.name = "material_id"

#         for material_id in material_ids:
#             df.loc[material_id, "experimentally_observed"] = self.get_experimentally_observed(material_id)
#             df.loc[material_id, "band_gap"] = self.get_band_gap(material_id)
#             #df.loc[material_id, "papers"] = ";".join(self.get_paper_titles(material_id))
            
#         return df
    


