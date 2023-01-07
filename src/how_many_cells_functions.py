# ALL IMPORTS

import napari
import numpy as np
import pandas as pd
import tifffile
import skimage
import os
import glob
from scipy import ndimage as ndi
from tifffile import imread
from skimage import color
from skimage import data    
from skimage import morphology
from skimage.morphology import disk
from skimage.filters import median    
from skimage.filters import threshold_local
from skimage.measure import label, regionprops, regionprops_table



# SEGMENTATIONS

# 1. Long shape segmentation
# for the image path enter : image_path = project_path + "/Long shape" , don't forget the capital letter !!

def long_segmentation(image_path) :
    
    #opening the image
    image = tifffile.imread(image_path)
    
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(13)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 137)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh

    # binary dilation
    mask = morphology.binary_dilation(mask.astype(bool),morphology.disk(3))
    
    #closing the holes in the mask
    mask = morphology.remove_small_holes(mask.astype(bool), 1200)
    
   
    #post-processing : creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img



# 2. Puzzle shape segmentation
# for the image path enter : image_path = project_path + "/Puzzle shape", capital letter !

def puzzle_segmentation(image_path):
   
    #opening the image
    image = tifffile.imread(image_path)
    
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(10.0)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 149)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh

    #removing the noise from the mask
    #removing small objects
    mask = morphology.remove_small_objects(mask.astype(bool), 500)
    
    #closing the holes in the mask
    mask = morphology.remove_small_holes(mask.astype(bool), 500)
    
    #erosion and dilation
    mask = morphology.binary_opening(mask.astype(bool), morphology.disk(15))
   
    #post-processing : creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img



# 3. Half round/ long segmentation
# for the image path enter : image_path = project_path + "/Half shape", capital letter !

def half_segmentation(image_pathway):
   
    #opening the image
    image = tifffile.imread(image_pathway)
    
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(15)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 71)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh

    #removing the noise from the mask
    #binary dilation 
    mask = morphology.binary_dilation(mask.astype(bool),morphology.disk(4))
    
    #removing small objects
    mask = morphology.remove_small_objects(mask.astype(bool), 500)
    
    #closing the small holes in the mask
    mask = morphology.remove_small_holes(mask.astype(bool), 1500)
    
    #closing any hole in the mask 
    mask = ndi.binary_fill_holes(mask)
    
    #erosion and dilation
    mask = morphology.binary_opening(mask.astype(bool), morphology.disk(6))
   
    #post-processing : creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img



# 4. Croco shape segmentation
# for the image path enter : image_path = project_path + "/Croco shape", capital letter !

def croco_segmentation(image_pathway):
   
    #opening the image
    image = tifffile.imread(image_pathway)
    
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(10.0)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 13)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh
   
    # closing and opening
    mask = morphology.binary_closing(mask.astype(bool), morphology.disk(2))
    mask = morphology.binary_opening(mask.astype(bool), morphology.disk(2))
   
    #removing the noise (small objects) and filling the holes (remove small holes) in the mask
   
    mask = ndi.binary_fill_holes(mask)
    mask = morphology.remove_small_holes(mask.astype(bool), 200)
    mask = morphology.remove_small_objects(mask.astype(bool), 700)
   
    #creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img


# 5. Round shape segmentation
# for the image path enter : image_path = project_path + "/Round shape", capital letter !

def round_segmentation(image_pathway):
   
    #opening the image
    image = tifffile.imread(image_pathway)
   
    #pre-processing
    #changing the rgb image to a grayscale image
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(10.0)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 79)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh

    #removing the noise from the mask
    mask = morphology.remove_small_objects(mask.astype(bool), 500)
    
    #closing the holes in the mask
    mask = morphology.remove_small_holes(mask.astype(bool), 2000)
    
    # binary opening
    mask = morphology.binary_opening(mask.astype(bool), morphology.disk(10))
    
    # fill the holes
    mask = ndi.binary_fill_holes(mask)

   
    #creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img



# 6. 5.20 shape segmentation
# for the image path enter : image_path = project_path + "/5.20 shape", capital letter !

