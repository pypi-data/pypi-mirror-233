
import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
import matplotlib.pyplot as plt
from rasterio.warp import reproject

import numpy as np

def resample_raster(src_array, src_transform, src_crs, dst_transform, dst_crs, dst_shape, resampling_method=rasterio.enums.Resampling.nearest):
    """
    Resample the source raster array to match the destination raster's resolution and extent.
    
    Parameters:
    - src_array: 2D numpy array of the source raster
    - src_transform: affine.Affine transform of the source raster
    - src_crs: CRS of the source raster
    - dst_transform: affine.Affine transform of the destination raster
    - dst_crs: CRS of the destination raster
    - dst_shape: Shape of the destination raster (height, width)
    - resampling_method: rasterio.enums.Resampling method to use for resampling
    
    Returns:
    - resampled_array: 2D numpy array of the resampled source raster
    """
    
    # Create an empty array with the destination shape
    resampled_array = np.empty(dst_shape, np.float32)
    
    # Define the source and destination transformations and arrays for reproject
    reproject(
        source=src_array,
        destination=resampled_array,
        src_transform=src_transform,
        src_crs=src_crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=resampling_method
    )

    return resampled_array



def scatter_area_mask(input_folder, output_folder, plot_folder, shapefile_path, scatter_Area_threshold=1.1, vegetation_mask_path=None):
    """
    Create an accumulated scatter area mask from a set of raster images based on a given threshold. the input dataset is taken from ASF RTC processing.
    The scattering area for each pixel in the RTC image in square meters. The values are calculated based on the effectively illuminated gamma-0 terrain surface using a digital elevation model, 
    the local incidence angle map, and the layover-shadow map. see detailes at the following website https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/#scattering-area-map

    The function processes each raster image in the input folder, crops it based on the provided AOI
    from the shapefile, normalizes the cropped raster, and then converts the normalized image to a binary
    mask based on the scatter_percentageArea_threshold. The binary masks from each raster are then accumulated
    to generate the final scatter area mask.

    Parameters:
    -----------
    input_folder : str
        Path to the folder containing raster files to be processed.
    
    output_folder : str
        Directory where the final accumulated mask raster file will be saved.
    
    plot_folder : str
        Directory where the visual representation (plot) of the accumulated mask will be saved.
    
    shapefile_path : str
        Path to the shapefile containing the Area of Interest (AOI) for cropping the raster images.
    
    scatter_Area_threshold : float, optional (default=1.1) unit is meter square
        Threshold for determining the binary mask from the normalized raster image. Pixels with values 
        less than this threshold are set to 0 and those above are set to 1.

    Returns:
    --------
    Shadow Mask for SAR image for sites less likey to have quality measurment points.
    The results are saved as files in the specified output and plot directories.

    Notes:
    ------
    - Assumes that there is only one geometry in the provided shapefile.
    - The accumulated mask is a result of multiplying binary masks from each raster. Therefore, a pixel in 
      the accumulated mask will have a value of 1 only if all rasters have a value of 1 at that pixel location.
    """
    
    # Ensure the output and plot folders exist
    for folder in [output_folder, plot_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Read the AOI from the shapefile
    aoi_gdf = gpd.read_file(shapefile_path)
    geometry = aoi_gdf.geometry[0]  # Assuming only one geometry in the shapefile

    accumulated_mask = None  # This will store the final aggregated mask

    # Process each raster
    for filename in os.listdir(input_folder):
        if filename.endswith(".tif"):
            input_path = os.path.join(input_folder, filename)
            
            with rasterio.open(input_path) as src:
                # Crop raster based on AOI
                cropped_image, cropped_transform = mask(src, [geometry], crop=True)
                cropped_image = cropped_image[0]  # As it returns in (bands, row, col) format
                
                # # Normalize the image
                # min_val = np.min(cropped_image)
                # max_val = np.max(cropped_image)
                
                # print('min: ', min_val)
                # print('max: ' , max_val)
                # normalized_image = (cropped_image - min_val) / (max_val - min_val)
                
                # Convert the normalized image to binary
                
                binary_image = np.where(cropped_image < scatter_Area_threshold, 1, 0).astype(rasterio.uint8)

                # Accumulate the mask
                if accumulated_mask is None:
                    accumulated_mask = binary_image
                else:
                    accumulated_mask *= binary_image

    # Save the final accumulated mask
    meta = src.meta.copy()
    meta.update({
        'dtype': rasterio.uint8,
        'height': accumulated_mask.shape[0],
        'width': accumulated_mask.shape[1],
        'transform': cropped_transform
    })

    if vegetation_mask_path is not None:
        with rasterio.open(vegetation_mask_path) as src:
            vegi_mask = src.read(1)
            vegi_mask = np.where(vegi_mask < 1, 0, 1).astype(rasterio.uint8)
            vegi_transform = src.transform
            vegi_crs = src.crs

        # Resample vegi_mask to match accumulated_mask
        resampled_vegi_mask = resample_raster(
            src_array=vegi_mask,
            src_transform=vegi_transform,
            src_crs=vegi_crs,
            dst_transform=cropped_transform,  # This should be the transform of accumulated_mask
            dst_crs=meta['crs'],  # This should be the CRS of accumulated_mask
            dst_shape=accumulated_mask.shape
        )

        combined_mask=resampled_vegi_mask+accumulated_mask
        combined_mask = np.where(combined_mask > 1, 1, 0).astype(rasterio.uint8)
        accumulated_mask = combined_mask
        
        # Plot and save the final accumulated mask
        plt.colorbar(plt.imshow(accumulated_mask, cmap='gray'))
        plt.axis('off')
        plt.savefig(os.path.join(plot_folder, "SAR_scatterArea_Vegetation_masks.png"), dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        
        
        with rasterio.open(os.path.join(output_folder, "SAR_scatterArea_Vegetation_masks.tif"), 'w', **meta) as dest:
            dest.write(accumulated_mask, 1)
    else:
        with rasterio.open(os.path.join(output_folder, "SAR_scatterArea_mask.tif"), 'w', **meta) as dest:
            dest.write(accumulated_mask, 1)

        # Plot and save the final accumulated mask
        plt.colorbar( plt.imshow(accumulated_mask, cmap='gray'))
        plt.axis('off')
        plt.savefig(os.path.join(plot_folder, "SAR_scatterArea_mask.png"), dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()
        


def utm_to_latlon(easting, northing, zone_number, zone_letter):
    '''
    This program converts geographic projection of shapefiles from UTM to LATLONG
    
    Parameters
    ----------
    easting: Geopandas column with Easting 
    
    northing: Geopandas column with Northing
    
    zone_number: int
    
    zone_letter: "N" or "S"
    
    Returns
    -------
    [lon , lat ]: List

    '''
    import geopandas as gpd
    import utm
    easting = easting
    northing = northing
    lon, lat=utm.to_latlon(easting, northing, zone_number, zone_letter)
    
    return [lon, lat]

import os

import numpy as np
import rasterio
from osgeo import gdal, osr
from rasterio.transform import Affine


def flip_geotiff_180(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        # Only process files with the .tif extension
        if filename.endswith(".tif"):
            filepath = os.path.join(directory, filename)

            # Open the file
            with rasterio.open(filepath) as src:
                # Read the image data
                data = src.read()
                # Define the transform
                transform = src.transform

            # Flip the data array upside down (180 degree rotation)
            data = np.flipud(data)

            # Update the transform
            transform = Affine(transform.a, transform.b, transform.c, transform.d, -transform.e, src.height * transform.e + transform.f)

            # Write the data to the same file, overwriting the original
            with rasterio.open(filepath, 'w', driver='GTiff', height=data.shape[1], width=data.shape[2], count=data.shape[0], dtype=data.dtype, crs=src.crs, transform=transform) as dst:
                dst.write(data)


def assign_fake_projection(input_dir, output_dir):
    '''
    Note
    ====

    This program assigns fake latlon geographic coordinates to ground-based images 
    so that it can be ingest using gdal and rasterio geospatial libraries for further processing
    
    input_dir: str
        path to image directories without projection info
    
    output_dir: str
        output path image directory for images included projection info

    
    '''
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List of valid extensions
    valid_extensions = ['.tif', '.jpg', '.png', '.bmp']

    # # Create a "fake" Spatial Reference object for source
    # source_srs = osr.SpatialReference()
    # source_srs.SetWellKnownGeogCS('LOCAL_CS')  # 'LOCAL_CS' is a placeholder coordinate system
    # Create a Spatial Reference object for source
    # source_srs = osr.SpatialReference()
    # source_srs.SetWellKnownGeogCS('LOCAL_CS')
    #source_srs.SetWellKnownGeogCS('WGS84')  # WGS84 is a commonly used geodetic coordinate system

    #######

    # Create a SpatialReference object
    source_srs = osr.SpatialReference()

    # Set the UTM Zone 10N coordinate system
    source_srs.SetUTM(10, 1)  # Zone 10, Northern Hemisphere


    ########
    from scipy import ndimage

    # Iterate over all files in the directory
    for filename in os.listdir(input_dir):
        # Check if the file has a valid extension
        if os.path.splitext(filename)[1] in valid_extensions:
            # Define the full path to the input raster
            input_raster_path = os.path.join(input_dir, filename)

            # Open the raster
            ds = gdal.Open(input_raster_path, gdal.GA_ReadOnly)

            # Read the raster data
            data = ds.ReadAsArray()

            # Rotate array by 45 degrees
            #data = ndimage.rotate(data, 180)

            # Define the full path to the output raster
            # We keep the original filename but put it into the output_dir
            output_raster_path = os.path.join(output_dir, filename[:-4]+".tif")

            # Create a new raster dataset with the same dimensions
            driver = gdal.GetDriverByName('GTiff')
            out_ds = driver.Create(output_raster_path, ds.RasterXSize, ds.RasterYSize, ds.RasterCount, ds.GetRasterBand(1).DataType)

            # Assign the "fake" projection and the same geotransform
            out_ds.SetProjection(source_srs.ExportToWkt())
            out_ds.SetGeoTransform(ds.GetGeoTransform())

             # Assign the WGS84 projection and the same geotransform
            out_ds.SetProjection(source_srs.ExportToWkt())
            out_ds.SetGeoTransform(ds.GetGeoTransform())

            # Write the data to the new raster
            for i in range(ds.RasterCount):
                out_band = out_ds.GetRasterBand(i+1)
                out_band.WriteArray(data[i])

            # Close the datasets
            ds = None
            out_ds = None
    for filename in os.listdir(output_dir):
        # Only process files with the .tif extension
        if filename.endswith(".tif"):
            filepath = os.path.join(output_dir, filename)

            # Open the file
            with rasterio.open(filepath) as src:
                # Read the image data
                data = src.read()
                # Define the transform
                transform = src.transform

            # Flip the data array upside down (180 degree rotation)
            data = np.flipud(data)

            # Update the transform
            transform = Affine(transform.a, transform.b, transform.c, transform.d, -transform.e, src.height * transform.e + transform.f)

            # Write the data to the same file, overwriting the original
            with rasterio.open(filepath, 'w', driver='GTiff', height=data.shape[1], width=data.shape[2], count=data.shape[0], dtype=data.dtype, crs=src.crs, transform=transform) as dst:
                dst.write(data)  
import os
import re
import shutil


def move_files(base_directory):
    """
    This function reorganizes files in the specified directory. 
    It searches for timestamps in filenames, creates subdirectories based on the hour part of the timestamp,
    and moves files to the appropriate subdirectories. The files are renamed based on the year, month, and day of the timestamp.
    
    Args:
        base_directory (str): Path of the directory containing the files to be reorganized.

    """

    # List of regex patterns for different timestamp formats
    timestamp_patterns = [
        r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})\.',  # yyyymmddhhmmss
        r'(?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})\.',  # yymmddhh
        r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.',  # yyyymmdd
        r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})\.',  # hhmmss
        r'(?P<hour>\d{2})\.'  # hh
        # Add more patterns as necessary
    ]

    for filename in os.listdir(base_directory):
        # If the file is not a file, skip
        if not os.path.isfile(os.path.join(base_directory, filename)):
            continue

        # Extract the timestamp from the filename
        for pattern in timestamp_patterns:
            match = re.search(pattern, filename)
            if match:
                year = match.groupdict().get('year', '0000')
                month = match.groupdict().get('month', '00')
                day = match.groupdict().get('day', '00')
                hour = match.group('hour')
                break
        else:
            print(f"No timestamp found in file {filename}.")
            continue

        # Construct new filename based on date and existing extension
        base, extension = os.path.splitext(filename)
        new_filename = f"{year}-{month}-{day}{extension}"

        # Make directory for this hour if it doesn't exist
        hour_dir = os.path.join(base_directory, hour)
        if not os.path.exists(hour_dir):
            os.makedirs(hour_dir)

        # Move and rename file to the corresponding hour folder
        shutil.move(os.path.join(base_directory, filename), os.path.join(hour_dir, new_filename))



