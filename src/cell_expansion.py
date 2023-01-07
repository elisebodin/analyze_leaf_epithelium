# Lobeyness computation

import napari
import tifffile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from tifffile import imread
from skimage import measure 
from skimage.morphology import convex_hull_image
from skimage.util import map_array
from skimage.measure import label, regionprops, regionprops_table


#function used as extra_properties in the region_props table later to compute the convex hull perimeter of each label
def convex_hull_perimeter(label_img): 
    #create the convex hull of each label
    convex_hull = convex_hull_image(label_img)
    #measure the perimeter of each convex hull
    convex_hull_perimeter = measure.perimeter(convex_hull)
    return convex_hull_perimeter


#function used to create a dataframe with the area, the perimeter, the convex_hull perimeter, the lobeyness and the species of each cell labeled (per species)
def measure_per_species(mask_species_result_path, species_name):
    
    df = pd.DataFrame()
    #looping on the different masks of a file from the sorted per species masks file 
    for image in glob.glob(mask_species_result_path  + "/*.tif"):
        df2 = pd.DataFrame()
        label_img = imread(image)
        
        #computing the different measure for each cell labeled
        props = regionprops_table(
        label_img, 
        properties=['label', 'area', 'perimeter'], 
        extra_properties = (convex_hull_perimeter,))

        #transform into a pandas table
        df2 = pd.DataFrame(props)
        df = pd.concat([df, df2])

    #calculation of lobeyness and adding it to the dataframe
    df = df.assign(lobeyness = df['perimeter']/df['convex_hull_perimeter']) 
        
    #adding a column with the species names    
    df = df.assign(species = f'{species_name}')
    df = df.reset_index(drop = True)
    return df


#function used for creating a parametric map of lobeyness for one mask
def parametric_map(mask_result_path, image_name):
    
    #read the image
    label_img = imread(mask_result_path + "/" + image_name) 
    
    #computing the properties
    props = regionprops_table(
    label_img, 
    properties=['label', 'area', 'perimeter'], 
    extra_properties = (convex_hull_perimeter,))

    #transform into a pandas table
    data = pd.DataFrame(props)
    
    #calculating the lobeyness    
    data = data.assign(lobeyness = data['perimeter']/data['convex_hull_perimeter']) 

    #creating the parametric map
    lobeyness = map_array(
    label_img,
    np.array(data['label']),
    np.array(data['lobeyness']),)
        
    #opening it on a napari viewer    
    viewer = napari.Viewer()
    viewer.add_image(lobeyness, colormap="turbo")
    return