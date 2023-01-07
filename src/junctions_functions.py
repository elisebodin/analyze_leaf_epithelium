# ALL IMPORTS

from scipy import ndimage as ndi
import pandas as pd
import napari
import numpy as np
import tifffile
import skimage
import glob
import matplotlib.pyplot as plt

from tifffile import imread, imwrite
from skimage import morphology
from skimage.filters import threshold_local
from skimage import data          
from skimage.morphology import disk
from skimage.morphology import square
from skimage.filters import median 
from skimage import color
from skimage.morphology import skeletonize 
from skimage.measure import label, regionprops, regionprops_table
from sklearn.neighbors import NearestNeighbors


# SEGMENTATION

def segmentation_junctions(images_path, disk_size, block_size, min_size_object, erosion_size):
    
    global skeleton
    
    #opening the image
    image = tifffile.imread(images_path)
    
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(disk_size)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = block_size)
    
    #segmenting the image to create a mask
    mask = img_filter < thresh

    mask = morphology.remove_small_objects(mask.astype(bool), min_size_object)
    mask = morphology.binary_erosion(mask.astype(bool),morphology.disk(erosion_size))
    
    skeleton = skeletonize(mask)
    skeleton = skeleton.astype(np.uint8)
    
    return skeleton

       
        
# DETERMINE THE TOTAL NUMBER OF JUNCTIONS

# general function to calculate the total number of junctions 

def total_junctions(mask_result_path):
    
    # reads the folder with the masks
    mask = imread(mask_result_path)
    
    # filter that classifies each pixel in the mask depending on the number of pixels connected to it
    connectivity = skimage.filters.rank.sum(mask, square(2))
    
    # pixels with more than 3 adjacent pixels are considered as being part of a junction
    label_connectivity = skimage.morphology.label(connectivity > 2)
    
    # labels the centroids of each group of pixels considered as junctions
    props_connectivity = regionprops_table(label_connectivity, properties=['label','centroid'])
    
    # transform into pandas dataframe containing the centroids and their positions on the x and y axis (here called 0 and 1)
    df_props = pd.DataFrame(props_connectivity)
    
    # renames the colums
    df_props.columns = ['label', 'axis-0', 'axis-1']
    connected = df_props[['axis-0','axis-1']]
    
    # number of junctions is equal to the number of centroids
    nbr_tt_junctions = len(connected)

    return nbr_tt_junctions, connected




# DETERMINE THE NUMBER OF NON TRIANGULAR JUNCTIONS

# general function to calculate the number of non-triangular junctions and create a csv of the centroids from non-triangular junctions

def non_triangular_junctions(connected, centroid_result_path, image_name):
    
    # creates an empty list
    centroids_coordinates_non_triang = []
    
    # takes the coordinates of the centroids of all junctions to put them under points coordinates (sets of two coordinates)
    centroid_points = np.array([list(connected["axis-0"]),list(connected["axis-1"])]).T
    
    # the NearestNeighbor function takes the two nearest neighbors to a point and returns the indice of these points and their distance to one another
    nearest_centroids = NearestNeighbors(n_neighbors= 2, algorithm= "ball_tree").fit(centroid_points)
    
    # if you print the distance you will get one that is equal to zero this is beceause the function considers the nearest point as itself
    distances, indices = nearest_centroids.kneighbors(centroid_points)
    
    # takes only the last column of the distance that cointains the distance to the other point and not to itself 
    centroids_distance = distances[:,1]
    
    # we loop on the total distances to select only the ones that are close (distance inferior to 10 pixels)
    for i in range(0,len(distances)):
        
        if centroids_distance[i] < 10 :
            
            centroids_coordinates_non_triang.append(centroid_points[i])
            
    # create an empty csv if there is no junctions with more than 3 branches 
    if len(centroids_coordinates_non_triang) ==0 :
        
        empty_df = pd.DataFrame(columns=["axis-0", "axis-1"])
        
        empty_df.index.name = "label"
        
        return empty_df
    
    # create a dataframe with the coordinates of the centroids from non-triangular junctions
    df_centroids_coordinates_non_triang = pd.DataFrame(centroids_coordinates_non_triang) 
    
    # rename the columns and change the index to "label"
    df_centroids_coordinates_non_triang.columns = ['axis-0', 'axis-1']
    df_centroids_coordinates_non_triang.index.name = "label"

    # stores the centroids coordinates in the path indicated by "centroid_result_path" in the csv format
    df_centroids_coordinates_non_triang.to_csv(centroid_result_path + "/" + "non_triangular_junctions-" + image_name.replace(".tif", ".csv"))
    
    # number of non-triangular junctions is equal to the number of centroids those junctions
    nbr_non_triangular_junctions = len(df_centroids_coordinates_non_triang)
    
    
    return nbr_non_triangular_junctions



# CREATE FINAL CSV

# function to create the final csv that stores the results

def nbr_junctions_total_csv(images_path, mask_result_path, centroid_result_path):
    
    # creates empty lists of all columns we will create
    image_name_list = []
    nb_total_junctions_list = []
    nb_non_triangular_junctions_list = []
    centroids_fname_list = []
    
    print("looking for this directory :", mask_result_path +"/*.tif")

    
    for mask_path in glob.glob(mask_result_path +"/*.tif") : # this directory is the folder containing the cells to analyse                                        
    
        print(mask_path)
        
        label_img = imread(mask_path)
        image_split = mask_path.split("/")
        image_name = image_split[-1]  # get the image name, only the end of the mask_path
        
        # list with names of images
        image_name_list.append(image_name)
        
        # list with total number of junctions
        total_nb_junctions, connected = total_junctions(mask_path)
        nb_total_junctions_list.append(total_nb_junctions)
        
        # list with the number of non triangular junctions
        nb_non_triangular_junctions = non_triangular_junctions(connected, centroid_result_path, image_name)
        nb_non_triangular_junctions_list.append(nb_non_triangular_junctions)
        
        # list with centroid csv file names
        centroid_fname = ("non_triangular_junctions-" + image_name).replace(".tif", ".csv")
        centroids_fname_list.append(centroid_fname)
        

    # create dictionary
    dict = {'image name' : image_name_list,
            'number non-triangular junctions' : nb_non_triangular_junctions_list,
            'total nb of junctions' : nb_total_junctions_list,
            'non-triangular centroids':centroids_fname_list 
            
           }

    # create dataframe
    final_df = pd.DataFrame(dict)
    
    print(final_df['image name'])
    
    # add a column species for the final graph 
    final_df["species code"] = final_df['image name'].str.split('-').str[:2].str.join("-")


    # create csv from dataframe, save it in the same folder as the centroids
    final_df.to_csv(centroid_result_path + "/number_junctions_total.csv") 
    
        
    return final_df