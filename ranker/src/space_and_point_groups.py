

def get_structure_info(material_ids: list):
    chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)
    data = []
    
    for chunk in chunks: 
        with MPRester(API_KEY) as mpr:
            data += mpr.materials.summary.search(material_ids=chunk, fields=["material_id", "point_group", "crystal_system", "point_group", "spacegroup_symbol"] "spacegroup_number"])
    
    point_group = {}
    crystal_system = {}
    point_group = {}
    spacegroup_symbol = {}
    for material in data:
        point_group[material.material_id] = material.point_group
        crystal_system[material.material_id] = material.crystal_system
        point_group[material.material_id] = material.point_group
        spacegroup_symbol[material.material_id] = material.spacegroup_symbol
    
    return point_group, crystal_system, point_group, pd.series(spacegroup_symbol)