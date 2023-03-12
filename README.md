# SLFMC
SLFMC: Seasonal Live Fuel Moisture Content. A python package for analyzing seasonal fluctuations of live fuel moisture content through satellite imagery

## **Background**

#### *What is Live Fuel Moisture Content (LFMC)?*
  LFMC is an estimation of water content within plants. It is expressed as a ratio of water content in fresh plant tissue to its dry weight (Pivovaroff et al. 2019) and is measured by collecting samples of vegetation on the ground. 

#### *Why is it Important?*
  LFMC is a key component for wildfire spread and ignition since moisture reduces the flammability of vegetation, subsequently lowering the possibility of wildfire progression (Pivovaroff et al. 2019). For ignition to occur, vegetation must reach a critical fuel moisture threshold. For the graph provided by Pivovaroff et al., LFMC exhibits a seasonal trend due to variations in precipitation. During the Summer and Fall, precipitation decreases in southern California and LFMC of chaparral (vegetation) reaches its critical threshold for ignition, increasing fire risk. 

<img src="https://github.com/amcfaddenGIS/SLFMC/blob/main/LFM.jpg" width = "600" height = "400" alt="Seasonal Live Fuel Moisture (Pivovaroff et al. 2019)" title="Seasonal Live Fuel Moisture (Pivovaroff et al. 2019)">

#### *How do we effectively estimate it through Remote Sensing?*
Wildfire researchers have pursued research methods that implement remote sensed imagery to estimate LFMC, specifically vegetation indices. Vegetation indices use the electromagnetic information (reflectance or absorption) of vegetation to determine vegetative properties, including biomass, plant health and fuel moisture (Xue and Su 2017). For estimating vegetation moisture, Gao et al. developed the Normalized Difference Water Index (NDWI). NDWI is also known as the Normalized Difference Moisture Index (NDMI). NDWI uses shortwave infrared (SWIR) and near infrared reflectance (NIR) to estimate vegetation moisture in vegetation: (SWIR-NIR/SWIR+NIR). Since NDWI is capable of estimating vegetation moisture, researchers have adopted it to determine LFMC of varying vegetation types.  Dennison et al. (2005) noted that NDWI was positively correlated with ground measurements of LFMC (Southern California Chaparral), suggesting it can effectively estimate NDWI. Dennison et al. also acknowledges the possibility of measuring seasonal variations in LFMC through NDWI. 