from tensorflow.keras import backend as K
from tensorflow.keras.layers import (Activation, Conv2D, Dense, Flatten,
                                     MaxPooling2D)
from tensorflow.keras.models import Sequential


class LeNet:
    @staticmethod
    def build(width, height, depth, classes):
        # initialize the model
        model = Sequential()
        inputShape = (height, width, depth)

        # if we are using "channels first", update the input shape
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)

        # first set of CONV => RELU => POOL layers
        model.add(Conv2D(20, (5, 5), padding="same",
            input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model

def Lenet_Model_training(dataset="DataForTraining", model_out="foggy_not_foggy.model", plot="Model_stat_plot.png", EPOCHS = 100,
    INIT_LR = 1e-3,  BS = 32):

    '''

    This function, Lenet_Model_train(), is designed to train a convolutional neural network (CNN) using the LeNet architecture. The network is trained on a dataset of images to classify whether they are "foggy" or "not foggy".

    Parameters:
    -----------

    dataset: str
      (default="DataForTraining") Path to the directory containing the image data for training. The images are expected to be in separate directories named after their corresponding class ("foggy" or "not foggy").
    model_out: str
      (default="foggy_not_foggy.model") The name or path for the output file where the trained model will be saved in the h5 format.
    plot: str
     (default="Model_stat_plot.png") The name or path for the output image file where a plot of the training loss and accuracy will be saved.
    EPOCHS: int
      (default=100)The number of epochs to use for training.
    INIT_LR: float
      (default=1e-3)The initial learning rate for the Adam optimizer.
    BS: int
      (default=32)The batch size for training.

    Returns:
    --------
    - Trains a LeNet model on the given dataset.
    - Saves the trained model to disk in the h5 format.
    - Plots the training and validation loss and accuracy as a function of epoch number, and saves the plot to disk. The plot also includes the model summary.
    - Note: The function uses data augmentation techniques during training, including random rotations, width and height shifts, shearing, zooming, and horizontal flipping.
    - This function uses the TensorFlow, Keras, OpenCV, and matplotlib libraries.

    '''
            
    import argparse
    import os
    import random

    import cv2
    import matplotlib.pyplot as plt
    import numpy as np
    from imutils import paths
    from sklearn.model_selection import train_test_split
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.preprocessing.image import (ImageDataGenerator,
                                                      img_to_array)
    from tensorflow.keras.utils import to_categorical

    #from mahmud_ml.lenet import LeNet

    

    dataset=dataset
    model=model_out
    plot=plot
    

    # initialize the number of epochs to train for, initial learning rate, and batch size
    EPOCHS = EPOCHS
    INIT_LR = INIT_LR
    BS = BS

    # initialize the data and labels
    print("[INFO] loading images...")
    data = []
    labels = []

    # grab the image paths and randomly shuffle
    imagePaths = sorted(list(paths.list_images(dataset)))
    random.seed(42)
    random.shuffle(imagePaths)

    # loop over the input images
    for imagePath in imagePaths:
        # load the image, pre-process it, and store it in the data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (28, 28))
        image = img_to_array(image)
        data.append(image)

        # extract the class label from the image path and update the labels list
        label = imagePath.split(os.path.sep)[-2]
        label = 1 if label == "foggy" else 0
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # partition the data into training and testing splits using 75% of the data for training and the remaining 25% for testing
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)

    # convert the labels from integers to vectors
    trainY = to_categorical(trainY, num_classes=2)
    testY = to_categorical(testY, num_classes=2)

    # construct the image generator for data augmentation
    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")

    # initialize the model
    print("[INFO] compiling model...")
    model = LeNet.build(width=28, height=28, depth=3, classes=2)
    opt = Adam(learning_rate=INIT_LR)
    model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

    # train the network
    print("[INFO] training network...")
    H = model.fit(x=aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS, epochs=EPOCHS, verbose=1)

    # save the model to disk
    print("[INFO] serializing network...")
    model.save(model_out, save_format="h5")

    #############

    from tensorflow.keras.models import load_model

    # Load the model
    model = load_model(model_out)

    # # Print model summary
    # print("\nModel Summary:")
    #model.summary()

    import io
    import re

    import matplotlib.pyplot as plt

    # Save the summary to a string
    stream = io.StringIO()
    model.summary(print_fn=lambda x: stream.write(x + '\n'))
    summary_string = stream.getvalue()
    stream.close()

    # Preprocess the string to remove unwanted characters
    summary_string = re.sub('_+', '', summary_string)
    summary_string = re.sub('=+', '', summary_string)


    ###############

    # plot the training loss and accuracy
    plt.style.use("ggplot")
    plt.figure(figsize=(15,5))
    N = EPOCHS
    plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy on fog/Not fog")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")


    # Add the summary string as a textbox
    # Add text to figure with a bounding box
    bbox_props = dict(boxstyle="round, pad=0.3", fc="white", ec="k", lw=2, alpha=0.6)
    plt.figtext(0.75, 0.5, summary_string, horizontalalignment='left', verticalalignment='center', fontsize=6, bbox=bbox_props)

    plt.tight_layout()

    plt.savefig(plot)

    plt.show()


