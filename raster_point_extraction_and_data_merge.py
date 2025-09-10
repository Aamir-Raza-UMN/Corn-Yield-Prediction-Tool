# =============================
# Part 1: Extract raster values at given points
# =============================

import os
import pandas as pd
import geopandas as gpd
import rasterio
import numpy as np

# Step 1: Load the CSV file containing latitude and longitude points
csv_path = "R:/Aamir Raza/NASA, USDA  work Data/County  Level/Points/Points_part1.csv"
points_df = pd.read_csv(csv_path)

# Step 2: Convert the CSV into a GeoDataFrame (spatial points with geometry)
# CRS = EPSG:4326 means WGS84 (Lat/Lon)
gdf = gpd.GeoDataFrame(
    points_df,
    geometry=gpd.points_from_xy(points_df["Lon"], points_df["Lat"]),
    crs="EPSG:4326"
)

# Make sure CRS is correct (still WGS84 in this case)
gdf = gdf.to_crs(epsg=4326)

# Step 3: Find all raster (.tif) files in the given directory
raster_directory = "R:/Aamir Raza/NASA, USDA  work Data/County  Level/Topography"
raster_files = [
    os.path.join(raster_directory, f)
    for f in os.listdir(raster_directory)
    if f.endswith(".tif")
]

# Step 4: Function to extract raster values at each point
def extract_values(raster_file, gdf):
    with rasterio.open(raster_file) as src:
        # Get coordinates of points
        coords = [(x, y) for x, y in zip(gdf.geometry.x, gdf.geometry.y)]
        # Sample raster values at each coordinate
        values = [src.sample([coord]).__next__()[0] for coord in coords]
        # Replace missing values (-999) with NaN
        values = [np.nan if v == -999 else v for v in values]
        return values

# Step 5: Extract data from all rasters and store in a dictionary
extracted_data = {}
for raster_file in raster_files:
    extracted_data[os.path.basename(raster_file)] = extract_values(raster_file, gdf)

# Step 6: Combine extracted values into a DataFrame
extracted_df = pd.DataFrame(extracted_data)

# Add original Lat/Lon to the final DataFrame
extracted_df["latitude"] = gdf["Lat"]
extracted_df["longitude"] = gdf["Lon"]

# Step 7: Save results to a new CSV file
output_path = "R:/Aamir Raza/NASA, USDA  work Data/County  Level/Points/Part1_Topography.csv"
extracted_df.to_csv(output_path, index=False)

print("✅ Raster extraction complete. Data saved to:", output_path)


# =============================
# Part 2: Combine multiple datasets (Indices, Yield, Soil, Topography, Soil Optix)
# =============================

import dask.dataframe as dd

# Step 1: Load all CSV files using Dask (handles large data efficiently)
Indices = dd.read_csv('R:/Aamir Raza/NASA Paper Data/2021/East Field/Indices/S2/2021_07_01.csv')
yield_data = dd.read_csv('R:/Aamir Raza/NASA Paper Data/2021/East Field/Yield, Topography, Polaris, Soil Optix/Yield.csv')
soil_data = dd.read_csv('R:/Aamir Raza/NASA Paper Data/2021/East Field/Yield, Topography, Polaris, Soil Optix/Polaris_sorted_.csv')
topography = dd.read_csv('R:/Aamir Raza/NASA Paper Data/2021/East Field/Yield, Topography, Polaris, Soil Optix/Topography.csv')
Sop = dd.read_csv('R:/Aamir Raza/NASA Paper Data/2021/East Field/Yield, Topography, Polaris, Soil Optix/Soil Optix.csv')

# Step 2: Standardize column names for merging
# Ensure that all datasets have 'Lat' and 'Lon' as coordinate columns
Indices = Indices.rename(columns={'latitude': 'Lat', 'longitude': 'Lon'})

# Step 3: Merge all datasets on Lat/Lon
# Outer join ensures no data is lost (keeps all points even if some datasets are missing values)
df_merged = (
    Indices.merge(yield_data, on=['Lat', 'Lon'], how='outer')
           .merge(soil_data, on=['Lat', 'Lon'], how='outer')
           .merge(topography, on=['Lat', 'Lon'], how='outer')
           .merge(Sop, on=['Lat', 'Lon'], how='outer')
)

# Step 4: Save merged dataset to CSV
output_merged = 'R:/Aamir Raza/NASA Paper Data/2021/East Field/Merged/S2/S2_07_01_21.csv'
df_merged.compute().to_csv(output_merged, index=False)

print("✅ Data merging complete. Merged dataset saved to:", output_merged)
