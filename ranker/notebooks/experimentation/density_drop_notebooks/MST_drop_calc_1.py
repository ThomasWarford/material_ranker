#!/usr/bin/env python
# coding: utf-8

# # Find maximum drop in number density along vector(s) connecting nearest neighbour sites 

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# import jax
# import jax.numpy as jnp

import sys
sys.path.append('/notebooks/ranker/src/')
from api_source import *
from interpolator_and_old_drop_functions import *

from pymatgen.core.structure import Structure
from pymatgen.transformations.standard_transformations import SupercellTransformation
from pymatgen.analysis.graphs import *
from pymatgen.analysis.local_env import CrystalNN, VoronoiNN, MinimumDistanceNN
from pymatgen.util.coord import find_in_coord_list

import networkx as nx


# ## Read in dataframe

# In[2]:


def convert_to_list(string):
    if string.startswith('[') and string.endswith(']'):
        return eval(string)
    else:
        return string
def convert_string_to_dict(string_dict):
    return eval(string_dict)
main_df = pd.read_csv("df_full_structure.csv", converters={'paper_titles': convert_to_list, "sub_lattice_structure": convert_string_to_dict,
                                                              "lattice_structure": convert_string_to_dict})
main_df.set_index("material_id", inplace=True)
#main_df['sub_lattice_structure'][0]


# ## Compare new and old single neighbour functions for one mat 
# ##### old function does not seem to match the 27k saved csv values
# ##### new functions read in from .npy file and use scipy interpolate

# In[3]:


# mat_id = 35
# scalar_field = np.load("D:/mp-{0}_chgcar_array.npy".format(mat_id))

# #print(get_nn_density_drop_old(main_df.loc["mp-{0}".format(mat_id)]))
# print(get_nn_density_drop(main_df.loc["mp-{0}".format(mat_id)], scalar_field))


# In[4]:


#print(Structure.from_dict(main_df["lattice_structure"][10000]).make_supercell([2,2,2]))
#print(Structure.from_dict(main_df["sub_lattice_structure"][10000]))
#Structure.from_dict(main_df["lattice_structure"][10000]).make_supercell([2,2,2]).sites[0].frac_coords
#Structure.from_dict(main_df["lattice_structure"][10000]).make_supercell([2,2,2]).lattice.abc


# # Generate shortest nearest neighbor spanning path of the superlattice using pymatgen

# In[81]:


def find_path(graph, start_site, end_site, weight_code):
    try:
        path = nx.shortest_path(graph, source=start_site, target=end_site, weight=weight_code)
        return path
    except nx.NetworkXNoPath:
        return None  # No path found
        
def scale_weights(graph, n=4):
    """
    ^n the weights of all edges in the graph and rescale
    """
    for u, v, data in graph.edges(data=True):
        if 'weight' in data:
            #print(data['weight'])
            data['weight'] = (data['weight']/10)**n
    return graph

def shortest_atomic_supercell_path(structure, start_index, end_index):
    # initiate neighbour finding algorithm class
    # Neighbour_finder = CrystalNN(weighted_cn=True, search_cutoff= max(structure.lattice.abc)/2, distance_cutoffs=None, 
    #                              x_diff_weight=3.0, porous_adjustment=True)
    #Neighbour_finder = VoronoiNN(cutoff=max(structure.lattice.abc)/2)
    Neighbour_finder = MinimumDistanceNN(tol = 1, cutoff=max(structure.lattice.abc)/3, get_all_sites=True)
    
    # make graph using this neighbor finding algorithm
    graph = StructureGraph.with_local_env_strategy(structure, Neighbour_finder, weights=True)
    #print(graph.types_and_weights_of_connections)
    
    # cube distance weights of edges to penalise 'skipping' sites
    d_weighted_graph = scale_weights(graph.graph)
    #print(d_weighted_graph.edges)
    path = find_path(d_weighted_graph, start_index, end_index, "weight")

    if path:
        #print("Path found:", [structure.sites[i].frac_coords for i in path])  # Convert indices to actual sites

        # we must *2 because supercell measures position as a fraction of SCALED unit vectors i.e. (2a),(2b),(2c)
        # but I have set the charge density array to be between 0 and 2 a for each unit vector
        # so we want the site coordinates to lie between 0 and 2* each unit vector
        return [structure.sites[i].frac_coords*2 for i in path]
    
    else:
        # return maximal drop fraction if no suitable weighted connectivity path found
        # I think, as this suggests large separation between unit cells
        return 1
        
#nn_positions = shortest_atomic_supercell_path(main_df["sub_lattice_structure"][10000])
#print(nn_positions)


# In[84]:


def form_density_supercell(field):
    # super_field is now a 2x2x2 supercell of the original field
    return np.tile(field, (2,2,2))