from os import listdir, makedirs
from os.path import isdir, isfile, join

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tqdm import tqdm


def classification(input_dir="dataset_imagery", trained_model="foggy_not_foggy.model"):
    """
    Classifies images in the specified directory using a trained model.

    Inputs:
    -------
        - input_dir (str, optional): Path to the directory containing the input images. Defaults to "dataset_imagery".
        - trained_model (str, optional): Path to the trained model file. Defaults to "foggy_not_foggy.model".

    

    Returns:
    --------
        - The function assumes that the input directory contains image files in JPG format.
        - The function uses a trained convolutional neural network model to classify the images.
        - It saves the classified images into separate directories based on their classification.

    
    """
    # Setting required file directories
    dir_list = ['filtered_images_noFog', 'filtered_images_Fog', 'ClearImages_daily']
    for directory in dir_list:
        if not isdir(directory):
            try:
                makedirs(directory)
            except OSError as e:
                raise OSError(f"Error creating directory '{directory}': {e}")

    No_Fogg_path = "filtered_images_noFog"
    Foggy_Path = "filtered_images_Fog"
    dailyimages = "ClearImages_daily"
    mypath = input_dir

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = np.empty(len(onlyfiles), dtype=object)

    # Load the trained convolutional neural network outside of loop
    model = load_model(trained_model)

    # Loop through each image and use tqdm for progress bar
    pbar = tqdm(range(len(onlyfiles)), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', colour='#00ff00', dynamic_ncols=True)

    for n in pbar:
        pbar.set_description(f"Processing image {n + 1}")
        image_path = join(mypath, onlyfiles[n])

        image = cv2.imread(image_path)
        orig = image.copy()

        # Pre-process the image for classification
        image = cv2.resize(image, (28, 28))
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = image.astype("float") / 255.0

        # Classify the input image
        (not_foggy, foggy) = model.predict(image)[0]
        label = "NotFoggy" if not_foggy > foggy else "Foggy"
        proba = not_foggy if not_foggy > foggy else foggy
        label = f"{label}: {proba * 100:.2f}%"

        cv2.putText(orig, label, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        im = Image.fromarray(orig)

        file = str(onlyfiles[n])
        position = file.index(".jpg")
        filename = file[:position]

        if proba > 0.95 and not_foggy > foggy:
            label = "Not Foggy"
            im.save(join(No_Fogg_path, f"{proba}-{filename}.jpg"))
            im.save(join(dailyimages, f"{filename}.jpg"))
        else:
            label = "Foggy"
            im.save(join(Foggy_Path, f"{proba}-{filename}.jpg"))

    print("\nNo more files left to process")  # Print final message on a new line


import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.transform import Affine


def calculate_volume(elevation_map, slope_map, cell_size, output_file, plot_map=False, plot_file=None):
    """
    Calculate the volume based on an elevation map and a slope map,
    and save the volume map as a GeoTIFF file. Optionally, plot the volume map as a figure and save it.

    Args:
        elevation_map (str): File path to the elevation map raster.
        slope_map (ndarray): 2D array representing the slope values.
        cell_size (float): Size of each cell in the map (e.g., length of one side of a square cell).
        output_file (str): Output file path for saving the volume map as a GeoTIFF.
        plot_map (bool, optional): Whether to plot the volume map as a figure. Default is False.
        plot_file (str, optional): Output file path for saving the volume map plot. Required if plot_map is True.

    Returns:
        ndarray: The calculated volume map.

    """
    # Read elevation map raster using rasterio
    src= rasterio.open(elevation_map)
    # Get CRS from elevation_map
    crs = src.crs

    # Get transform from elevation_map
    transform = src.transform

     # Read elevation map data
    elevation_data = src.read(1)

     # Read elevation map raster using rasterio
    src1= rasterio.open(slope_map)
        
     # Read slope_map data
    slope_data = src.read(1)

    # Calculate the dimensions of the maps
    rows, cols = elevation_data.shape

    # Initialize the volume map
    volume_map = np.zeros_like(elevation_data, dtype=float)

    # Iterate over each cell in the maps
    for i in range(rows):
        for j in range(cols):
            # Calculate the cell area
            area = cell_size ** 2

            # Calculate the cell volume contribution
            volume_map[i, j] += elevation_data[i, j] * area

            # Calculate the slope gradient
            slope_gradient = np.tan(np.radians(slope_data[i, j]))

            # Calculate the additional volume due to the slope
            volume_map[i, j] += 0.5 * slope_gradient * area

    # Save volume map as GeoTIFF
    with rasterio.open(output_file, "w", driver="GTiff", height=volume_map.shape[0], width=volume_map.shape[1], count=1, dtype=volume_map.dtype, crs=crs, transform=transform) as dst:
        dst.write(volume_map, 1)

    # Plot and save volume map if desired
    if plot_map:
        plt.imshow(volume_map, cmap='viridis')
        plt.colorbar(label='Volume')
        plt.title('Volume Map')
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.tight_layout()
        plt.savefig(plot_file)
        plt.show()

    return volume_map




# def ts_plot(df, plot_number, save_plot=False , output_dir="", plot_filename="" , VEL_Scale='year'):


#     import plotly.graph_objects as go
#     import plotly.express as px
#     import plotly.express as px_temp
#     import pandas as pd
#     import numpy as np
#     import matplotlib.pyplot as plt
#     import geopandas as gpd 
#     import pandas as pd  
#     import seaborn as sns  
#     import plotly.offline as py_offline
#     import os   
#     import statsmodels.api as sm
#     from sklearn.metrics import mean_squared_error, r2_score
#     import numpy as np
#     from sklearn.linear_model import LinearRegression
#     from datetime import datetime
#     import math
    
#     py_offline.init_notebook_mode()
#     #%matplotlib widget
#     #df=pd.read_csv("temp.csv")
#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y%m%d')
    
#     df=df.set_index('dd')
    
#     ########################
#     df=df.dropna()
#     # Make index pd.DatetimeIndex
#     df.index = pd.DatetimeIndex(df.index)
#     # Make new index
#     idx = pd.date_range(df.index.min(), df.index.max())
#     # Replace original index with idx
#     df = df.reindex(index = idx)
#     # Insert row count
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())

#     df=df.dropna()
    
#     #df=df.set_index(df['row_count'], inplace=True)

#     df.sort_index(ascending=True, inplace=True)
    

#     def best_fit_slope_and_intercept(xs,ys):
#         from statistics import mean
#         xs = np.array(xs, dtype=np.float64)
#         ys = np.array(ys, dtype=np.float64)
#         m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
#             ((mean(xs)*mean(xs)) - mean(xs*xs)))
        
#         b = mean(ys) - m*mean(xs)
        
#         return m, b

    

#     #convert dattime to number of days per year
    
    
    

#     dates_list=([datetime.strptime(x, '%Y%m%d') for x in df.dd_str])
#     days_num=[( ((x) - (pd.Timestamp(year=x.year, month=1, day=1))).days + 1) for x in dates_list]
#     time2=days_num[len(days_num)-1]
#     time1=days_num[0]
#     delta=time2-time1
#     delta=float(delta)
#     print(days_num, delta)
    
#     m, b = best_fit_slope_and_intercept(df.row_count, df.val)
#     print("m:", math.ceil(m*100)/100, "b:",math.ceil(b*100)/100)
#     regression_model = LinearRegression()
#     val_dates_res = regression_model.fit(np.array(days_num).reshape(-1,1), np.array(df.val))
#     y_predicted = regression_model.predict(np.array(days_num).reshape(-1,1))
    
#     if VEL_Scale=='year':
#         rate_change=regression_model.coef_[0]/delta * 365.0
#     elif VEL_Scale=='month':
#         rate_change=regression_model.coef_[0]/delta * 30
        
#     # model evaluation
#     mse=mean_squared_error(np.array(df.val),y_predicted)
#     rmse = np.sqrt(mean_squared_error(np.array(df.val), y_predicted))
#     r2 = r2_score(np.array(df.val), y_predicted)
    
#     # printing values
#     print('Slope(linear deformation rate):' + str(math.ceil(regression_model.coef_[0]*100)/100/delta) + " mm/day")
#     print('Intercept:', math.ceil(b*100)/100)
#     #print('MSE:',mse)
#     print('Root mean squared error: ', math.ceil(rmse*100)/100)
#     print('R2 score: ', r2)
#     print("STD: ",math.ceil(np.std(y_predicted)*100)/100) 
#     # Create figure
#     #fig = go.Figure()
    
#     fig = go.FigureWidget()
    
#     plot_number="Plot Number:"+str(plot_number)

#     fig.add_trace(go.Scatter(x=list(df.index), y=list(df.val)))
#     fig = px.scatter(df, x=list(df.index), y=list(df.val),
#                 color="val", hover_name="val"
#                     , labels=dict(x="Dates", y="mm/"+VEL_Scale , color="mm/"+VEL_Scale))
    
#     # fig.add_trace(
#     # go.Scatter(x=list(df.index), y=list(val_fit), mode = "lines",name="trendline", marker_color = "red"))
    
    
    
#     fig.add_trace(go.Scatter(x=list(df.index), y=list(df.val),mode = 'lines',
#                             name = 'draw lines', line = dict(shape = 'linear', color = 'rgb(0, 0, 0)', dash = 'dash'), connectgaps = True))
    
#     fig.add_trace(
#         go.Scatter(x=list(df.index), y=list(y_predicted), mode = "lines",name="trendline", marker_color = "black", line_color='red'))
    
    

#     # Add range slider
#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=1,
#                         label="1m",
#                         step="month",
#                         stepmode="backward"),
#                     dict(count=6,
#                         label="6m",
#                         step="month",
#                         stepmode="backward"),
#                     dict(count=1,
#                         label="YTD",
#                         step="year",
#                         stepmode="todate"),
#                     dict(count=1,
#                         label="1y",
#                         step="year",
#                         stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             rangeslider=dict(
#                 visible=True
#             ),
#             type="date"
#         ) 
#     )
#     fig.update_xaxes(rangeslider_thickness = 0.05)
#     #fig.update_layout(showlegend=True)

#     #fig.data[0].update(line_color='black')
#     tt= "Defo-Rate:"+str(round(rate_change,2))+":"+ "Defo-Rate-STD:"+str(round(np.std(y_predicted), 2))+ ":" +plot_number
    
#     # make space for explanation / annotation
#     fig.update_layout(margin=dict(l=20, r=20, t=20, b=60),paper_bgcolor="LightSteelBlue")

    
#     fig.update_layout(
        
#     title_text=tt, title_font_family="Sitka Small",
#     title_font_color="red", title_x=0.5 , legend_title="Legend",
#     font=dict(
#         family="Courier New, monospace",
#         size=15,
#         color="RebeccaPurple" ))
    
#     fig.update_layout(legend=dict(
#     yanchor="top",
#     y=-0,
#     xanchor="left",
#     x=1.01
# ))

#     # fig.update_layout(
#     # updatemenus=[
#     #     dict(
#     #         type="buttons",
#     #         direction="right",
#     #         active=0,
#     #         x=0.57,
#     #         y=1.2,
#     #         buttons=list([
#     #             dict(
#     #                 args=["colorscale", "Viridis"],
#     #                 label="Viridis",
#     #                 method="restyle"
#     #             ),
#     #             dict(
#     #                 args=["colorscale", "turbo"],
#     #                 label="turbo",
#     #                 method="restyle"
#     #             )
#     #         ]),
#     #     )
#     # ])

    
#     fig.update_xaxes(showspikes=True, spikemode='toaxis' , spikesnap='cursor', spikedash='dot', spikecolor='blue', scaleanchor='y', title_font_family="Arial", 
#                     title_font=dict(size=15))
#     fig.update_yaxes(showspikes=True, spikemode='toaxis' , spikesnap='cursor', spikedash='dot', spikecolor='blue', scaleanchor='x', title_font_family="Arial",
#                     title_font=dict(size=15))

    
    
#     if save_plot==True:
    
#         if not os.path.exists(output_dir):
#             os.mkdir(output_dir)

#         fig.write_html(output_dir + "/" + plot_filename + ".html" )
#         fig.write_image(output_dir + "/" + plot_filename + ".jpeg", scale=1, width=1080, height=300 )
        
    
#     def zoom(layout, xrange):
#         in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
#         fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

#     fig.layout.on_change(zoom, 'xaxis.range')
    
#     fig.show()
    
    




    
#     start=int(start.timestamp() * 1000)
#     end=int(end.timestamp() * 1000)

#     #df=pd.read_csv('temp2.csv')
    
#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y-%m-%d')
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())
#     #df=df.set_index('dd')
#     #df.index = pd.DatetimeIndex(df.index)
#     df.dd_str = pd.DatetimeIndex(df.dd_str)
#     df['dd_int'] = [int(i.timestamp()*1000) for i in df.dd_str]
#     import numpy as np 
#     def find_nearest(array, value):
#         array = np.asarray(array)
#         idx = (np.abs(array - value)).argmin()
#         return array[idx]
#     s=find_nearest(np.array(df.dd_int), start)
#     e=find_nearest(np.array(df.dd_int), end)

