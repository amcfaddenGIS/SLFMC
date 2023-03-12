# Live Fuel Moisture Equations
import os
import tempfile
import shutil
from .Spectral_Indices import indices
import pathlib as ptlib
import numpy as np
import rasterstats
from matplotlib import pyplot as plt
from osgeo import gdal
import statistics as stats
import csv
import rasterio

# List rasters
def __List_Rasters(Path, file_type = "tif"):
    path = ptlib.Path(Path)
    All_Rasters = list(path.glob('**/*.{}'.format(file_type)))
    Raster_List = []
    for raster in All_Rasters:
        Raster_Path = str(raster).replace("/", "\\")
        Raster_List.append(Raster_Path)
    return Raster_List

# Create a seasonal live fuel moisture plot
def __Create_Monthly_Moisture_Plot(list, std, output_location, error_bars = False):
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    plt.title("Average Seasonal NDMI")
    plt.grid('on')
    plt.xlabel("Month")
    plt.ylabel("NDMI")
    if error_bars is True:
        plt.errorbar(months, list, yerr=std, capsize=5, fmt = '-bo', ecolor='black')
    else:
        plt.plot(months, list, '-bo')
    plt.savefig("{}SLFMC.png".format(output_location))

def Average_Annual_Fuel_Moisture(csv_folder, raster_folder, NIR, SWIR1, file_type = "tif",
                                 shapefile_location = None, zonal_stats = False,
                                 error_bars = False, output_csv = False):
    """
    Determines the Seasonal Live Fuel Moisture of a specified extent by calculating the mean NDMI/NDWI




    :param csv_folder: Output location for CSV
    :param raster_folder: Location of raster dataset
    :param NIR: Band number affiliated with NIR band
    :param SWIR1: Band number affiliated with SWIR1 band
    :param file_type: File type for your rasters
    :param shapefile_location: File location of your zonal statistics shape file
    :param zonal_stats: If True, run zonal statistics
    :param error_bars:  IF True, provide error bars on graph
    :param output_csv: If True, provide output CSV of measured NDMIs and their associated Image
    :return: Seasonal Live Fuel Moisture Graph  and CSV (optional)
    """
    # Function that ouptuts a list of all rasters
    raster_list = __List_Rasters(raster_folder, file_type=file_type)
    # List of MEAN NDMIs
    # Index values for this list are associated with the index values in the name, year, and month list
    # This is important for the csv
    Mean_list = []
    # Record the number of times a specific month is identified in a Landsat image name
    month_freq_dict = {
        "01": 0,
        "02": 0,
        "03": 0,
        "04": 0,
        "05": 0,
        "06": 0,
        "07": 0,
        "08": 0,
        "09": 0,
        "10": 0,
        "11": 0,
        "12": 0, }
    # Sum of all NDMIs for each month
    month_sum_LFM = {
        "01": 0,
        "02": 0,
        "03": 0,
        "04": 0,
        "05": 0,
        "06": 0,
        "07": 0,
        "08": 0,
        "09": 0,
        "10": 0,
        "11": 0,
        "12": 0, }
    # Standard deviation for all recorded means for each month
    month_std = []
    # List of months. Index value is associated with year, Landsat image name, and NDMI mean list
    month_list = []
    # List of LANDSAT names. Index value is associated with year,  month list and NDMI mean list
    name_list = []
    # List of year. Index value is associated with Landsat name, month list and NDMI mean list
    year_list = []
    # IF zonal statistics is true, run this portion of the function
    # Mean NDMI/NDWI is calculated for a shapefile extent
    if zonal_stats is True:
        # Temporary directory
        temp = tempfile.mkdtemp()
        # Grabs each raster in the list
        for raster in raster_list:
            # Grabs the file name from the path
            file_name = os.path.basename(raster)
            # Appends the file name to the name list
            name_list.append(file_name)
            # Grabs the month from the landsat image name
            month = file_name[16:18]
            # Grabs the year from the landsat image name
            year = file_name[12:16]
            # Append the year to the year list
            year_list.append(year)
            # Append the month to the month list
            month_list.append(month)
            month_freq_dict[month] = month_freq_dict[month] + 1
            # Calculate NDMI/NDWI and output a raster to the temp directory
            indices.NDMI_NDWI(output_location="{}/zonal_stat.tif".format(temp), raster_location=raster,
                              shapefile_location=shapefile_location, output_raster=True,
                              clip_extent=False, NIR_Band=NIR, SWIR1_Band=SWIR1)
            # Calculate zonal statistics with the temp raster
            zstats = rasterstats.zonal_stats(shapefile_location, "{}/zonal_stat.tif".format(temp), stats = "mean std")
            # Grab the mean from the zstats dictionary
            mean = zstats[0]
            # If a specific month is called, change the value for the month (key) in the month sum list
            # If January (01) is called, the value from the 01 key is increased/decreases by the mean
            month_sum_LFM[month] = month_sum_LFM[month] + mean['mean']
            # Found this off of stack overflow (specifically removing a file)
            Mean_list.append(mean['mean'])
            # Remove the temp raster and run again
            os.remove("{}/zonal_stat.tif".format(temp))
        # Close the directory when the loop is done
        shutil.rmtree(temp)
    # Function runs the same, however the mean value from the raster is calculated
    # This is assumed if the user has preprocessed their data
    if zonal_stats is False:
        # A Stack overflow article helped me figure this out
        temp = tempfile.mkdtemp()
        for raster in raster_list:
            file_name = os.path.basename(raster)
            name_list.append(file_name)
            month = file_name[16:18]
            year = file_name[12:16]
            year_list.append(year)
            month_list.append(month)
            month_freq_dict[month] = month_freq_dict[month] + 1
            NDMI = indices.NDMI_NDWI(output_location="{}/zonal_stat.tif".format(temp), raster_location=raster,
                         shapefile_location=shapefile_location, output_raster=True, clip_extent=False,
                         NIR_Band=NIR, SWIR1_Band=SWIR1)
            Mean_list.append(np.mean(NDMI))
        shutil.rmtree(temp)
    # Create list for the monthly average
    monthly_average = []
    for i in month_sum_LFM.keys():
        # Found this from a stack overflow question
        # Grab the index value for a specified month in the month list
        # I.e. each index value for January (1)
        index = [j for j, x in enumerate(month_list) if x == i]
        # Since those index values are associated with specific NDMI/NDWI means
        # Grab the NDMI/NDWI means based on the index values that you chose
        mean_month = [Mean_list[n] for n in index]
        # Calculate the standard deviation for the list of means (split by month)
        std = stats.pstdev(mean_month)
        # Append that standard deviation to the standard deviation month list.
        month_std.append(std)
        # Calculate the average NDMI/NDWI based on the month and the frequency of the month
        average = month_sum_LFM[i]/month_freq_dict[i]
        monthly_average.append(average)
    # Create a plot of the monthly NDMI/NDWIs
    __Create_Monthly_Moisture_Plot(monthly_average, month_std, error_bars=error_bars, output_location=csv_folder)
    print(month_freq_dict)
    # Output a csv with the mean NDMIs
    if output_csv is True:
        with open('{}/NDMI.csv'.format(csv_folder), 'w', newline='') as file:
            # Write a CSV
            writer = csv.writer(file)
            # Provide row titles for the CSV
            Row_title = ["Image_ID", "Year", "Month", "NDMI"]
            # Add row titles to the newly created CSV
            writer.writerow(Row_title)
            # Iterate through each image name, year, month and mean NDMI
            # Add values from each list as a new row to the CSV
            for i in range(0, len(name_list)):
                Rows = [name_list[i],  year_list[i], month_list[i], Mean_list[i]]
                writer.writerow(Rows)

