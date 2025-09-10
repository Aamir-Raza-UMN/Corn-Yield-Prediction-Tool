library(sf)       # For handling shapefiles
library(raster)   # For working with raster data
library(XPolaris) # For accessing POLARIS soil data

# Function to download soil rasters for a given AOI shapefile
download_soil_rasters <- function(shapefile_path, 
                                  statistics = c('mean'), 
                                  variables = c('ph', 'om', 'clay', 'sand', 'silt', 'bd', 'hb', 'n', 'alpha', 'ksat', 'lambda', 'theta_r', 'theta_s'), 
                                  layersdepths = c('0_5', '5_15', '15_30'), 
                                  output_folder = "R:/Aamir Raza/NASA, USDA  work Data/County  Level/POLARIS2") {
  

  # Read AOI shapefile
  aoi <- st_read(shapefile_path)
  
  # Fix invalid geometries
  aoi <- st_make_valid(aoi)
  
  # Convert AOI to centroid points for soil extraction
  aoi_centroids <- st_centroid(aoi)
  
  # Extract coordinates for all features
  locations <- data.frame(
    ID = paste0("LOC_", seq_len(nrow(aoi_centroids))),
    lat = st_coordinates(aoi_centroids)[, 2],
    long = st_coordinates(aoi_centroids)[, 1]
  )
  
  # Ensure the output folder exists
  if (!dir.exists(output_folder)) {
    dir.create(output_folder, recursive = TRUE)
  }
  
  # Download POLARIS images as GeoTIFFs (Fix the storage path issue)
  df_ximages <- ximages(locations = locations,
                        statistics = statistics,
                        variables = variables,
                        layersdepths = layersdepths,
                        localPath = normalizePath(output_folder, winslash = "/"))
  
  # Print the paths of downloaded files
  downloaded_files <- df_ximages$local_file
  message("Downloaded raster GeoTIFF images are stored in: ", output_folder)
  print(downloaded_files)
  
  return(df_ximages)
}

# Example usage
download_soil_rasters("R:/Aamir Raza/NASA, USDA  work Data/County  Level/for_soil.shp")

