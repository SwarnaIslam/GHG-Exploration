from datetime import datetime

import branca
import ee
import folium
import geemap.foliumap as geemap
import geocoder
import requests
import streamlit as st
from folium import Map, TileLayer
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("MiCASA DataSet View")

# Constants
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "micasa-carbonflux-monthgrid-v1"
asset_name = "rh"
color_map = "purd"
g = geocoder.ip("me")
current_location = g.latlng


# Load all items when the application is launched
@st.cache_data()
def load_map():
    items_response = requests.get(
        f"{STAC_API_URL}/collections/{collection_name}/items?limit=300"
    ).json()["features"]
    return {item["properties"]["start_datetime"][:10]: item for item in items_response}


items = load_map()

######### DATE BASED MAP ##########

# Get rescale values
rescale_values = {
    "max": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0][
        "histogram"
    ]["max"],
    "min": items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0][
        "histogram"
    ]["min"],
}

# Date picker
available_months = [
    datetime.strptime(date, "%Y-%m-%d").replace(day=1) for date in items.keys()
]
unique_months = sorted(set(available_months))

col1, col2 = st.columns(2)

with col1:
    date1 = st.date_input(
        "Select first date",
        min_value=min(available_months),
        max_value=max(available_months),
        value=min(available_months),
        format="YYYY-MM-DD",
    )
    date1 = date1.replace(day=1)

with col2:
    date2 = st.date_input(
        "Select second date",
        min_value=min(available_months),
        max_value=max(available_months),
        value=max(available_months),
        format="YYYY-MM-DD",
    )
    date2 = date2.replace(day=1)

# Ensure the day is always 1
selected_date1 = date1.replace(day=1)
selected_date2 = date2.replace(day=1)

# Convert selected date to string format
date1 = selected_date1.strftime("%Y-%m-%d")
date2 = selected_date2.strftime("%Y-%m-%d")


# Cache the tile fetching process
@st.cache_data
def get_tile_data(url):
    return requests.get(url).json()


# Get tile information for the selected date (with caching)
date1_tile = get_tile_data(
    f"{RASTER_API_URL}/collections/{items[date1]['collection']}/items/{items[date1]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}",
)

date2_tile = get_tile_data(
    f"{RASTER_API_URL}/collections/{items[date2]['collection']}/items/{items[date2]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}",
)

# Create two maps side by side

map_ = folium.plugins.DualMap(
    location=(current_location[0], current_location[1]),
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    zoom_start=6,
    min_zoom=4,
    max_zoom=8,
    attr="<a href=https://endless-sky.github.io/>Endless Sky</a>",
)


# # Define the first map layer with Rh level for the tile fetched for date 1
# The TileLayer library helps in manipulating and displaying raster layers on a map
map_layer_date1 = TileLayer(
    tiles=date1_tile["tiles"][0],  # Path to retrieve the tile
    attr="GHG",  # Set the attribution
    opacity=0.5,  # Adjust the transparency of the layer
    name=f"{date1} Rh Level",  # Title for the layer
    overlay=True,  # The layer can be overlaid on the map
    legendEnabled=True,  # Enable displaying the legend on the map
)

# Add the first layer to the Dual Map
map_layer_date1.add_to(map_.m1)


# Define the first map layer with Rh level for the tile fetched for date 2
map_layer_date2 = TileLayer(
    tiles=date2_tile["tiles"][0],  # Path to retrieve the tile
    attr="GHG",  # Set the attribution
    opacity=0.5,  # Adjust the transparency of the layer
    name=f"{date2} RH Level",  # Title for the layer
    overlay=True,  # The layer can be overlaid on the map
    legendEnabled=True,  # Enable displaying the legend on the map
)

# Add the second layer to the Dual Map
map_layer_date2.add_to(map_.m2)

# Display data markers (titles) on both maps
folium.Marker((current_location[0], current_location[1]), tooltip="both").add_to(map_)

# Add a layer control to switch between map layers
folium.LayerControl(collapsed=False).add_to(map_)

# Add a legend to the dual map using the 'branca' library.
# Note: the inserted legend is representing the minimum and maximum values for both tiles.
colormap = branca.colormap.linear.PuRd_09.scale(
    0, 0.3
)  # minimum value = 0, maximum value = 0.3 (gm Carbon/m2/daily)

# Classify the colormap according to specified Rh values
colormap = colormap.to_step(index=[0, 0.07, 0.15, 0.22, 0.3])

# Add the data unit as caption
colormap.caption = "Rh Values (gm Carbon/m2/daily)"

# Display the legend and caption on the map
colormap.add_to(map_.m1)

# Visualize the Dual Map
st_folium(map_, width=1600, height=600)


######### GENERIC MAP ##########
Map = geemap.Map()

# Add Earth Engine datasets
dataset = ee.ImageCollection("MODIS/MCD43A4_006_NDVI").filter(
    ee.Filter.date(date1, date2)
)

colorized = dataset.select("NDVI")

print(colorized)

vis_params = {
    "min": 0,
    "max": 1,
    "palette": [
        "ffffff",
        "ce7e45",
        "df923d",
        "f1b555",
        "fcd163",
        "99b718",
        "74a901",
        "66a000",
        "529400",
        "3e8601",
        "207401",
        "056201",
        "004c00",
        "023b01",
        "012e01",
        "011d01",
        "011301",
    ],
}

Map.setCenter(-7.03125, 31.0529339857, 2)
Map.addLayer(colorized, vis_params, "Colorized")
folium.LayerControl().add_to(Map)


st_folium(Map, width=1200, height=600)
