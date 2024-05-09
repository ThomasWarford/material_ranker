import pandas as pd
import numpy as np
#from bibtexparser import parse_string
import pandas as pd

from pymatgen.core import Structure 
from mp_api.client import MPRester
from key import API_KEY # keep API key off github!

from scipy.interpolate import RegularGridInterpolator


def interpolate_3d(scalar_field, p1, p2, x,y,z, n):
    fn = RegularGridInterpolator((x,y,z), scalar_field)
    l1 = np.linspace(0,1,n)
    line = p1+(p2-p1)*l1[:,None]
    return fn(line)


def get_nn_site(str_dict):
    # return positions of first and second sites (I believe they are in order of closest neighbours already 
    #but not certain)
    # will update this function to make more sophisticated search over neighbours (in main notebook)
    # if doesn't run too slow
    
    # if only a single atomic site present, return the corner of unit cell as comparison position
    if len(str_dict['sites'])==1:
        return [str_dict['sites'][0]['abc'], [1,1,1]]
    
    return [str_dict['sites'][0]['abc'], str_dict['sites'][1]['abc']]


# Define a function to return drop in number density between just two sites
# uses API directly
def get_nn_density_drop_old(row):
    str_dict = row['sub_lattice_structure']
    mat_ID = row.name
    
    try:
        with MPRester(API_KEY) as mpr:
            charge_density = mpr.get_charge_density_from_material_id(mat_ID)
    except:
        return np.nan
    
    nn_positions = get_nn_site(str_dict)
    
    # sometimes one of the positions is very very slightly negative (leading to out of bounds error in interpolate)
    # when I believe it should be basically zero
    
    try:
        chg_den_interpolated = charge_density.linear_slice(nn_positions[0], nn_positions[1], n=70)
    except ValueError:
        for i in range(len(nn_positions)):
            if nn_positions[i]>1:
                nn_positions[i]=1
        chg_den_interpolated = charge_density.linear_slice(np.abs(np.array(nn_positions[0])), np.abs(np.array(nn_positions[1])), n=70)
        
        
    peak = max(chg_den_interpolated)

    return (peak-min(chg_den_interpolated))/peak


# Define a function to return drop in number density between just two sites
# reads in a .npy file to perform calculation
def get_nn_density_drop(row, density_field):
    str_dict = row['sub_lattice_structure']
    mat_ID = row.name
    
    nn_positions = get_nn_site(str_dict)

    # sometimes one of the positions is very very slightly negative (leading to out of bounds error in interpolate)
    # when I believe it should be basically zero
    
    # number density grid points for single unit cell (in terms of a,b,c)
    (x,y,z) = [np.linspace(0,1,density_field.shape[i]) for i in range(3)]
    
    try:
        chg_den_interpolated = interpolate_3d(density_field, nn_positions[0], nn_positions[1], x,y,z, n=70)
    except:
        for i in range(len(nn_positions)):
            for j in nn_positions[i]:
                if j>1:
                    nn_positions[i][j]=1
        chg_den_interpolated = interpolate_3d(density_field, np.abs(np.array(nn_positions[0])), np.abs(np.array(nn_positions[1])), x,y,z, n=70)
        
        
    peak = max(chg_den_interpolated)

    return (peak-min(chg_den_interpolated))/peak