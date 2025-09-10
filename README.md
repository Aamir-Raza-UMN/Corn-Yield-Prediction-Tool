# 🌽 Corn-Yield-Prediction-Tool
<img src="PAC.png" alt="PAC Logo" width="240" height="240" style="display: inline-block; margin: 10px;">   <img src="USDA.png" alt="USDA Logo" width="240" height="240" style="display: inline-block; margin: 10px;">   <img src="NASA.png" alt="NASA Logo" width="240" height="240" style="display: inline-block; margin: 10px;">


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

- Use [Vegetation_Indices_L8.js](Vegetation_Indices_L8.js) in Google Earth Engine (GEE) to calculate vegetation indices for your region of interest.

- Provide area boundary input and select imagery from a consistent growth stage (e.g., 15–31 August for Minnesota).

- Export the results as GeoTIFF files.

- Open one GeoTIFF in ArcGIS or QGIS, calculate latitude/longitude for each pixel, and export as CSV (Lat, Lon, Value).

- Alternatively, you can automate this step in Python or directly in GEE.


**2. Soil Data**

- Use [download_polaris_soil_rasters.R](download_polaris_soil_rasters.R) to download POLARIS soil data for your region.

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

- Use [raster_point_extraction_and_data_merge.py](raster_point_extraction_and_data_merge.py) to extract numeric data from VIs, soil, and topography rasters.

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

<hr>

<h2>⚙️ Model Setup and Execution</h2>

<p>To run the model, download the base files from the following link:</p>
<p><a href="https://drive.google.com/drive/folders/1o-nj30ePG_8DWgCBAw8yOjwm_CjHq0Mb?usp=drive_link" target="_blank">📂 Model Base Files</a></p>

<p>
  Additionally, download the <a href="Tool.py">Tool.py</a> file and place it in the same folder as the base files.
</p>


<h3>🔧 File Path Configuration</h3>
<p>Right-click on <code>imputer.pkl</code>, copy its path, and update it in the code lines for all logos and model base files inside <code>Tool.py</code>. Save the file after editing.  
This can be done in Notepad or any Python-supported editor.</p>

<pre><code class="language-python">
logo1 = Image.open("C:/Users/araza/Desktop/Model_base_files/PAC.png").resize((150, 100))
logo2 = Image.open("C:/Users/araza/Desktop/Model_base_files/USDA.png").resize((120, 100))
logo3 = Image.open("C:/Users/araza/Desktop/Model_base_files/NASA.png").resize((120, 100))

model   = joblib.load("C:/Users/araza/Desktop/Model_base_files/stacking_model.pkl")
scaler  = joblib.load("C:/Users/araza/Desktop/Model_base_files/scaler.pkl")
imputer = joblib.load("C:/Users/araza/Desktop/Model_base_files/imputer.pkl")
</code></pre>

<h3>▶️ Running the Tool</h3>
<ol>
  <li>Open <strong>Command Prompt</strong>.</li>
  <li>Navigate to the folder containing the base files:
    <pre><code>cd C:\Users\araza\Desktop\Model_base_files</code></pre>
  </li>
  <li>Run the tool:
    <pre><code>python Tool.py</code></pre>
  </li>
</ol>
<p>The application will launch (see figure below). Keep the command prompt open while using the tool.</p>

<hr>

<!-- Tool UI Screenshot -->
<p align="center">
  <a href="Tool_UI.png">
    <img src="Tool_UI.png" alt="Corn Yield Prediction Tool – User Interface" width="900">
  </a>
  <br>
  <em>Figure: Corn Yield Prediction Tool – User Interface</em>
</p>


<h2>🖥️ Prototype Tool Implementation</h2>

<p>The prototype User Interface (UI) was designed to simplify the use of the corn yield prediction framework. The workflow involves the following steps:</p>

