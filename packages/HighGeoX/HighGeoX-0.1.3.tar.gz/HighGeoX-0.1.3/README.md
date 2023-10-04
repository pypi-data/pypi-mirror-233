# HighGeoX 

This is official documaentation of HighGeoX The package has many useful functions for dealing with geospatial data, also few functions like computation of NDVI(Natural Density Vegetation Index), MNDVI(Modified Natural Density Vegetation Index) are integrated with dask to speed up it's computation.

## Installation
This can installed using pip using the following command in both Windows and Linux OS

```
$ pip install HighGeoX
```
## Usage
### All Sorted File Names
The geospatial data file names are moslty represented by date and time. For few specific tasks like time series forecasting , it might be necessary to get all files in sequential form. This function returns list of all file names in sorted order.

**Function**
```
get_file_names(folder_path)
```

**Parameters**

1. _folder_path_: Folder path where geospatial Images exist

**Return Type**

Ordered name list of Geospatial Images
***
### Number of Bands
The functions finds number of bands in the image. Red, Green, Blue, Infrared etc.

**Function**
```
number_of_bands(filepath)
```
**Parameters**

1. _file path_: Path of Image.

**Return Type**

Integer value, number of bands.
***
### Numpy Array of the Image

The functions converts the file in numpy array format with all it's bands.

**Function**
```
numpy_image(filepath):
```
**Parameters**

1. _file path_: Path of Image.

**Return Type**

Numpy Array.
***

### Dataframe of the Image

Converts the geospatial file in pandas dataframe.

**Function**
```
dataframe_image(filepath)
```
**Parameters**

1. _file path_: Path of Image.

**Return Type**

Pandas dataframe.
***
### Min Max Scaling of Dataframe

This functions performs min-max scaling of the dataframe.

**Function**
```
min_max_scaled(df_raw)
```
**Parameters**

1. df_raw: Input pandas dataframe.

**Return Type**

Numpy array representing scaled values.
***

### Convert the numpy to dask array

This function converts numpy array to dask array with specified chunks of the same baMNDVIdth.

**Function**
```
numpy_to_dask_array(df,chunk_len)
```

**Parameters**

1. _df_: Input dataframe
2. _chunk_len_:specifies the chunk size 

**Return Type**

Dask array.
***
### One hot to label

Some of the geospatial data may be segmented (each pixel being classified to a label). Generally the open source labelled data is one hot encoded. This functions converts the it in labelled form. 

**Function**
```
one_hot_to_label(file_path)
```
**Parameters**

1. _file path_: Path of Image.

**Return Type**

Numpy array representing labelled data with only one band.
***
### Ordered labels 

Some of the labels of an image might not be following a sequential form. For eg there is bunch of images whose pixel labels are from 2,4, 7. To make it sequential this function would be helpful 

**Function**
```
get_ordered_labels(y)
```
**Parameters**

1. _y: Labelled numpy array.

**Return Type**

Ordered numpy array.
***
### Normalized difference

This is a key functions used for NDVI and MMNDVI indices. With specifying band values as Red and Near Red Infrared bands we can find NDVI index , and by specifying Short Wave Infrared and Green bands whe can get MMNDVI index for any geospatial image.

**Function**
```
normalized_difference( b1, b2):
```
***
### NDVI Computation (Returning list)

Functions here are used for finding NDVI indices of list of geospatial image 

#### Without Dask

**Function**
```
find_ndvi_list(file_path_list)
```
**Parameters**

1. _file path_list_: List of path of Images.

**Return Type**

List of NDVI index (numpy array) in the same order of values in input list.

---
#### With Dask
**Function**
```
find_ndvi_list_with_dask(worker_nodes,file_path_list)
```

**Parameters**

1. _file path_list_: List of path of Images.
2. worker_nodes: Number of dask worker nodes in a cluster

**Return Type**

List of NDVI index (numpy array) in the same order of values in input list.
***
### NDVI Computation (Saving the values in folder)
#### Without Dask
**Function**
```
find_and_write_ndvi_list(file_path_list,destination_folder)
```
**Parameters**

1. _file path_list_: List of path of Images.
2.  destination_folder: path where indices will be saved.

**Return Type**

 None

---
#### With Dask
**Function**
```
find_and_write_ndvi_list_with_dask(worker_nodes,file_path_list,destination_folder)
``` 
**Parameters**

1. _file path_list_: List of path of Images.
2. worker_nodes: Number of dask worker nodes in a cluster
3. destination_folder: path where indices will be saved.

**Return Type**

None

### MNDVI Computation (Returning list)

Functions here are used for finding MNDVI (Natural Density Water Index) indices of list of geospatial image 

#### Without Dask

**Function**
```
find_mndvi_list(file_path_list)
```
**Parameters**

1. _file path_list_: List of path of Images.

**Return Type**

List of MNDVI index (numpy array) in the same order of values in input list.

---
#### With Dask
**Function**
```
find_mndvi_list_with_dask(worker_nodes,file_path_list)
```

**Parameters**

1. _file path_list_: List of path of Images.
2. worker_nodes: Number of dask worker nodes in a cluster

**Return Type**

List of MNDVI index (numpy array) in the same order of values in input list.
***
### MNDVI Computation (Saving the values in folder)
#### Without Dask
**Function**
```
find_and_write_mndvi_list(file_path_list,destination_folder)
```
**Parameters**

1. _file path_list_: List of path of Images.
2.  destination_folder: path where indices will be saved.

**Return Type**

 None

---
#### With Dask
**Function**
```
find_and_write_mndvi_list_with_dask(worker_nodes,file_path_list,destination_folder)
``` 
**Parameters**

1. _file path_list_: List of path of Images.
2. worker_nodes: Number of dask worker nodes in a cluster
3. destination_folder: path where indices will be saved.

**Return Type**

None

## Contributing

The following are the core contributors:
1. Deeksha Agarwal
2. Pratyush Upadhyay

## License

`fasGeo` was created by IITB-SCL. It is licensed under the terms of the MIT license.



