import ee
import os
from dotenv import load_dotenv
load_dotenv()
# Authenticate and initialize Earth Engine
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, "keys.json")
ee.Initialize(credentials)

# Define a region of interest (e.g., Bangladesh boundary)
roi = ee.Geometry.Rectangle([88.0, 20.6, 92.7, 26.6])

# Define the MODIS dataset and year
year = "2023"  # Change this to the desired year
start_date = f"{year}-01-01"
end_date = f"{year}-12-31"

# Define the MODIS dataset
modis = (
    ee.ImageCollection("MODIS/061/MOD11A1")
    .filterDate(start_date, end_date)
    .select("LST_Day_1km")
)


# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(image):
    return (
        image.multiply(0.02)
        .subtract(273.15)
        .copyProperties(image, ["system:time_start"])
    )


modis_celsius = modis.map(kelvin_to_celsius)

# Calculate mean temperature over the year
mean_temp = modis_celsius.mean().reduceRegion(
    reducer=ee.Reducer.mean(), geometry=roi, scale=1000, maxPixels=1e13
)

# Fetch the results
print("Mean Yearly Temperature (°C):", mean_temp.getInfo())
