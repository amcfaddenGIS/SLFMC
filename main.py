import os
import tempfile
import pandas
import matplotlib.pyplot as plt
from Live_Fuel_Moisture.Spectral_Indices import indices
from Live_Fuel_Moisture import Live_Fuel_Moisture
import rasterstats
def main():
    wd = os.getcwd()
    wd_path = str(wd).replace("\\", "/")
    # Specify raster location
    raster_location = "C:/Users/alexm/PycharmProjects/Thesis2/Landsat8_Esperanza"
    # Specify output_csv location
    csv_folder = "{}/outputs/".format(wd_path)
    # Specfy shapefile location
    shapefile_location = "{}/data/Shapefile/Esperanza.shp".format(wd_path)
    # Specify raster stack output location
    raster_stack = "{}/outputs/Average_Annual_Raster.tif".format(wd_path)
    # Estimate Sesaonal Live Fuel Moisture
    #Live_Fuel_Moisture.Average_Annual_Fuel_Moisture(csv_folder= csv_folder, raster_folder=raster_location, NIR=3, SWIR1=4, shapefile_location=shapefile_location, zonal_stats=True, error_bars=True, output_csv=True)
    # Create live fuel moisture temporal raster stack
    Live_Fuel_Moisture.Annual_Live_Fuel_Moisture_Raster_Stack(raster_folder=raster_location, NIR=3, SWIR1=4, shapefile_location=shapefile_location, clip_extent=True, output_location= raster_stack)


"""
Next Tools:
- Webscraping to grab RAWs data based on specifications from the user
- Which sensor and date range
    - This will take time, but I'll work on it in my free time

Analysis:
- Examine series of LFMC for varying types of crops


"""


if __name__ == "__main__":
    main()
