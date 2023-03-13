# SLFMC
**Seasonal Live Fuel Moisture Content (SLFMC)**: A python package for analyzing seasonal fluctuations of live fuel moisture content through Landsat imagery

## **Background**

#### *What is Live Fuel Moisture Content (LFMC)?*
  LFMC is an estimation of water content within plants. It is expressed as a ratio of water content in fresh plant tissue to its dry weight (Pivovaroff et al. 2019) and is measured by collecting samples of vegetation on the ground. 

#### *Why is it Important?*
  LFMC is a key component for wildfire spread and ignition since moisture reduces the flammability of vegetation, subsequently lowering the possibility of wildfire progression (Pivovaroff et al. 2019). For ignition to occur, vegetation must reach a critical fuel moisture threshold. For the graph provided by Pivovaroff et al., LFMC exhibits a seasonal trend due to variations in precipitation. During the Summer and Fall, precipitation decreases in southern California and LFMC of chaparral (vegetation) reaches its critical threshold for ignition, increasing fire risk. 


<img src="https://github.com/amcfaddenGIS/SLFMC/blob/main/LFM.jpg" width = "500" height = "300" align = "right" alt="Seasonal Live Fuel Moisture (Pivovaroff et al. 2019)" title="Seasonal Live Fuel Moisture (Pivovaroff et al. 2019)">

#### *How do we effectively estimate it through Remote Sensing?*
Wildfire researchers have pursued research methods that implement remote sensed imagery to estimate LFMC, specifically vegetation indices. Vegetation indices use the electromagnetic information (reflectance or absorption) of vegetation to determine vegetative properties, including biomass, plant health and fuel moisture (Xue and Su 2017). For estimating vegetation moisture, Gao et al. developed the Normalized Difference Water Index (NDWI). NDWI is also known as the Normalized Difference Moisture Index (NDMI). NDWI uses shortwave infrared (SWIR) and near infrared reflectance (NIR) to estimate vegetation moisture in vegetation: (SWIR-NIR/SWIR+NIR). Since NDWI is capable of estimating vegetation moisture, researchers have adopted it to determine LFMC of varying vegetation types.  Dennison et al. (2005) noted that NDWI was positively correlated with ground measurements of LFMC (Southern California Chaparral), suggesting it can effectively estimate NDWI. Dennison et al. also acknowledges the possibility of measuring seasonal variations in LFMC through NDWI. 


## **The Python Package**
#### *Estimating Seasonal Live Fuel Moisture Through Vegetation Indices and Landsat Imagery*
Since NDWI/NDMI is positively correlated with ground-based estimations of LFMC, NDWI/NDMI can effectively track seasonal variations in LFMC. This python package tracks seasonal variations in LFMC by calculating the NDWI/NDMI of a series of Landsat images that extend numerous years. The month-by-month NDWI/NDMI average  is the Seasonal Live Fuel Moisture Content (SLFMC). 

#### *Data Requirements*
For properly estimating Seasonal Live Fuel Moisture Content, the Landsat imagery must be pruned appropriately. Specifically, the names for each raster in the multitemporal series must match a specified sequence. When downloading Landsat imagery on GEE, or through directly from the USGS, each image has a specific syntax that provides important information about when the imagery was collected. An example is provided below

#### **LC08_040036_20180112.tif**

Note that the end of the file name indicates the time at which the imagery was collected. Make sure each image in your raster series follows the naming conventions above. If your files do not, the SLFMC approximation will not work properly. In addition, make sure the CRS of your shapefiles match the CRS of your raster series. If they do not, the rasters won't be properly clipped and the zonal stats tool will not work properly. 

<img src="https://github.com/amcfaddenGIS/SLFMC/blob/main/NDMI.png" width = "500" height = "350" align = "right" title="Seasonal Live Fuel Moisture (Pivovaroff et al. 2019)">

#### *Modules and Packages*
First, the indices module contains the NDWI/NDMI function to calculate NDMI/NDWI for individual rasters. Important packages to install include rasterio and fiona. The Indices module is then imported to the Live Fuel Moisture Module. The Average Annual Fuel Moisture Function calculates the SLFMC through the users raster series. The user can specify a shapefile for zonal statistics. This can be particularly helpful when looking at SLFMC between different extents and fuel types. It is important to note that the tools requires the installation of the rasterstats package to properly run zonal statistics. The user can also output a CSV with fuel moisture estimations for each raster in your series. The final output of this tool is a graph that shows the SLFMC of your identified extent and raster series. Provided is an example of an output SLFMC graph. Note that the error bars can provide an indicator of noise in your raster series, including the possibility of clouds obscuring the landscape and causing a miscalculation of ground NDMI. In addition, the user can output a multitemporal NDMI/NDWI raster stack through the Annual Live Fuel Moisture Raster Stack function. This is particularly helpful for those that wish to perform further analysis in a different GIS application, including ENVI or ArcGIS Pro.


## **Possible Applications**
#### *Suggested Applications*

Tracking of SLFMC for fire prone areas may provide a more thorough insight into how their fire regime may operate. This may be particularly helpful for long form studies examining the encroachment of invasive species post fire. How does SLFMC change due to the expansion of dry grass in Southern California Chaparral? The  multitemporal raster stack may provide an indication for when fuel loads changed. Variations in fuel age may be indicated by the SLFMC post fire.

## **Updates in the Future**

Future updates will allow users to plot separate SLFMC graphs for specified time frames. Restricting time frames may allow users to analyze shifts in SLFMC for numerous years. In addition, users may be provided the option to compare differing extents at the same type (i.e. different extents with different fuel loads or ages). Animations tracking changes in NDMI/NDWI will be provided in the near future