<ul>
  <li><strong>Upload Input Files</strong>:
    <ul>
      <li>CSV file with predictor (independent) variables (vegetation indices, lat/lon coordinates, soil, and topography).</li>
      <li>CSV file with daily weather parameters (precipitation, temperature, radiation, etc.).</li>
    </ul>
  </li>
  <li><strong>Data Cleaning</strong>:  
  The <em>Clean IVs</em> function automatically detects and handles missing or <code>NaN</code> values, ensuring consistency and reliability before modeling.</li>
  <li><strong>Select Prediction Year</strong>:  
  Users can choose the target year via a drop-down menu.</li>
  <li><strong>Predict Yield</strong>:  
  Clicking the <em>Predict Yield</em> button runs the model on the uploaded datasets and generates predictions.</li>
  <li><strong>Show Summary</strong>:  
  Displays descriptive statistics (mean, standard deviation, range) of the predicted yields.</li>
  <li><strong>Export Results</strong>:  
  Users can export predictions (Latitude, Longitude, Yield) as a CSV file, which can be mapped for spatial yield distribution analysis.</li>
</ul>

<hr>

<h2>🔬 Prototype Demonstration</h2>

<p>To operationalize the spatial regression (SR) framework, the <strong>Corn Yield Prediction Tool</strong> was developed with a graphical user interface (GUI). This makes the tool accessible to researchers, agronomists, and stakeholders without requiring programming expertise.</p>

<p>The GUI provides a step-by-step workflow:</p>
<ol>
  <li>Upload CSV files with vegetation indices, coordinates, soil/topographic variables, and daily weather data.</li>
  <li>The <em>Clean IVs</em> function ensures input integrity by handling missing values.</li>
  <li>Select the prediction year.</li>
  <li>Run predictions using the stacking regression model, which integrates environmental, soil, and vegetation predictors.</li>
  <li>Review descriptive statistics of predicted yields.</li>
  <li>Export results as CSV for mapping and spatial analysis of yield distributions.</li>
</ol>

<p>This prototype serves as a bridge between advanced machine learning models and practical agricultural applications. By unifying environmental, soil, and weather data into an intuitive workflow, it empowers stakeholders to query, analyze, and visualize regional yield forecasts effectively.</p>

<hr>

<hr>

<hr>

<h2>✍️ Authors</h2>

<div style="margin-bottom:20px;">
  <h3>Aamir Raza</h3>
  <p>PhD Student | Graduate Research Assistant<br>
  🌱 Precision Agriculture Center<br>
  📍 Department of Soil, Water, and Climate<br>
  University of Minnesota | St. Paul, MN 55108, USA</p>
</div>

<div style="margin-bottom:20px;">
  <h3>Yuxin Miao, Ph.D.</h3>
  <p> Professor of Precision Agriculture <br>
  🌱 Precision Agriculture Center<br>
  📍 Department of Soil, Water and Climate<br>
  University of Minnesota | St. Paul, MN 55108, USA</p>
</div>

<div style="margin-bottom:20px;">
  <h3>Dr. Yanbo Huang</h3>
  <p>Research Agricultural Engineer<br>
  📍 USDA-ARS Genetics and Sustainable Agriculture Research Unit<br>
  Mississippi State, MS 39762, USA</p>
</div>

<div style="margin-bottom:20px;">
  <h3>Junjun Lu</h3>
  <p>🌱 Precision Agriculture Center<br>
  📍 Department of Soil, Water and Climate<br>
  University of Minnesota | St. Paul, MN 55108, USA</p>
</div>

<div style="margin-bottom:20px;">
  <h3>Zhengwei Yang</h3>
  <p>📍 USDA-NASS Research and Development Division<br>
  Washington, D.C. 20250, USA</p>
</div>

<div style="margin-bottom:20px;">
  <h3>Rajat Bindlish</h3>
  <p>📍 NASA Goddard Space Flight Center<br>
  Greenbelt, MD 20771, USA</p>
</div>

<p><strong>📌 Correspondence:</strong><br>
<a href="mailto:ymiao@umn.edu">ymiao@umn.edu</a> ; 
<a href="mailto:yanbo.huang@usda.gov">yanbo.huang@usda.gov</a></p>

<hr>
