import streamlit as st
import ee
import geemap.foliumap as geemap
import json
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    layout="wide",
)

# Authenticate and initialize Earth Engine
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, "keys.json")
ee.Initialize(credentials)


def get_geojson(output):
    eoJSON = any
    ok = 0

    # Check if the user has drawn any features (polygons, etc.) and output it as GeoJSON
    if output and output.get("all_drawings"):
        geojson_data = output["all_drawings"]

        # Convert GeoJSON to string
        geojson_str = json.dumps(geojson_data, indent=2)

        geoJSON = geojson_data
        # Display the GeoJSON data in Streamlit
        st.write("GeoJSON Data for the Polygon(s):")

        ok = 1

        return geoJSON[0]


world_geojson = {
    "type": "Feature",
    "properties": {"name": "World"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-180.0, -90.0],
                [180.0, -90.0],
                [180.0, 90.0],
                [-180.0, 90.0],
                [-180.0, -90.0],
            ]
        ],
    },
}

# Set title and layout for the app
st.title("Bangladesh LST Statistical Analysis Using MODIS Data")

# Step 1: Add start and end date picker inside a container for better layout control
with st.container():
    start_date = st.date_input("Select start date", value=datetime(2014, 8, 27))
    end_date = st.date_input("Select end date", value=datetime(2024, 9, 23))

# Step 2: Create an interactive map for region selection using geemap
st.write("Select a region on the map:")

# Create a layout with fixed height using st.columns()
col1, col2 = st.columns([3, 3])

# Map goes in one column
with col1:
    Map = geemap.Map(center=[23.6850, 90.3563], zoom=6)
    Map.add_basemap("ROADSIDE")
    map_output = st_folium(Map, height=600, width=700)  # Adjust the height here

# Results container in another column
with col2:
    
    # Check if the user has selected a region
    # if map_output and map_output.get("all_drawings"):
    geojson = get_geojson(map_output)
    st.code(geojson, language="json")
    aoi = ee.FeatureCollection(ee.Geometry(world_geojson["geometry"]))

    # Step 3: Load MODIS LST data
    modis = (
        ee.ImageCollection("MODIS/061/MOD11A1")
        .filterDate(str(start_date), str(end_date))
        .select("LST_Day_1km")
    )

    # Convert LST from Kelvin to Celsius
    modCel = modis.map(
        lambda img: img.multiply(0.02)
        .subtract(273.15)
        .copyProperties(img, ["system:time_start"])
    )

    # Function to group images by month and calculate monthly statistics
    def calculate_monthly_stats(collection, aoi):
        # Convert system:time_start to a formatted date (year-month)
        def set_month(image):
            date = ee.Date(image.get("system:time_start"))
            month = date.format("YYYY-MM")
            return image.set("month", month)

        # Apply the function to each image in the collection
        collection = collection.map(set_month)

        # Group by month and compute monthly mean
        months = ee.List(collection.aggregate_array("month")).distinct()

        def monthly_mean(month):
            # Filter images for the current month
            monthly_images = collection.filter(ee.Filter.eq("month", month))

            # Calculate mean for each month
            mean_image = monthly_images.mean()

            # Calculate statistics (mean, min, max, std) for each month
            stats = mean_image.reduceRegion(
                reducer=ee.Reducer.mean()
                .combine(ee.Reducer.minMax(), sharedInputs=True)
                .combine(ee.Reducer.stdDev(), sharedInputs=True),
                geometry=aoi.geometry(),
                scale=1000,
                maxPixels=1e9,
            )

            # st.write("DONE ", month)

            # Return a feature with the month and stats
            return ee.Feature(None, stats.set("month", month))

        # Map over the months and return a FeatureCollection
        monthly_stats_fc = ee.FeatureCollection(months.map(monthly_mean))
        return monthly_stats_fc

    # Use the modified function to calculate monthly stats
    monthly_stats_fc = calculate_monthly_stats(modCel, aoi)

    # Convert the FeatureCollection to a list of dictionaries
    monthly_stats = monthly_stats_fc.getInfo()

    # Step 4: Extract stats and create a Pandas DataFrame
    months = []
    means = []
    mins = []
    maxs = []
    std_devs = []

    for feature in monthly_stats["features"]:
        prop = feature["properties"]
        months.append(prop["month"])
        means.append(prop["LST_Day_1km_mean"])
        mins.append(prop["LST_Day_1km_min"])
        maxs.append(prop["LST_Day_1km_max"])
        std_devs.append(prop["LST_Day_1km_stdDev"])

    # Create a Pandas DataFrame with the monthly data
    df = pd.DataFrame(
        {
            "Month": months,
            "Average Temp (°C)": means,
            "Min Temp (°C)": mins,
            "Max Temp (°C)": maxs,
            "Std Dev (°C)": std_devs,
        }
    )

    # Display the DataFrame in Streamlit
    st.write("Monthly LST Statistics for the selected region:")
    st.dataframe(df, height=400)

    # # Function to calculate daily stats for each image
    # def calculate_daily_stats(image):
    #     stats = image.reduceRegion(
    #         reducer=ee.Reducer.mean()
    #         .combine(ee.Reducer.minMax(), sharedInputs=True)
    #         .combine(ee.Reducer.stdDev(), sharedInputs=True),
    #         geometry=aoi.geometry(),
    #         scale=1000,
    #         maxPixels=1e9,
    #     )
    #     # Add the date as a property to the image stats
    #     return ee.Feature(
    #         None,
    #         stats.set(
    #             "date", ee.Date(image.get("system:time_start")).format("YYYY-MM-dd")
    #         ),
    #     )

    # # Map the function over each image in the collection
    # daily_stats_fc = modCel.map(calculate_daily_stats)

    # # Convert the FeatureCollection to a list of dictionaries
    # daily_stats = daily_stats_fc.getInfo()

    # # Step 4: Extract stats and create a Pandas DataFrame
    # dates = []
    # means = []
    # mins = []
    # maxs = []
    # std_devs = []

    # for feature in daily_stats["features"]:
    #     prop = feature["properties"]
    #     dates.append(prop["date"])
    #     means.append(prop["LST_Day_1km_mean"])
    #     mins.append(prop["LST_Day_1km_min"])
    #     maxs.append(prop["LST_Day_1km_max"])
    #     std_devs.append(prop["LST_Day_1km_stdDev"])

    # # Create a Pandas DataFrame with the daily data
    # df = pd.DataFrame(
    #     {
    #         "Date": dates,
    #         "Mean Temp (°C)": means,
    #         "Min Temp (°C)": mins,
    #         "Max Temp (°C)": maxs,
    #         "Std Dev (°C)": std_devs,
    #     }
    # )

    # # Display the DataFrame in Streamlit
    # st.write("Daily LST Statistics for the selected region:")
    # st.dataframe(df, height=400)  # Adjust table height here
