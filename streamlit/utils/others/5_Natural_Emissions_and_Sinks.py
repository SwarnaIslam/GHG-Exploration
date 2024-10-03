import json
import os
from datetime import datetime
from urllib import response

import branca
import ee
import folium
import folium.plugins as plugins
import geemap.foliumap as geemap
import pandas as pd
import requests
import streamlit as st
from pyexpat import features
from streamlit_folium import st_folium
from keys import credentials_json
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")
with open("styles.css") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)

############ CONSTANTS ##############
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
gosat_tile = "https://earth.gov/ghgcenter/api/raster/collections/gosat-based-ch4budget-yeargrid-v1/items/gosat-based-ch4budget-yeargrid-v1-2019/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=prior-total&color_formula=gamma+r+1.05&colormap_name=rainbow&rescale=0.0%2C2.121816635131836"
micasa_tile = "https://earth.gov/ghgcenter/api/raster/collections/micasa-carbonflux-monthgrid-v1/items/micasa-carbonflux-monthgrid-v1-201201/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=rh&color_formula=gamma+r+1.05&colormap_name=purd&rescale=-0.3509398102760315%2C6.5816521644592285"

asset_name = "rh"


############ METHODS ###############
@st.cache_data
def generate_stats(item, geojson):

    # A POST request is made to submit the data associated with the item of interest (specific observation) within the Dallas, TX boundaries to compute its statistics
    result = requests.post(
        # Raster API Endpoint for computing statistics
        f"{RASTER_API_URL}/cog/statistics",
        # Pass the URL to the item, asset name, and raster identifier as parameters
        params={"url": item["assets"][asset_name]["href"]},
        # Send the GeoJSON object (Dallas, TX polygon) along with the request
        json=geojson,
        # Return the response in JSON format
    ).json()

    print(result["properties"])

    return {
        **result["properties"],
        "datetime": item["properties"]["start_datetime"][:7],
    }


def clean_stats(stats_json) -> pd.DataFrame:

    # Normalize the JSON data
    df = pd.json_normalize(stats_json)

    # Replace the naming "statistics.b1" in the columns
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]

    # Set the datetime format
    df["date"] = pd.to_datetime(df["datetime"])

    # Return the cleaned format
    return df


############ MAIN FUNCTION ##############

# Initialize the Streamlit app
st.title("Natural Emissions and Sinks Visualization")
st.write(
    "This app visualizes methane emissions and natural sources (like wetlands) using satellite data."
)

# Add interpretive information for users
with st.expander("How to Interpret This Map"):
    st.write(
        """
        This map displays two layers representing methane emissions data:
        
        - **GOSAT-based Methane Emissions (Top Layer):** 
            - This layer shows methane emissions derived from satellite observations.
            - Areas with **brighter colors** indicate higher methane emissions. 
            - This dataset includes total emissions from both natural sources (like wetlands) and human activities (like agriculture and industry).
            
        - **MICASA Dataset (Bottom Layer):** 
            - This layer provides ground-based measurements of methane emissions.
            - It highlights specific emission sources and local variations.
            - Brighter areas indicate higher measured emissions, giving a detailed view of methane sources in specific regions.
        """
    )
col1, col2 = st.columns([2, 2])

with col1:
    # Initialize the leafmap map
    m = geemap.Map(center=[0, 0], zoom=2, google_map="HYBRID")

    # Add the TileJSON layers
    folium.TileLayer(
        tiles=gosat_tile,
        name="GOSAT-based Emissions",
        attr="NASA EMIT",
        opacity=0.6,
        overlay=True,
        legendEnabled=True,
    ).add_to(m)

    folium.TileLayer(
        tiles=micasa_tile,
        name="MICASA",
        attr="MICASA",
        opacity=0.6,
        overlay=True,
        legendEnabled=True,
    ).add_to(m)

    # Add a layer control to switch between map layers
    folium.LayerControl(collapsed=False).add_to(m)

    # Add a color map
    colormap = branca.colormap.linear.PuRd_09.scale(0, 2.1218)
    colormap = colormap.to_step(index=[0, 0.5, 1.0, 1.5, 2.0, 2.1218])
    colormap.caption = "Methane Emissions (CH4 - kg/m²/year)"
    colormap.add_to(m)

    # Display the map in Streamlit and capture drawing data
    output = st_folium(m, height=600, width=800)

with col2:

    geoJSON = any
    ok = 0

    # Check if the user has drawn any features (polygons, etc.) and output it as GeoJSON
    if output and output.get("all_drawings"):
        geojson_data = output["all_drawings"]

        # Convert GeoJSON to string
        geojson_str = json.dumps(geojson_data, indent=2)

        geoJSON = geojson_data
        # Display the GeoJSON data in Streamlit
        st.write("GeoJSON Data for the Polygon(s):")
        st.code(geojson_str, language="json")
        ok = 1

    #     # Create a downloadable link for the GeoJSON  ;; extra if we need this one
    #     st.download_button(
    #         label="Download GeoJSON as Text File",
    #         data=geojson_str,
    #         file_name="polygon_data.txt",
    #         mime="text/plain",
    #     )

    # # if we want to store it in the system
    # #  the file path where the GeoJSON will be saved
    # file_path = os.path.join("**path**", "polygon_data.geojson")

    # # Write the GeoJSON to a file
    # with open(file_path, "w") as geojson_file:
    #     geojson_file.write(geojson_str)

#################################################   checking 👍  #########################################

collection_name = "micasa-carbonflux-monthgrid-v1"
world_bbox = [-180.0, -90.0, 179.99999999999994, 90.0]
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

sample_geojson = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [84.023438, 2.460181],
                [84.023438, 40.979898],
                [124.453125, 40.979898],
                [124.453125, 2.460181],
                [84.023438, 2.460181],
            ]
        ],
    },
}

# https://earth.gov/ghgcenter/api/stac/collections/micasa-carbonflux-monthgrid-v1/items?limit=5
# https://earth.gov/ghgcenter/api/stac/collections/oco2-mip-co2budget-yeargrid-v1/items?limit=6

# url = f"{STAC_API_URL}/collections/{collection_name}/items?limit=5"
url = f"{STAC_API_URL}/collections/oco2-mip-co2budget-yeargrid-v1/items?limit=5"
st.write("URL ", url)

items = requests.get(url).json()["features"]

# Print the total number of items (granules) found
print(f"Found {len(items)} items")
st.write(items[0]["assets"]["ff"]["raster:bands"][0]["statistics"])
st.write(items[0]["properties"])

# stats = [generate_stats(item, geojson_data[0]) for item in items]     # this is for dynammically selected geojson, it must have [0] to get the geojson value
stats = [generate_stats(item, sample_geojson) for item in items]
st.markdown("##Generated stats")
st.write(stats)

df = clean_stats(stats)
st.table(df.head(3))