def Annual_Live_Fuel_Moisture_Raster_Stack(raster_folder, NIR, SWIR1, shapefile_location, output_location, file_type = "tif", clip_extent = False):
    """
    Creates a temporal NDMI/NDWI raster stack for analysis in other GIS software. Bands are temporal and not spectral.
    Suggested applications would involve dimensionality reduction through PCAs to determine temporal endmembers in the burn extent

    :param raster_folder: File path for all rasters
    :param NIR: Band number associated with the NIR band
    :param SWIR1: Band number associated with the SWIR band
    :param shapefile_location: Shapefile location, if the user wants to clip the raster
    :param output_location: Output location for the raster stack
    :param file_type: File type for the output
    :param clip_extent: If true, clip the raster using the shapefile location
    :return: Temporal Raster stack
    """
    # Function that ouptuts a list of all rasters
    temp = tempfile.mkdtemp()
    raster_list = __List_Rasters(raster_folder, file_type=file_type)
    r = rasterio.open(raster_list[0])
    # Detemrine the number of bands required based on the length of this list
    bands = len(raster_list)
    out_meta = r.meta
    out_meta.update({'count': bands})
    ndmi_raster = rasterio.open(output_location, 'w', **out_meta)
    i = 1
    for r in raster_list:
        NDMI_Array = indices.NDMI_NDWI(output_location="{}/clipped.tif".format(temp), raster_location=r,
                                       shapefile_location=shapefile_location, output_raster=True,
                                       clip_extent=clip_extent,
                                       NIR_Band=NIR,
                                       SWIR1_Band=SWIR1)
        ndmi_raster.write_band(NDMI_Array, i)
        i += 1
        os.remove("{}/clipped.tif".format(temp))
    # Loop through each raster and assign the NDMI/NDWI array to each band in the temporal raster stack
    # Remove the temp directory
    shutil.rmtree(temp)




