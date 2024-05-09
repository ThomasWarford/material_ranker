# DONT NEED TO RUN ON PAPERSPACE

material_ids = main_df.index.to_list()[1600:]

with MPRester(API_KEY) as mpr:
    for mat_id in material_ids:
        try:
            charge_density = mpr.get_charge_density_from_material_id(mat_id);
            partial = charge_density.data["total"]
            #partial.write_file("charge_density_files/{0}_chgcar.vasp".format(mat_id))
            np.save("charge_density_files/{0}_chgcar_array".format(mat_id), partial)
        except:
            pass