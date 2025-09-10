// Load your Field Boundary
var aoi = ee.FeatureCollection("projects/ee-araza/assets/Dusty_Brennan");

// Center the map on the AOI
Map.centerObject(aoi);


// Define the time range
var startDate = '2023-08-15';
var endDate = '2023-08-20';

function maskClouds(image) {
  // Extract the QA_PIXEL band
  var qa = image.select('QA_PIXEL');
  
  // Cloud and shadow masking (bit 3: cloud, bit 4: cloud shadow)
  var cloudShadowMask = qa.bitwiseAnd(1 << 3).eq(0) // No cloud (bit 3)
                        .and(qa.bitwiseAnd(1 << 4).eq(0)); // No cloud shadow (bit 4)
  
  // Apply the mask to the image
  return image.updateMask(cloudShadowMask);
}

// Load and filter Landsat 8 imagery
var landsat8Collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_TOA')
  .filterBounds(aoi)
  .filterDate(startDate, endDate)
  .map(maskClouds)
  .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10']); // B2:Blue, B3:Green, B4:Red, B5:NIR, B6:SWIR1, B7:SWIR2, B10:Thermal

print('Number of images:', landsat8Collection.size());

// Get the dates of available images
var imageDates = landsat8Collection.aggregate_array('system:time_start')
  .map(function(time) {
    return ee.Date(time).format('YYYY-MM-dd');
  });

print('Available Landsat 8 Image Dates:', imageDates);

// Create a median composite
var composite = landsat8Collection.median().clip(aoi);

// Compute vegetation indices (excluding those requiring red-edge band)
var indices = composite.addBands([
  // 1. NDVI
  composite.expression(
    '(NIR - RED) / (NIR + RED)', {
      'NIR': composite.select('B5').divide(10),
      'RED': composite.select('B4').divide(10)
    }).rename('NDVI'),
  
  // 2. EVI
  composite.expression(
    '2.5 * (NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1)', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4'),
      'BLUE': composite.select('B2')
    }).rename('EVI'),

  // 3. GNDVI
  composite.expression(
    '(NIR - GREEN) / (NIR + GREEN)', {
      'NIR': composite.select('B5'),
      'GREEN': composite.select('B3')
    }).rename('GNDVI'),

  // 4. WDRVI (with alpha=0.2)
  composite.expression(
    '0.2 * (NIR - RED) / (0.2 * NIR + RED)', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4')
    }).rename('WDRVI'),

  // 5. SR
  composite.expression(
    'NIR / RED', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4')
    }).rename('SR'),

  // 6. GCI
  composite.expression(
    '(NIR / GREEN) - 1', {
      'NIR': composite.select('B5'),
      'GREEN': composite.select('B3')
    }).rename('GCI'),

  // 7. CVI
  composite.expression(
    'NIR * RED / (GREEN * GREEN)', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4'),
      'GREEN': composite.select('B3')
    }).rename('CVI'),

  // 8. NCMI
  composite.expression(
    '(NIR - (GREEN - RED)) / (NIR + (GREEN + RED))', {
      'NIR': composite.select('B5'),
      'GREEN': composite.select('B3'),
      'RED': composite.select('B4')
    }).rename('NCMI'),

  // 9. NDWI (using SWIR1)
  composite.expression(
    '(NIR - SWIR1) / (NIR + SWIR1)', {
      'NIR': composite.select('B5'),
      'SWIR1': composite.select('B6')
    }).rename('NDWI'),

  // 10. MNDWI
  composite.expression(
    '(GREEN - SWIR1) / (GREEN + SWIR1)', {
      'GREEN': composite.select('B3'),
      'SWIR1': composite.select('B6')
    }).rename('MNDWI'),

  // 11. ARVI
  composite.expression(
    '(NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4'),
      'BLUE': composite.select('B2')
    }).rename('ARVI'),

  // 12. GCVI
  composite.expression(
    '(NIR / GREEN) - 1', {
      'NIR': composite.select('B5'),
      'GREEN': composite.select('B3')
    }).rename('GCVI'),

  // 13. TVI
  composite.expression(
    'sqrt((NIR - RED) / (NIR + RED) + 0.5)', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4')
    }).rename('TVI'),

  // 14. ELAI
  composite.expression(
    '0.57 * exp(2.33 * ((NIR - RED) / (NIR + RED)))', {
      'NIR': composite.select('B5'),
      'RED': composite.select('B4')
    }).rename('ELAI')
]);

// Add layers to the map
Map.addLayer(aoi, {}, 'AOI');

// Add each vegetation index to the map with appropriate visualization parameters
Map.addLayer(indices.select('NDVI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'NDVI');
Map.addLayer(indices.select('EVI'), {min: 0, max: 1, palette: ['red', 'yellow', 'green']}, 'EVI');
Map.addLayer(indices.select('GNDVI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'GNDVI');
Map.addLayer(indices.select('WDRVI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'WDRVI');
Map.addLayer(indices.select('SR'), {min: 0, max: 10, palette: ['blue', 'white', 'green']}, 'SR');
Map.addLayer(indices.select('GCI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'GCI');
Map.addLayer(indices.select('CVI'), {min: 0, max: 10, palette: ['blue', 'white', 'green']}, 'CVI');
Map.addLayer(indices.select('NCMI'), {min: -1, max: 1, palette: ['blue', 'white', 'green']}, 'NCMI');
Map.addLayer(indices.select('NDWI'), {min: -1, max: 1, palette: ['blue', 'white', 'brown']}, 'NDWI');
Map.addLayer(indices.select('MNDWI'), {min: -1, max: 1, palette: ['blue', 'white', 'brown']}, 'MNDWI');
Map.addLayer(indices.select('ARVI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'ARVI');
Map.addLayer(indices.select('GCVI'), {min: -1, max: 1, palette: ['red', 'yellow', 'green']}, 'GCVI');
Map.addLayer(indices.select('TVI'), {min: 0, max: 2, palette: ['red', 'yellow', 'green']}, 'TVI');
Map.addLayer(indices.select('ELAI'), {min: 0, max: 10, palette: ['blue', 'white', 'green']}, 'ELAI');
Map.addLayer(composite, {min: 0, max: 0.3, bands: ['B4', 'B3', 'B2']}, 'True Color Composite');

// Function to export each index as a GeoTIFF
function exportIndex(image, indexName) {
  Export.image.toDrive({
    image: image,
    description: indexName + '_L8_2018',
    folder: 'redwood_2023',
    fileNamePrefix: indexName,
    region: aoi,
    scale: 30, // Landsat 8 resolution
    crs: 'EPSG:4326',
    maxPixels: 1e13
  });
}

// Export each vegetation index
exportIndex(indices.select('NDVI'), 'NDVI');
exportIndex(indices.select('EVI'), 'EVI');
exportIndex(indices.select('GNDVI'), 'GNDVI');
exportIndex(indices.select('WDRVI'), 'WDRVI');
exportIndex(indices.select('SR'), 'SR');
exportIndex(indices.select('GCI'), 'GCI');
exportIndex(indices.select('CVI'), 'CVI');
exportIndex(indices.select('NCMI'), 'NCMI');
exportIndex(indices.select('NDWI'), 'NDWI');
exportIndex(indices.select('MNDWI'), 'MNDWI');
exportIndex(indices.select('ARVI'), 'ARVI');
exportIndex(indices.select('GCVI'), 'GCVI');
exportIndex(indices.select('TVI'), 'TVI');
exportIndex(indices.select('ELAI'), 'ELAI');
