import os
import numpy as np
import rasterio
import dask.dataframe as dd
import matplotlib.pyplot as plt
import dask
import pandas as pd
import dask.array as da
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from dask.distributed import Client, LocalCluster

def get_file_names(folder_path):
    input_images = os.listdir(folder_path)
    input_images.sort()
    return input_images

def numpy_image(filepath):
    img = rasterio.open(filepath)
    return img.read()

def number_of_bands(filepath):
    img = rasterio.open(filepath)
    return img.read().shape[0]


def dataframe_image(filepath):
    img = rasterio.open(filepath)
    len = img.read().shape[0]
    df = pd.DataFrame({})
    for i in range(1,len+1):
        c=img.read(i).flatten()
        df[str(i)] = c
    return df    

def min_max_scaled(df_raw):
    scaler = MinMaxScaler()
    scaler.fit(df_raw)
    df_normalized = scaler.transform(df_raw)
    return df_normalized

def numpy_to_dask_array(df,chunk_len):
    chunk_size = (chunk_len, df.shape[1])
    dask_input = da.from_array(df, chunks=chunk_size)
    return dask_input


def one_hot_to_label(file_path):
    one_hot_label = numpy_image(file_path)
    mask = np.zeros((one_hot_label.shape[1], one_hot_label.shape[2]), dtype=np.int32)
    num_classes = one_hot_label.shape[0]
    for i in range(num_classes):
        mask[one_hot_label[i, :, :] == 255] = i
    return mask.flatten()  


def get_ordered_labels(y):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    return y_encoded

def normalized_difference( b1, b2):
    band1 = np.where((b1==0) & (b2==0), np.nan, b1) 
    band2 = np.where((b1==0) & (b2==0), np.nan, b2)
    return (band1 - band2) / (band1 + band2)



def find_ndvi_store_in_list(filename):
    with rasterio.open(filename) as src:
        # read the red and NIR bands
        band_red = src.read(3)#extracting red band
        band_nir = src.read(4)#extracting infrared band
        ndvi = normalized_difference(band_nir, band_red)#ndvi calculation for a given file 
        #ndvi_list.append(ndvi) #appending ndvi index in the list 
        return ndvi
    

def find_ndvi_list(file_path_list):
    ndvi_list = []
    for i in file_path_list:
        ndvi = find_ndvi_store_in_list(i)
        ndvi_list.append(ndvi)
    return ndvi_list

#calculating nvdi index for a given file, and appending it to ndvi list
def find_mndvi_store_in_list(filename):
    with rasterio.open(filename) as src:
        # read the red and NIR bands
        band_green = src.read(2)#extracting green
        band_nir = src.read(4)#extracting infrared band
        mmndvi = normalized_difference(band_green, band_nir)#mmndvi calculation for a given file 
        return mmndvi


def find_mndvi_list(file_path_list):
    ndvi_list = []
    for i in file_path_list:
        mmndvi = find_mndvi_store_in_list(i)
        ndvi_list.append(mmndvi)
    return ndvi_list          

#calculating nvdi index for a given file, and creating .tif file for storing the nvdi index
#folder1 = "ndvi-images/"
def find_ndvi_write_in_file(source_path,destination_folder):
    with rasterio.open(source_path) as src:
        # read the red and NIR bands
        band_red = src.read(3)#extracting red 
        band_nir = src.read(4)#extracting infrared
        ndvi = normalized_difference(band_nir, band_red)#calling ndvi function
        # write NDVI index to file
        output_filename1 = destination_folder+'ndvi_' + source_path.split('/')[-1].split('\\')[-1]#creating output file path
        profile = src.profile.copy()
        profile.update(dtype=rasterio.float32, count=1, compress='lzw')
        with rasterio.open(output_filename1, 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)#writing back in .tif format  

# folder2 = "mmndvi-images/"
def find_mndvi_write_in_file(source_path,destination_folder):
    with rasterio.open(source_path) as src:
        # read the red and NIR bands
        band_green = src.read(2)#extracting green
        band_nir = src.read(4)#extracting infrared
        mmndvi = normalized_difference(band_green, band_nir)
        # write NDVI index to file
        output_filename2 = destination_folder+'mndvi_' + source_path.split('/')[-1].split('\\')[-1]#creating output file path
        profile = src.profile.copy()
        profile.update(dtype=rasterio.float32, count=1, compress='lzw')
        with rasterio.open(output_filename2, 'w', **profile) as dst:
            dst.write(mmndvi.astype(rasterio.float32), 1)#writing back in .tif format 

def find_ndvi_list_with_dask(worker_nodes,file_path_list):
    cluster = LocalCluster(n_workers=worker_nodes)
    client = Client(cluster)
    delayed_results = [dask.delayed(find_ndvi_store_in_list)(filename) for filename in file_path_list]#storing all dask delayed objects after applying the function in list 
    final_list = dask.compute(*delayed_results)#parallel computing of all dask delayed objects by worker 
    client.shutdown()
    client.close()
    cluster.close()
    return final_list

def find_mndvi_list_with_dask(worker_nodes,file_path_list):
    cluster = LocalCluster(n_workers=worker_nodes)
    client = Client(cluster)
    delayed_results = [dask.delayed(find_mndvi_store_in_list)(filename) for filename in file_path_list]#storing all dask delayed objects after applying the function in list 
    final_list = dask.compute(*delayed_results)#parallel computing of all dask delayed objects by worker 
    client.shutdown()
    client.close()
    cluster.close()
    return final_list

def find_and_write_ndvi_list(file_path_list,destination_folder):
    for i in file_path_list:
        find_ndvi_write_in_file(i,destination_folder)

def find_and_write_mndvi_list(file_path_list,destination_folder):
    for i in file_path_list:
        find_mndvi_write_in_file(i,destination_folder)

def find_and_write_ndvi_list_with_dask(worker_nodes,file_path_list,destination_folder):
    cluster = LocalCluster(n_workers=worker_nodes)#defining local cluster with number of worker nodes
    client = Client(cluster)
    delayed_results = [dask.delayed(find_ndvi_write_in_file)(filename,destination_folder) for filename in file_path_list]#storing all dask delayed objects after applying the function in list 
    dask.compute(*delayed_results)#simultanously process the dask delayed objects
    client.shutdown()
    client.close()
    cluster.close()
    
def find_and_write_mndvi_list_with_dask(worker_nodes,file_path_list,destination_folder):
    cluster = LocalCluster(n_workers=worker_nodes)#defining local cluster with number of worker nodes
    client = Client(cluster)
    delayed_results = [dask.delayed(find_mndvi_write_in_file)(filename,destination_folder) for filename in file_path_list]#storing all dask delayed objects after applying the function in list 
    dask.compute(*delayed_results)#simultanously process the dask delayed objects
    client.shutdown()
    client.close()
    cluster.close()                    