#     s=(df[df['dd_int']==s].index)
#     e=(df[df['dd_int']==e].index)

#     df_filter=df[s[0]:e[0]]
#     print(df_filter)

#     df=df_filter  
    
# import pandas as pd
# import ipywidgets as widgets
# from IPython.display import display

# class DateRangePicker(object):
#     def __init__(self,start,end,freq='D',fmt='%Y-%m-%d'):
#         """
#         Parameters
#         ----------
#         start : string or datetime-like
#             Left bound of the period
#         end : string or datetime-like
#             Left bound of the period
#         freq : string or pandas.DateOffset, default='D'
#             Frequency strings can have multiples, e.g. '5H' 
#         fmt : string, defauly = '%Y-%m-%d'
#             Format to use to display the selected period

#         """
#         self.date_range=pd.date_range(start=start,end=end,freq=freq)
#         options = [(item.strftime(fmt),item) for item in self.date_range]
#         self.slider_start = widgets.SelectionSlider(
#             description='start',
#             options=options,
#             continuous_update=False
#         )
#         self.slider_end = widgets.SelectionSlider(
#             description='end',
#             options=options,
#             continuous_update=False,
#             value=options[-1][1]
#         )

#         self.slider_start.on_trait_change(self.slider_start_changed, 'value')
#         self.slider_end.on_trait_change(self.slider_end_changed, 'value')