# Define a function to return drop in number density between just two sites
def get_single_density_drop(density_field, nn_positions, plot_iter):
    # number density grid points for single unit cell (in terms of a,b,c)
    (x,y,z) = [np.linspace(0,2,density_field.shape[i]) for i in range(3)]
    
    try:
        chg_den_interpolated = interpolate_3d(density_field, nn_positions[0], nn_positions[1], x,y,z, n=60)
    except:
        for i in range(len(nn_positions)):
            for j,val in enumerate(nn_positions[i]):
                if val>1:
                    nn_positions[i][j]=1
        chg_den_interpolated = interpolate_3d(density_field, np.abs(np.array(nn_positions[0])), np.abs(np.array(nn_positions[1])), x,y,z, n=40)
    
    #start_val = max(chg_den_interpolated)
    
    # compare to charge density at beginning or end atomic site
    # if used max, that might take value at a non-sublattice site which we might cross
    #start_val = max(chg_den_interpolated[0], chg_den_interpolated[-1])
    index_zone = 10
    start_val = (np.max(chg_den_interpolated[0:index_zone]) + np.max(chg_den_interpolated[-index_zone:]) ) /2
    
    #print(start_val)
    #x=np.linspace(0,1,40)
    #plt.plot(x+x[-1]*plot_iter, chg_den_interpolated)
    #print(chg_den_interpolated)
    
    return (start_val-min(chg_den_interpolated[index_zone:-index_zone]))/start_val


# FUNCTIONS FOR MINIMUM SPANNING TREE
def supercell_MST(structure):
    Neighbour_finder = MinimumDistanceNN(tol = 1, cutoff=max(structure.lattice.abc)/2, get_all_sites=True)
    
    # make graph using this neighbor finding algorithm
    graph = StructureGraph.with_local_env_strategy(structure, Neighbour_finder, weights=True)
    
    # ^4 distance weights of edges to penalise 'skipping' sites
    d_weighted_graph = scale_weights(graph.graph)
    
    Min_span_tree = nx.minimum_spanning_tree(d_weighted_graph.to_undirected(), weight="weight")

    return Min_span_tree

def get_drops_MST(row, density_supercell):
    sub_supercell = Structure.from_dict(row['sub_lattice_structure']).make_supercell([2,2,2])
    mat_ID = row.name
    
    # form minimum spanning tree of sublattice supercell
    MST = supercell_MST(sub_supercell)
    
    connected_sites_coordinates = []
    for edge in MST.edges():
        site1_index, site2_index = edge
        site1 = sub_supercell[site1_index]
        site2 = sub_supercell[site2_index]

        # Step 3: Get the coordinates of the atomic sites
        site1_coords = site1.frac_coords
        site2_coords = site2.frac_coords

        # Step 4: Store the coordinates of the connected pairs
        connected_sites_coordinates.append([site1_coords, site2_coords])

    drops = np.array([])
    for i in range(len(connected_sites_coordinates)-1):
        drops = np.append(drops, get_single_density_drop(density_supercell, connected_sites_coordinates[i], i))
    return drops

# In[87]:


#mat_id = "mp-616821"
#mat_id = "mp-7"
#scalar_field = np.load("D:/{0}_chgcar_array.npy".format(mat_id))
# scalar_field = np.load("charge_density_files/{0}_chgcar_array.npy".format(mat_id))
# density_supercell = form_density_supercell(scalar_field)
# get_drops_along_path(main_df.loc[mat_id], density_supercell, sub=False)  


# # Save to csv when ready (need to update to use .npy inputs)

# In[ ]:
def below_fermi(arr):
    #print(arr)
    boole = False
    for i, num in enumerate(arr):
        #print(num)
        if num == '3' or num == '4':
            boole = True
    return boole

main_df = main_df[main_df["band_gap"]<=1]
#print(len(main_df.index))
# remove materials with no flat band below E_fermi
#main_df["flat_band_below_Ef"] = main_df["flat_segments"].apply(below_fermi)
#df_cut = main_df[main_df["flat_band_below_Ef"]]

# Apply the function to create a new column
MAX_MATERIAL_IDS_LENGTH = 1000
material_ids = df_cut.index.to_list()
#print(len(material_ids))

chunks = divide_chunks(material_ids, MAX_MATERIAL_IDS_LENGTH)

# Initialize an empty DataFrame to store drop values
drop_values_df = pd.DataFrame()

for chunk in chunks:
    d_values = []
    
    id_check = np.array([])
    
    for i, ID in enumerate(chunk):
        try:
            scalar_field = np.load("D:/{0}_chgcar_array.npy".format(ID))
            density_supercell = form_density_supercell(scalar_field) 
            drop_values = get_drops_MST(main_df.loc[ID], density_supercell)
        except:
            # set as -1 if no charge density data is available
            drop_values = [-1]

        #drop_values = get_drops_MST(main_df.loc[ID], density_supercell)
        
        d_values.append(drop_values)
        
        id_check = np.append(id_check, ID)
        
    drop_values_df = pd.concat([drop_values_df, pd.DataFrame([{'mat_id': material_id, 'drop_values': arr} for material_id, arr in zip(id_check, d_values)])])


    # Save drop values to CSV file
    drop_values_df.to_csv('sub_all_fermi_MST_drops.csv', index=False)

