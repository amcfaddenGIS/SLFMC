# Indices used for calculating LFC through remote sensed image
from osgeo import ogr
from osgeo import gdal
import tempfile
import os
import shutil
import numpy as np
import rasterio
import fiona
# Function creates an output raster, used for numerous functions
# Change this function to Rasterio

def __Clip_Rasters_IO(raster, shapefile, output_path):
    with fiona.open(shapefile, 'r') as shapefile:
        for feature in shapefile:
            shapes = [feature['geometry']]
    with rasterio.open(raster) as r:
            out_image, out_transform = rasterio.mask.mask(r, shapes, crop=True)
            out_meta = r.meta
            out_meta.update({
                "driver": "Gtiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })
    with rasterio.open(output_path, 'w', **out_meta) as dst:
            dst.write(out_image)

def NDMI_NDWI(output_location, raster_location, SWIR1_Band, NIR_Band,
              shapefile_location = None,
              output_raster=False, clip_extent=False):
    """
    Calculate NDMI/NDWI for a single raster

    :param output_location: Output location for NDMI/NDWI raster. Must be specified as a .tif (i.e. /output/NDMI.tif)
    :param raster_location: File path for the input raster
    :param SWIR1_Band: Band number for the SWIR band
    :param NIR_Band: Band number for the NIR band
    :param shapefile_location: File path for input shapefile
    :param output_raster: If True, output raster
    :param clip_extent: If True, clip raster
    :return: NDMI/NDWI array and output raster (optional)
    """

    Array = 0
    # If clip_extent is true, run this
    temp = tempfile.mkdtemp()
    if clip_extent is True:
        # Create temporary directory to house clipped raster
        # Use a Rasterio Function to clip the raster and output it to the temp directory
        __Clip_Rasters_IO(output_path = "{}\clipped.tif".format(temp),
                          raster=raster_location,
                          shapefile=shapefile_location)
        # Open the output raster in the temp directory
        r = rasterio.open("{}\clipped.tif".format(temp))
        out_meta = r.meta
        out_meta.update({'count': 1})
        NIR_Array = r.read(NIR_Band).astype(float)
        SWIR_Array = r.read(SWIR1_Band).astype(float)
        # Calculate NDMi/NDWI
        NDMI = (NIR_Array - SWIR_Array) / (NIR_Array + SWIR_Array)
        # If there are NA values during the calculation, convert them into 0s
        NDMI[np.isnan(NDMI)] = 0
        # If the user specifies an output location for their output raster
        if output_raster is True:
            with rasterio.open(output_location, 'w', **out_meta) as dst:
                dst.write(NDMI, 1)
        # Remvoe the clipped raster
        r = None
        # Delete the clipped raster in the temp file
        os.remove("{}\clipped.tif".format(temp))
        # Remote the output temp directory
        shutil.rmtree(temp)
        # Assign the NDMI/NDWI array to the global array variable
        Array = NDMI
    # If clip extent is false, run this
    if clip_extent is False:
        # Tool runs essentially the same, however a temporary directory is not created
        r = rasterio.open("{}\clipped.tif".format(temp))
        out_meta = r.meta
        out_meta.update({'count': 1})
        NIR_Array = r.read(NIR_Band).astype(float)
        SWIR_Array = r.read(SWIR1_Band).astype(float)
        # Calculate NDMi/NDWI
        NDMI = (NIR_Array - SWIR_Array) / (NIR_Array + SWIR_Array)
        # If there are NA values during the calculation, convert them into 0s
        NDMI[np.isnan(NDMI)] = 0
        # If the user specifies an output location for their output raster
        if output_raster is True:
            with rasterio.open(output_location, 'w', **out_meta) as dst:
                dst.write(NDMI, 1)
        # Remvoe the clipped raster
        Array = NDMI
    return Array