#         self.widget = widgets.Box(children=[self.slider_start,self.slider_end])

#     def slider_start_changed(self,key,value):
#         self.slider_end.value=max(self.slider_start.value,self.slider_end.value)
#         self._observe(start=self.slider_start.value,end=self.slider_end.value)

#     def slider_end_changed(self,key,value):
#         self.slider_start.value=min(self.slider_start.value,self.slider_end.value)
#         self._observe(start=self.slider_start.value,end=self.slider_end.value)

#     def display(self):
#         display(self.slider_start,self.slider_end)

#     def _observe(self,**kwargs):
#         if hasattr(self,'observe'):
#             self.observe(**kwargs)

# def fct(start,end):
#     print (start,end)
    
#     start=int(start.timestamp() * 1000)
#     end=int(end.timestamp() * 1000)

#     df=pd.read_csv('temp2.csv')

#     df.rename(columns={ df.columns[0]: "dd" }, inplace = True)
#     df['dd_str']=df['dd'].astype(str)
#     df['dd_str'] = df['dd_str'].astype(str)
#     df.rename(columns={ df.columns[1]: "val" }, inplace = True)
#     df['dd']= pd.to_datetime(df['dd'].astype(str), format='%Y-%m-%d')
#     df.insert(df.shape[1],
#             'row_count',
#             df.index.value_counts().sort_index().cumsum())
#     #df=df.set_index('dd')
#     #df.index = pd.DatetimeIndex(df.index)
#     df.dd_str = pd.DatetimeIndex(df.dd_str)
#     df['dd_int'] = [int(i.timestamp()*1000) for i in df.dd_str]
#     import numpy as np 
#     def find_nearest(array, value):
#         array = np.asarray(array)
#         idx = (np.abs(array - value)).argmin()
#         return array[idx]
#     s=find_nearest(np.array(df.dd_int), start)
#     e=find_nearest(np.array(df.dd_int), end)

#     s=(df[df['dd_int']==s].index)
#     e=(df[df['dd_int']==e].index)

#     df_filter=df[s[0]:e[0]]
#     print(df_filter)
#     return (start, end)
    
# w=DateRangePicker(start='2022-08-02',end="2022-09-02",freq='D',fmt='%Y-%m-%d')
# w.observe=fct
# w.display()

# #a=fct[0]
# print(w.observe[0])

############################################################


