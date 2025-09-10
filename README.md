# 🌽 Corn-Yield-Prediction-Tool

This repository provides a complete workflow for predicting corn yield using vegetation indices, soil data, topography, and climate variables.  

---

## 📦 Requirements

Ensure you are using **Python 3.11.9** and have the following libraries installed:

```bash
python --version
# Python 3.11.9

pip install pandas==2.2.3 joblib==1.4.2 numpy==1.26.4 pillow==11.1.0 scipy==1.15.1 xgboost==3.0.2

```
## 📊 Data Preparation Workflow
**1. Vegetation Indices (VIs)**

Use Vegetation_Indices_L8.js in Google Earth Engine (GEE) to calculate vegetation indices for your region of interest.

Provide area boundary input and select imagery from a consistent growth stage (e.g., 15–31 August for Minnesota).

Export the results as GeoTIFF files.

Open one GeoTIFF in ArcGIS or QGIS, calculate latitude/longitude for each pixel, and export as CSV (Lat, Lon, Value).

Alternatively, you can automate this step in Python or directly in GEE.
