from datetime import date, datetime
import os
import ee
import folium
import geemap.foliumap as geemap
import streamlit as st
from streamlit_folium import st_folium
from keys import credentials_json
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")
with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.title("Vegetation Index Data")

############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)

############ WIDGET ##############

# Define a range of dates (you can adjust this as needed)
start_date = date(2000, 2, 24)
end_date = date(2023, 2, 10)

# Create date pickers
date1 = st.date_input(
    "Select start date", start_date, min_value=start_date, max_value=end_date
)
date2 = st.date_input(
    "Select end date", end_date, min_value=start_date, max_value=end_date
)

# Ensure the day is always 1
selected_date1 = date1.replace(day=1)
selected_date2 = date2.replace(day=1)

# Convert selected date to string format
date1_str = selected_date1.strftime("%Y-%m-%d")
date2_str = selected_date2.strftime("%Y-%m-%d")

st.write(date1_str)
st.write(date2_str)


############ MAP CONFIG ##############

Map = geemap.Map()

# Add Earth Engine datasets
dataset = ee.ImageCollection("MODIS/MCD43A4_006_NDVI").filter(
    ee.Filter.date(date1_str, date2_str)
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