def akhdefo_fitPlane(dem_data='', line_shapefile=None , out_planeFolder='Planes_out'):
    """
    Fit planes to points in a Digital Elevation Model (DEM) and visualize the results.

    Parameters:
        - dem_data (str): Path to the DEM data file (GeoTIFF format).
        - line_shapefile (str): Path to the shapefile containing line features representing planes.
        - out_planeFolder (str): Path to the folder where the output plane data will be saved.

    How It Works:
        This function reads a DEM and shapefile, allows the user to interactively select points from the DEM,
        fits planes to the selected points, and visualizes the results in 2D and 3D plots. It also provides options
        to save the fitted planes as XYZ and DXF files. additionally plots poles to planes on polar grid and rose diagram for strike/trends of planes

    Note:
        - The function utilizes various libraries such as numpy, matplotlib, tkinter, osgeo (GDAL), and geopandas.
        - Ensure that the required libraries and dependencies are installed to use this function effectively.

    Example Usage:
        akhdefo_fitPlane(dem_data='path/to/dem.tif',line_shapefile='path/to/lines.shp',out_planeFolder='output/folder')
        
    """
    
    global dip_angle_list, dip_direction_list , fig1_cmap, plane_colors
    
    dip_angle_list=[]
    dip_direction_list=[]
    plane_colors=[]
    
    # def cmap_plot(plane_colors,  label='Color'):
        
    #     from matplotlib.colors import ListedColormap
    #     import numpy as np
    #     try:
    #         cmap = ListedColormap(plane_colors)
    #         fig, ax = plt.subplots(figsize=(6, 1))
    #         fig.subplots_adjust(bottom=0.5)
    #         cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), cax=ax, orientation='horizontal')
    #         cbar.set_label(label)
    #         plt.show()
    #     except Exception as ex:
    #         print("")
        
    #     return fig
    
    import os
    import numpy as np
    import matplotlib.pyplot as plt
    from osgeo import gdal
    import tkinter as tk
    from tkinter import ttk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.colors import LightSource
    import earthpy.spatial as es
    import geopandas as gpd
    import random
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    from shapely.geometry import LineString
    
    
    if not os.path.exists(out_planeFolder):
        os.makedirs(out_planeFolder)
    
    def color_from_dip_and_direction(dip, direction):
        cmap_dip = plt.get_cmap('hsv')
        cmap_direction = plt.get_cmap('hsv')

        col_dip = cmap_dip(dip / 90.0)
        col_direction = cmap_direction(direction / 360.0)

        color = [0.5*(col_dip[i] + col_direction[i]) for i in range(3)]
    
        return color

    def random_color():
        """Generate a random color."""
        return (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    def read_dem(dem_file):
        ds = gdal.Open(dem_file)
        data = ds.ReadAsArray()
        transform = ds.GetGeoTransform()
        projection = ds.GetProjection()
        ds = None  # Close the dataset
        return data, transform, projection
    
    data, transform, projection = read_dem(dem_data)
    
    import math

    def calculate_dip_angle_and_direction(A, B):
        # Calculate the dip angle (inclination)
        dip_angle = math.degrees(math.atan(math.sqrt(A**2 + B**2)))
       
        
        # Calculate the dip direction (azimuth)
        dip_direction = math.degrees(math.atan2(-B, -A))
        
        # Ensure dip_direction is in the range [0, 360)
        dip_direction = (dip_direction + 90) % 360
        
        return dip_angle, dip_direction
    
    def fit_plane(points, xx, yy):
        min_range = np.nanmin(data)
        max_range = np.nanmax(data)
        
        # xx = (xx - np.nanmin(xx)) / (np.nanmax(xx) - np.nanmin(xx))
        # xx = xx * (max_range - min_range) + min_range
        
        # yy = (yy - np.nanmin(yy)) / (np.nanmax(yy) - np.nanmin(yy))
        # yy = yy * (max_range - min_range) + min_range
        
        x_vals, y_vals, z_vals = zip(*points)
    
        A = np.vstack([x_vals, y_vals, np.ones(len(x_vals))]).T
        a, b, c = np.linalg.lstsq(A, z_vals, rcond=None)[0]
        
        print(f"Plane equation: z = {a}x + {b}y + {c}")  # Debugging line
        
        zz = a * xx + b * yy + c
        ##################################
        # points = np.array(points) 
        # # Compute the centroid of the points
        # centroid = np.mean(points, axis=0)

        # # Subtract the centroid from the points to center them
        # centered_points = points - centroid

        # # Perform SVD on the centered points
        # U, S, Vt = np.linalg.svd(centered_points)

        # # The normal vector of the plane is the last row of Vt
        # normal_vector = Vt[-1, :]

        # # Normalize the normal vector
        # normal_vector /= np.linalg.norm(normal_vector)

        # # The equation of the plane is: ax + by + cz + d = 0, where [a, b, c] is the normal vector
        # a, b, c = normal_vector

        # # Calculate d using the plane equation and the centroid
        # d = -np.dot(normal_vector, centroid)
        # zz = (-a * xx - b * yy - d) / c  # Solve for z
        
       
        dip_angle, dip_direction = calculate_dip_angle_and_direction(a, b)

        print(f"Dip Angle (Inclination): {dip_angle} degrees")
        print(f"Dip Direction (Azimuth): {dip_direction} degrees")
        
        
        
       
        
        #  # Clip the values to the desired range
        #zz = np.clip(zz, min_range, max_range)
        
        zz[zz < min_range] = np.nan
        zz[zz > max_range] = np.nan
       
       
        # # Define the desired range based on your 'data'
        # if limit_extend==False:
           
        # # # # Normalize 'zz' to match the 'min_range' and 'max_range' of 'data'
        # zz = (zz - np.nanmin(zz)) / (np.nanmax(zz) - np.nanmin(zz))
        # zz = zz * (max_range - min_range) + min_range
        
               
        # print(zz.shape)
        # print(zz)
        return zz, a, b, c, dip_angle, dip_direction
    
   
   
   

    def onclick(event, points, data, transform):
        x, y = event.xdata, event.ydata
        col = int((x - transform[0]) / transform[1])
        row = int((y - transform[3]) / transform[5])

        if 0 <= col < data.shape[1] and 0 <= row < data.shape[0]:
            z = data[row, col]
            points.append([x, y, z])
            ax_2d.plot(x, y, 'o', color='black')
            canvas_2d.draw()

            point_str = f"x={x:.2f}, y={y:.2f}, z={z:.2f}"
            points_listbox.insert(tk.END, point_str)

    def on_point_double_click(event):
        global points, ax_2d, points_listbox, hs
        idx = points_listbox.curselection()[0]  # Index of selected point in the listbox
        point = points[idx]
        
        # Remove the point from our data
        points.pop(idx)
        points_listbox.delete(idx)

        # Identify and remove the corresponding point from the ax_2d plot
        for line in ax_2d.lines:
            xdata, ydata = line.get_xdata(), line.get_ydata()
            if xdata[0] == point[0] and ydata[0] == point[1]:
                line.remove()
                break

        canvas_2d.draw()
        
        
    
    
    def plot_planes(dip_list, azimuth_list, rgb_colors, out_planeFolder=out_planeFolder):
        #from mplstereonet import StereonetAxes
         # Create a stereo net plot
        fig = plt.figure(figsize=(10, 10), dpi=300)
        #ax = fig.add_subplot(121, projection='stereonet')
        ax=fig.add_subplot(121, polar=True)

        for dip_angles, dip_directions, color in zip(dip_list, azimuth_list, rgb_colors):
            # Convert dip directions and dip angles to radians
            #dip_directions = (dip_directions + 90) % 360 #converted dip direction to strike
            dip_angles = (90 - np.array(dip_angles))  # Convert dip angles to complementary angles
             # Convert dip azimuths to radians
            dip_azimuths_rad = np.radians(dip_directions)
            # Plot the poles of planes as dots
            ax.scatter(dip_azimuths_rad, dip_angles, color=color)   

        ax.grid(True)
        ax.set_theta_zero_location('N')  # Set 0 degrees at the top
        ax.set_theta_direction(-1)  # Reverse the direction of the angles

        # Set labels for cardinal directions
        ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
        ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

        # Set the radial grid and labels
        ax.set_rlabel_position(90)
        ax.set_yticks([15, 30, 45, 60, 75])
        ax.set_rmax(90)  # Set the maximum radial distance
        ax.set_title("Poles to Planes")
        # Customize tick marks - specify angles in radians
        # ax.set_xticks(np.radians(range(0, 360, 10)))  # 10-degree intervals
        # ax.set_yticks(np.radians(range(-90, 90, 10)))

        strikes=[]
        all_colors=[]
        for dip_angles, dip_directions, color in zip(dip_list, azimuth_list, rgb_colors):
            dip_azimuths_rad = np.radians(dip_directions)
            #dip_directions = (dip_directions + 90) % 360
            dip_angles = (90 - np.array(dip_angles))  # Convert dip angles to complementary angles
            strikes.append((dip_azimuths_rad + 90) % 360)
            all_colors.append(color)
        

         # Calculate the number of bins using Scott's Rule
        n = len(strikes)

        # Calculate the standard deviation of the data
        std_dev = np.std(strikes)

        # Calculate the bin width using Scott's Rule formula, ensuring it's not zero
        if std_dev != 0:
            bin_width = 0.5 * std_dev / (n**(1/3))  # Scott's Rule formula
            num_bins = max(int((max(strikes) - min(strikes)) / bin_width), 1)  # Ensure num_bins is at least 1
        else:
            num_bins = 12  # A default number of bins if std_dev is zero
        # Create a rose diagram (circular histogram)
        ax_rose = fig.add_subplot(122, polar=True)

        for dip, strike, color, az in zip(dip_list, strikes, all_colors, azimuth_list):
            # Convert dip azimuths to radians
            dip_azimuths_rad = np.radians(az)
            dip_angles = (90 - np.array(dip_angles))  # Convert dip angles to complementary angles
            
            # Plot dip angles as radii and dip azimuths as angles
            #ax_rose.scatter(dip_azimuths_rad, dip_angles, c=color, alpha=0.5)
            # Plot the orientation data as a rose diagram
            n, bins, patches=ax_rose.hist(strike, bins=num_bins, color=color, alpha=0.5)
             # Annotate the number of data points and bin number
            ax_rose.text(0, -0.1, f"Data Points: {len(strikes)}", ha='center', va='center', transform=ax_rose.transAxes)
            ax_rose.text(0, -0.15, f"Bin Count: {num_bins}", ha='center', va='center', transform=ax_rose.transAxes)

        # # Customize the rose diagram
        # ax_rose.set_theta_zero_location("N")
        # ax_rose.set_theta_direction(-1)
        # Customize the polar plot
        ax_rose.set_theta_zero_location('N')  # Set 0 degrees at the top
        ax_rose.set_theta_direction(-1)  # Reverse the direction of the angles

        # Set labels for cardinal directions
        ax_rose.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
        ax_rose.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
       

        # Set the radial grid and labels
        # ax_rose.set_rlabel_position(90)
        # ax_rose.set_yticks([15, 30, 45, 60, 75])
        # ax_rose.set_rmax(90)  # Set the maximum radial distance
        ax_rose.set_title("Rose Diagram Strike")

        # Adjust spacing between subplots
        plt.subplots_adjust(wspace=0.2)

        plt.savefig(out_planeFolder + "/" + "stereoplot.png", dpi=300)
        plt.tight_layout
        #plt.close()
        plt.close()
        
    
    
        
    def draw_plane(xx,yy):
        
        if len(points) >= 3:
            fitted_plane, a, b, c , dip_angle, dip_direction = fit_plane(points, xx, yy)
            
            dip_angle_list.append(dip_angle)
            dip_direction_list.append(dip_direction)
            
            # if limit_extend:
            #  #Get bounding box of the selected points
            #     xmin, xmax, ymin, ymax = bounding_box(points)
                
            #     mask = (xx >= xmin) & (xx <= xmax) & (yy >= ymin) & (yy <= ymax)
                
            #     for i in range(xx.shape[0]):
            #         for j in range(xx.shape[1]):
            #             if not mask[i, j]:
            #                 fitted_plane[i, j] = np.nan  # Set out-of-bounds values to NaN
        
            planes.append(fitted_plane)
            
            #plane_color = random_color()
            plane_color=color_from_dip_and_direction(dip_angle, dip_direction)
            print('plane color: ', plane_color)
            plane_colors.append(plane_color)

            for point  in points:
                ax_2d.plot(point[0], point[1], 'o', color=plane_color , alpha=0.7)
          
            
        
            canvas_2d.draw()
            

            #ax_3d.clear()
            ax_3d.set_title('3D DEM with Fitted Planes')
            ax_3d.plot_surface(xx, yy, data, cmap='terrain', linewidth=0, antialiased=True, alpha=0.5)
            #for plane in planes:
            surf=ax_3d.plot_surface(xx, yy, fitted_plane, alpha=0.6, linewidth=0, antialiased=True, color=plane_color)
            
                #plot points in 3D
            for point in points:
                ax_3d.plot(point[0], point[1], 'o', color=plane_color)
                
            canvas_3d.draw()
            
            
            

            points_listbox.delete(0, tk.END)
            points.clear()
            
            plot_planes(dip_angle_list, dip_direction_list, plane_colors)
            
            # Assuming you have a 'planes' list, you can check its format
            # for plane in planes:
            #     print(type(plane))
            #     print(len(plane))  # This will give you the length or number of elements in the plane

            #     # If it's a NumPy array, you can print its shape to see the dimensions
            #     if isinstance(plane, np.ndarray):
            #         print(plane.shape)
                
            #     # Print the first element (assuming it's a list or NumPy array)
            #     print(plane[0])

            # # Print the length of the 'planes' list
            # print(len(planes))
            
            
            
        

    def bounding_box(points):
        """Find the bounding box for a set of points."""
        x_vals, y_vals, _ = zip(*points)
        
        
        return min(x_vals) , max(x_vals), min(y_vals), max(y_vals)

    ########

   
    
    import ezdxf
    from scipy.spatial import Delaunay
    import numpy as np
    import os

    def list_xyz_files_in_folder(folder_path):
        xyz_files = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".xyz"):
                xyz_files.append(os.path.join(folder_path, filename))
        return xyz_files

    def create_dxf_from_xyz_files(xyz_files, output_path, single=None):
        
        if single is None:
             # Create a new DXF document
            doc = ezdxf.new()

            # Create a new DXF model space
            msp = doc.modelspace()
            
           

        for xyz_file in xyz_files:
            
            if single is not None:
                # Create a new DXF document
                doc = ezdxf.new()

                # Create a new DXF model space
                msp = doc.modelspace()
            # Load XYZ data from a file
            data = np.loadtxt(xyz_file)
            

            # Separate the XYZ data into individual arrays
            x = data[:, 0]
            y = data[:, 1]
            z = data[:, 2]

            # Create a Delaunay triangulation of the points
            tri = Delaunay(np.column_stack((x, y)))

            # Add the triangles to the model space
            for simplex in tri.simplices:
                vertices = [(x[i], y[i], z[i]) for i in simplex]
                msp.add_3dface(points=vertices)
            
            if single is not None:
                    # Save the DXF file
                doc.saveas(output_path)
            
        if single is None: 

            # Save the DXF file
            doc.saveas(output_path)
        
    
    def save_planes_to_obj():
        x_coords = np.linspace(left, right, data.shape[1])
        y_coords = np.linspace(top, bottom, data.shape[0])
        xx, yy = np.meshgrid(x_coords, y_coords)
       
        if not planes:
            print("No planes to save.")
            return
        
        
        output_filename_dxf = f"{out_planeFolder}/planes.dxf"
        for idx, plane in enumerate(planes):
            output_filename = f"{out_planeFolder}/planes_{idx}.xyz"
            output_filename_idx = f"{out_planeFolder}/planes_{idx}.dxf"
            
            # Initialize lists to store vertices and faces
            vertices = []
            
            # Sampled point interval
            sample_interval = 200
            
            # Open the XYZ file for writing
            with open(output_filename, 'w') as xyz_file:
                for i in range(0, plane.shape[0], sample_interval):
                    for j in range(0, plane.shape[1], sample_interval):
                        if i < xx.shape[0] and j < xx.shape[1]:
                            x = xx[i, j]
                            y = yy[i, j]
                            z = plane[i, j]

                            # Check for NaN values
                            if not np.isnan(x) and not np.isnan(y) and not np.isnan(z):
                                # Add the vertex to the list
                                vertices.append((x, y, z))
                               
                                # Write vertex data to the XYZ file
                                xyz_file.write(f'{x} {y} {z}\n')
            
            create_dxf_from_xyz_files(list_xyz_files_in_folder(out_planeFolder), output_filename_idx, single=idx)
            
                  
        print(f'zz values saved to {output_filename}')
            
        
   
        
        
    def collect_points_from_line(gdf):
        """Collect start, middle, and end points from each line feature."""
        collected_points = []

        for geometry in gdf.geometry:
            if geometry.geom_type == "LineString":
                x, y = geometry.xy
                start = (x[0], y[0])
                end = (x[-1], y[-1])
                
                #print('start: ' ,start)
                
                # # Create a LineString from coordinates to easily get a point at 50% distance
                line = LineString(zip(x, y))
                # if len(line.coords) >= 3:
                #     # If the line has more than 2 vertices, collect points at vertices
                #     vertices = list(line.coords)
                #     #print('vertics: ', vertices)
                #     vertex_list=[i for i in vertices]
                #     for kj in vertex_list:
                #         collected_points.append(kj)
                #     #collected_points.extend(vertices)
                # else:
                    
                middle = line.interpolate(0.5, normalized=True).coords[0]
                p2 = line.interpolate(0.25, normalized=True).coords[0]
                p1 = line.interpolate(0.75, normalized=True).coords[0]

                collected_points.append([start, middle, end, p1,p2])

        return collected_points

    # def collect_points_from_line(gdf):
    #     # Initialize an empty list to store the coordinates
    #     collected_points = []

    #     # Iterate through the GeoDataFrame
    #     for geometry in gdf['geometry']:
    #         if isinstance(geometry, LineString):
    #             # Count the number of vertices in the LineString
    #             num_vertices = len(geometry.coords)
                
    #             # Check if the LineString is straight (3 or fewer vertices)
    #             if num_vertices <= 3:
    #                 # For straight lines, take coordinates of start, end, and middle
    #                 start_point = geometry.coords[0]
    #                 end_point = geometry.coords[-1]
    #                 middle_point = geometry.interpolate(0.5, normalized=True).coords[0]
                    
    #                 collected_points.extend([start_point, middle_point, end_point])
    #             else:
    #                 # For curved lines, take coordinates of all vertices
    #                 for point in geometry.coords:
    #                     x, y = point
    #                     collected_points.append((x, y))
        
    #     return collected_points