def five_segmentation(image_pathway):
   
    #opening the image
    image = tifffile.imread(image_pathway)
   
    #pre-processing
    img_gray = color.rgb2gray(image)
    
    #filter with a median filter
    footprint = disk(10.0)
    img_filter = skimage.filters.median(img_gray, footprint)

    #processing
    #computing a threshold with local_treshold
    thresh = threshold_local(img_filter, block_size = 37)
    
    #segmenting the image to create a mask
    mask = img_filter > thresh

    #dilation, erosion and opening
    mask = morphology.binary_dilation(mask.astype(bool), morphology.disk(4))
    mask = morphology.binary_erosion(mask.astype(bool), morphology.disk(6))
    mask = morphology.binary_opening(mask.astype(bool), morphology.disk(2))

    #fill holes, remove small holes and small objects (noise)
    mask = ndi.binary_fill_holes(mask)
    mask = morphology.remove_small_holes(mask.astype(bool), 10000)
    mask = morphology.remove_small_objects(mask.astype(bool), 1000)

    #creating the labels
    label_img = skimage.morphology.label(mask)
    
    return label_img



###


# CREATE MASKS 

# change the image path 6 categories corresponding to 6 segmentations
# the mask result path is the same, all masks go to the same folder

# 1. long shape masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/Long shape")

def save_long_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = long_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
   
    
    
# 2. puzzle shape masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/Puzzle shape")

def save_puzzle_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = puzzle_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
        
        
# 3. half round/long masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/Half shape")

def save_half_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = half_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
        
        
# 4. croco shape masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/Croco shape")

def save_croco_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = croco_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
        
        
# 5. round shape masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/Round shape")

def save_round_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = round_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
        
        
# 6. 5.20 shape masks
# image path for long shapes (ex : "/Users/camille/Documents/project plants/data/FDV_cell_database new/5_20 shape")

def save_five_mask(image_path,mask_result_path):
    
    for image in glob.glob(image_path +"*.tif"):  
        
        image_split = image.split("/")
        image_name = image_split[-1]
        label_img = five_segmentation(image)
        tifffile.imwrite(mask_result_path + "/" + image_name , label_img)
        
        

###





# COUNT CELLS

# the mask result path is the same for images from the 6 categories
# this function will be used in a loop in the last main function

def count_cells(mask_result_path, image_name):
    
    # get mask of image
    label_img = imread(mask_result_path + "/" + image_name)
    # create an array containing all the unique numbers of label_img, all the different cells
    label_cells = np.unique(label_img)
    
    # number of cells
    nb_cells = len(label_cells)
    
    return nb_cells


###




# CREATE CENTROID CSV

# this will loop on all the masks of all images

def centroids(mask_result_path, centroid_result_path):
    
    for mask_path in glob.glob(mask_result_path +"/*.tif"):
        
        image_split = mask_path.split("/")
        image_name = image_split[-1] 
        label_img = imread(mask_result_path + "/" + image_name)
    
        # create a table with the label associated to the cell and the coordinates of its centroid
        props = regionprops_table(label_img, properties=['label','centroid'])
    
        # transform into panda tabled
        df_props = pd.DataFrame(props)   
    
        # rename columns with the x and y coordinates
        df_props.columns = ['label', 'centroid-x', 'centroid-y']
    
        # create a csv of the table and store it in results/centroid_database
        df_props.to_csv((centroid_result_path + "/" + "cells_centroid" + image_name).replace(".tif", ".csv"), index=False)  
    
    return df_props



###


# FINAL CSV


# create three lists, add them to dict, create dataframe, turn df in csv
# this will loop on all the masks of all images
# source : https://www.geeksforgeeks.org/python-save-list-to-csv/


def nb_cells_centroid_csv(centroid_result_path, nb_cells_final_csv_path, mask_result_path):
    
    name_list = []
    nb_cells_list = []
    csv_list = []
    
    
    for mask_path in glob.glob(mask_result_path +"/*.tif"):  # this directory is the folder containing long shape cell                                        
        # reads the mask of the particular image of the loop
        label_img = imread(mask_path)
        image_split = mask_path.split("/")
        image_name = image_split[-1]  # get the image name, only the end of the mask_path
        
        # list with names of images
        name_list.append(image_name)
        
        # list with number of cells
        nb_cells = count_cells(mask_result_path, image_name)
        nb_cells_list.append(nb_cells)
        
        # list with centroid csv file names
        centroid_csv = ("cells_centroid" + image_name).replace(".tif", ".csv")
        csv_list.append(centroid_csv)

        # create dictionary
        dict = {'image name' : name_list, 'number of cells' : nb_cells_list, 'centroid csv' : csv_list}
    
        # create dataframe
        final_df = pd.DataFrame(dict)
        
    
        # create csv from dataframe, save it in the same folder as the centroids
        final_df.to_csv(centroid_result_path+"/number_cells_total.csv") # input "nb_cells_final_csv_path"
        
    return final_df

