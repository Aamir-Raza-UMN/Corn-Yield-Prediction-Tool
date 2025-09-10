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

- Use Vegetation_Indices_L8.js in Google Earth Engine (GEE) to calculate vegetation indices for your region of interest.

- Provide area boundary input and select imagery from a consistent growth stage (e.g., 15–31 August for Minnesota).

- Export the results as GeoTIFF files.

- Open one GeoTIFF in ArcGIS or QGIS, calculate latitude/longitude for each pixel, and export as CSV (Lat, Lon, Value).

- Alternatively, you can automate this step in Python or directly in GEE.


**2. Soil Data**

- Use download_polaris_soil_rasters.R to download POLARIS soil data for your region.

- Extract three soil depths: 0–5 cm, 5–15 cm, 15–30 cm.

- Rename rasters with consistent variable names (e.g., 0_5_OM, 5-15_OM, 15-30_OM).

- Place them in the same folder as other variables.


**3. Topography Data**

- Download DEM for your study area.

- Derive terrain attributes:
Relative elevation, Slope, Aspect, Curvature, Topographic Wetness Index (TWI)

Formula for TWI:

<p><strong>TWI = ln(α / tanβ)</strong></p>
<p>where:</p>
<ul>
  <li><strong>α</strong> = upslope contributing area per unit width (m²/m)</li>
  <li><strong>β</strong> = local slope angle (radians)</li>
</ul>

**4. Data Integration**

- Use raster_point_extraction_and_data_merge.py to extract numeric data from VIs, soil, and topography rasters.

- Match datasets by VI pixel coordinates (Lat, Lon).

- Average soil depth variables into single values.

- Final merged CSV should include these columns:
```


MNDWI, TVI, EVI, NDWI, ELAI, NCMI, SR, GCI, CVI, GCVI, WDRVI, GNDVI, NDVI, ARVI,
Sand_%, Clay_%, Silt_%, OM_%, pH, BD_g/cm3, Ksat_cm/hr, HB_Kpa, MPSD, SPIPMPD, 
PSDI, RSWC, SSWC, Lat, Lon, TWI, Curvature, Slope, Relative_Elevation, Aspect
```

**5. Climate Data**

<u>Collect daily climate data:</u>

- **PAR_TOT** (Photosynthetically Active Radiation)
- **SW_DWN** (Surface Shortwave Downward Radiation)
- **Mean Temperature (TM)**, **Maximum (TM_MAX)**, **Minimum (TM_MIN)**
- **Precipitation**

<u>Derived Variables:</u>

**Corn Heat Units (CHU):** Adjusts min/max temperature thresholds (≥4.4°C and ≥10°C).

Daily CHU = average of adjusted min and max heat contributions.


<h3>Growing Degree Days (GDD)</h3>
<p><strong>GDD = (T<sub>max</sub> + T<sub>min</sub>) / 2 - 10</strong></p>
<p>Negative values are set to 0.</p>
<p><em>Widely used in crop growth modeling.</em></p>

<h3>Abundant and Well-Distributed Rainfall Index (AWDR)</h3>
<p><strong>AWDR = PPT × SDI</strong></p>
<p>where:</p>
<ul>
  <li>PPT = precipitation</li>
  <li>SDI = Shannon Diversity Index of rainfall distribution</li>
</ul>

<h3>Standardized Precipitation Index (SPI)</h3>
<p><strong>SPI = (x - x̄) / σ</strong></p>
<p>where:</p>
<ul>
  <li>x = observed precipitation</li>
  <li>x̄ = mean precipitation</li>
  <li>σ = standard deviation</li>
</ul>

## 📂 Final Data Output

- At the end of preparation, you should have two CSV files:

- Static variables → Vegetation Indices + Soil + Topography

- Dynamic variables → Climate features (CHU, GDD, AWDR, SPI, etc.)

These files are then used as inputs for the Corn-Yield-Prediction-Tool.