# Now, coordinates_list contains the coordinates of start, end, middle, and all vertices
# based on whether the line is straight (3 or fewer vertices) or curved
        
    

    def draw_planes_from_lines(xx,yy):
        global ax_2d, ax_3d, data, transform, left, right, bottom, top, planes 
        
        data, transform, projection = read_dem(dem_data)

        gdf = gpd.read_file(line_shapefile)
        if gdf.crs.to_string() != projection:
            gdf = gdf.to_crs(projection)

        point_sets = collect_points_from_line(gdf)
        # x_coords = np.linspace(left, right, data.shape[1])
        # y_coords = np.linspace(top, bottom, data.shape[0])
        # xx, yy = np.meshgrid(x_coords, y_coords)
        
        from tqdm import tqdm
        planes=[]
        for points in tqdm(point_sets, desc="Processing fitted planes"):
            #print('points: ', points)
            #z_values = [data[int((point[1] - top) / abs(transform[5])), int((point[0] - left) / transform[1])] for point in points]
            
            z_values = []

            for point in points:
                y_index = int((point[1] - top) / abs(transform[5]))
                # y_index = int((point[1] - top) / abs(transform[5])) if isinstance(point[1], (int, float)) and isinstance(transform[5], (int, float)) else None
                # x_index = int((point[0] - top) / abs(transform[1])) if isinstance(point[0], (int, float)) and isinstance(transform[1], (int, float)) else None

                x_index = int((point[0] - left) / transform[1])
                
                z_value = data[y_index][x_index]
                
                z_values.append(z_value)

            xyz_points = [points[i] + (z_values[i],) for i in range(len(z_values))]

            if len(xyz_points) >= 3:
                fitted_plane, a, b, c, dip_angle, dip_direction = fit_plane(xyz_points, xx, yy)
                
                dip_angle_list.append(dip_angle)
                dip_direction_list.append(dip_direction)
            
                # if limit_extend:
                #     # Get bounding box of the selected points
                #     xmin, xmax, ymin, ymax = bounding_box(xyz_points)
                    
                #     mask = (xx >= xmin) & (xx <= xmax) & (yy >= ymin) & (yy <= ymax)
                    
                #     for i in range(xx.shape[0]):
                #         for j in range(xx.shape[1]):
                #             if not mask[i, j]:
                #                 fitted_plane[i, j] = np.nan  # Set out-of-bounds values to NaN
                ###########
                
                #########
            
                planes.append(fitted_plane)
                #plane_color = random_color()
                plane_color=color_from_dip_and_direction(dip_angle, dip_direction)
                plane_colors.append(plane_color)
                
                
        
            ####
                for pointn in xyz_points:
                    ax_2d.plot(pointn[0], pointn[1], 'o', color=plane_color, alpha=0.7)
                canvas_2d.draw()

                #ax_3d.clear()
                ax_3d.set_title('3D DEM with Fitted Planes')
                ax_3d.plot_surface(xx, yy, data, cmap='terrain', linewidth=0, antialiased=True, alpha=0.5)
                #for plane in planes:
                ax_3d.plot_surface(xx, yy, fitted_plane, alpha=0.6, linewidth=0, antialiased=True, color=plane_color)
                canvas_3d.draw()
                
                plot_planes(dip_angle_list, dip_direction_list, plane_colors)
            
        
    

    def plot_dem(data, transform, projection, path_to_shapefile):
        global ax_2d, ax_3d, points, canvas_2d, canvas_3d, points_listbox, planes, plane_colors, hs, left, right, bottom, top
        points = []
        planes = []
        plane_colors = []
        
        

        hs = es.hillshade(data)

        root = tk.Tk()
        root.title("Akhdefo_FitPlanes")

        left, cell_size_x, _, top, _, cell_size_y = transform
        
       
        right = left + cell_size_x * data.shape[1]
        bottom = top + cell_size_y * data.shape[0]

        fig1 = plt.Figure(figsize=(6, 6), dpi=150)
        ax_2d = fig1.add_subplot(111)
        ax_2d.imshow(hs, cmap='gray', extent=[left, right, bottom, top])
        ax_2d.set_title('Hillshade', fontweight="bold", fontsize=14)
        ax_2d.set_xlabel("Longitude", fontsize=12)
        ax_2d.set_ylabel("Latitude", fontsize=12)
        ax_2d.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax_2d.set_aspect('equal')
        
        
        
        if path_to_shapefile is not None:
            gdf = gpd.read_file(path_to_shapefile)
            if gdf.crs.to_string() != projection:
                gdf = gdf.to_crs(projection)
            gdf.plot(ax=ax_2d, color='red', label="Linear Features")
            ax_2d.legend(loc="upper left")
        
        fig2 = plt.Figure(figsize=(6, 6), dpi=150)
        # Create a figure and axis
        ax_3d = fig2.add_subplot(111, projection='3d')
        ax_3d.set_title('3D DEM with Fitted Planes', fontweight="bold", fontsize=14)
        ax_3d.set_xlabel("Longitude", fontsize=12)
        ax_3d.set_ylabel("Latitude", fontsize=12)
        ax_3d.set_zlabel("Elevation", fontsize=12)
        x_coords = np.linspace(left, right, data.shape[1])
        y_coords = np.linspace(top, bottom, data.shape[0])
        xx, yy = np.meshgrid(x_coords, y_coords)
        
        
        

        

        # ax_3d.set_xlim([left, right])
        # ax_3d.set_ylim([bottom, top])
        # ax_3d.set_zlim([zmin, zmax])

        frame_2d = tk.Frame(root)
        frame_2d.grid(row=0, column=0, sticky='nsew')
        # canvas_2d = FigureCanvasTkAgg(fig1, master=frame_2d)
        # canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=False)
        # toolbar_2d = NavigationToolbar2Tk(canvas_2d, frame_2d)
        # toolbar_2d.update()
        # Create the canvas for the plot
        canvas_2d = FigureCanvasTkAgg(fig1, master=frame_2d)
        canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Fill the frame
        # Create the toolbar and place it at the top of the canvas
        toolbar_2d = NavigationToolbar2Tk(canvas_2d, frame_2d)
        toolbar_2d.update()
        toolbar_2d.pack(side=tk.TOP, fill=tk.X)  # Pack the toolbar at the top
        
        #######add colorbar figure to Canvas
        



        frame_3d = tk.Frame(root)
        frame_3d.grid(row=0, column=1, sticky='nsew')
        # canvas_3d = FigureCanvasTkAgg(fig2, master=frame_3d)
        # canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=False)
        # toolbar_3d = NavigationToolbar2Tk(canvas_3d, frame_3d)
        # toolbar_3d.update()
        canvas_3d = FigureCanvasTkAgg(fig2, master=frame_3d)
        canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Fill the frame
        # Create the toolbar and place it at the top of the canvas
        toolbar_3d = NavigationToolbar2Tk(canvas_3d, frame_3d)
        toolbar_3d.update()
        toolbar_3d.pack(side=tk.TOP, fill=tk.X)  # Pack the toolbar at the top

        # Create a frame on the right to hold controls
        controls_frame = tk.Frame(root)
        controls_frame.grid(row=0, column=3, rowspan=1, sticky='nsew')
        

        # Now put all buttons and Listbox inside this controls_frame
        draw_button = ttk.Button(controls_frame, text="Draw Plane", command=lambda: draw_plane(xx,yy))
        draw_button.pack(pady=2, padx=2)

        line_plane_button = ttk.Button(controls_frame, text="Create Planes from Lines", command=lambda: draw_planes_from_lines(xx,yy))
        line_plane_button.pack(pady=2, padx=2)

        save_plane_button = ttk.Button(controls_frame, text="Save Planes to OBJ", command=save_planes_to_obj) #save_fitted_planes_as_dxf
        save_plane_button.pack(pady=2, padx=2)
        # save_plane_button_dxf = ttk.Button(controls_frame, text="Save Planes to DXF", command=save_fitted_planes_as_dxf)
        # save_plane_button_dxf.pack(pady=10, padx=10)

        points_listbox = tk.Listbox(controls_frame, height=5, width=40, exportselection=False)
        points_listbox.pack(pady=2, padx=2, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(controls_frame, orient="vertical", command=points_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        points_listbox.config(yscrollcommand=scrollbar.set)
        points_listbox.bind("<Double-Button-1>", on_point_double_click)
        ####
    
        
        ####

        fig1.canvas.mpl_connect('button_press_event', lambda event: onclick(event, points, data, transform))
        
        
        # Adding the size grip for window resizing
        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(row=3, column=1, sticky='nsew')

        # Making the design responsive
        root.grid_rowconfigure(0, weight=1)  # Canvas row
        root.grid_rowconfigure(1, weight=0)  # Toolbar row
        root.grid_rowconfigure(2, weight=0)  # Button row
        root.grid_columnconfigure(0, weight=1)  # 2D plot column
        root.grid_columnconfigure(1, weight=1)  # 3D plot column
        
        
                
        root.mainloop()


    
    plot_dem(data, transform, projection, line_shapefile)
   
    
#akhdefo_fitPlane(dem_data='currie/dem_1m.tif', line_shapefile='currie/lines.shp', out_planeFolder='Planes_out/new', limit_extend=False)