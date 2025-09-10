# ------------------------------------------------------------
# Required Libraries
# ------------------------------------------------------------
# sf       : For handling vector data (e.g., shapefiles, GeoJSON).
# raster   : For working with raster data (e.g., GeoTIFFs).
# XPolaris : For accessing and downloading POLARIS soil property rasters.
# ------------------------------------------------------------
library(sf)
library(raster)
library(XPolaris)

# ------------------------------------------------------------
# Function: download_soil_rasters
# ------------------------------------------------------------
# Purpose:
#   - Reads an AOI (Area of Interest) shapefile.
#   - Converts AOI polygons into centroid points.
#   - Uses the centroids to query POLARIS soil database.
#   - Downloads soil rasters for specified variables, depths, and statistics.
#   - Saves the results as GeoTIFF files in a local folder.
#
# Arguments:
#   shapefile_path : Path to your AOI shapefile (e.g., "C:/data/aoi.shp").
#   statistics     : Soil data statistics to request (e.g., mean, p5, p95).
#   variables      : Soil properties to extract:
#                     - ph       : Soil pH
#                     - om       : Organic matter
#                     - clay     : Clay fraction
#                     - sand     : Sand fraction
#                     - silt     : Silt fraction
#                     - bd       : Bulk density
#                     - hb       : Bubbling pressure head
#                     - n        : Pore size distribution
#                     - alpha    : Alpha parameter
#                     - ksat     : Saturated hydraulic conductivity
#                     - lambda   : Pore connectivity
#                     - theta_r  : Residual water content
#                     - theta_s  : Saturated water content
#   layersdepths   : Depth layers in cm (default = "0_5", "5_15", "15_30").
#   output_folder  : Folder where GeoTIFF files will be saved.
#
# Returns:
#   A data frame with metadata and local file paths for downloaded rasters.
# ------------------------------------------------------------
download_soil_rasters <- function(shapefile_path, 
                                  statistics = c('mean'), 
                                  variables = c('ph', 'om', 'clay', 'sand', 'silt', 
                                                'bd', 'hb', 'n', 'alpha', 'ksat', 
                                                'lambda', 'theta_r', 'theta_s'), 
                                  layersdepths = c('0_5', '5_15', '15_30'), 
                                  output_folder = "R:/Aamir Raza/NASA, USDA  work Data/County  Level/POLARIS2") {
  
  # ------------------------------------------------------------
  # Step 1: Read the AOI shapefile
  # ------------------------------------------------------------
  aoi <- st_read(shapefile_path)
  
  # Step 2: Fix invalid geometries (e.g., self-intersections in polygons)
  aoi <- st_make_valid(aoi)
  
  # Step 3: Convert AOI polygons into centroid points
  # POLARIS data is queried by points, so we use centroids.
  aoi_centroids <- st_centroid(aoi)
  
  # Step 4: Extract coordinates (latitude & longitude) of centroids
  locations <- data.frame(
    ID = paste0("LOC_", seq_len(nrow(aoi_centroids))),  # Unique ID for each location
    lat = st_coordinates(aoi_centroids)[, 2],          # Latitude
    long = st_coordinates(aoi_centroids)[, 1]          # Longitude
  )
  
  # Step 5: Ensure the output folder exists
  if (!dir.exists(output_folder)) {
    dir.create(output_folder, recursive = TRUE)
  }
  
  # ------------------------------------------------------------
  # Step 6: Download POLARIS soil rasters
  # ------------------------------------------------------------
  # - ximages() fetches soil data from POLARIS API
  # - Saves results as GeoTIFF files in the specified output folder
  df_ximages <- ximages(locations = locations,
                        statistics = statistics,
                        variables = variables,
                        layersdepths = layersdepths,
                        localPath = normalizePath(output_folder, winslash = "/"))
  
  # Step 7: Print paths of downloaded GeoTIFFs
  downloaded_files <- df_ximages$local_file
  message("Downloaded raster GeoTIFF images are stored in: ", output_folder)
  print(downloaded_files)
  
  return(df_ximages)
}

# ------------------------------------------------------------
# Example Usage
# ------------------------------------------------------------
# Replace the path below with your shapefile path.
# The function will download rasters for pH, organic matter, texture, 
# bulk density, and hydraulic properties for 3 depth layers (0–5, 5–15, 15–30 cm).
# Results will be saved to the specified output folder.
# ------------------------------------------------------------
download_soil_rasters("R:/Aamir Raza/NASA, USDA  work Data/County  Level/for_soil.shp")
