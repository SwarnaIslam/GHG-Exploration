import datetime
import json
import os
import warnings
from datetime import date

import ee

# import fiona
import folium
import geemap.colormaps as cm
import geemap.foliumap as geemap
import geocoder
import geopandas as gpd
import requests
import streamlit as st
from folium import GeoJson
from shapely.geometry import Polygon
from utils.get_current_weather import get_weather_and_aqi_data
from streamlit_folium import st_folium

import streamlit as st
import datetime
from keys import credentials_json



# Streamlit page configuration
st.set_page_config(
    page_title="GHG Earth Explorer",
    page_icon="🌍",
    layout="wide",
)
st.sidebar.image(image="streamlit/static/gex_logo.png")

with open("streamlit/styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Initialize Google Earth Engine
service_account = st.secrets["general"]["GEE_EMAIL"]
credentials = ee.ServiceAccountCredentials(service_account, key_data= credentials_json)
ee.Initialize(credentials)

############### CURRENT LOCATION ##############
g = geocoder.ip("me")
current_location = g.latlng

############### DRAW MAP ##############
 
# Add a custom title with styling
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>
        🌍 GHG Explorer: Visualize Global Greenhouse Gas Emissions
    </h1>
    """,
    unsafe_allow_html=True,
)
 
# Add a brief introduction
st.markdown(
    """
    <p style='text-align: center; font-size: 1.2em;'>
        Explore and analyze greenhouse gas emissions across the globe with our interactive mapping tool.
    </p>
    """,
    unsafe_allow_html=True,
)
 
############## FUNCTION ##############
 
 
def display_weather_and_aqi_info(weather_data):
    location = weather_data["weather"]["location"]
    current = weather_data["weather"]["current"]
    aqi = weather_data["aqi"]
 
    st.title(f"Weather in {location['name']}, {location['country']}")
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.metric("Temperature", f"{current['temp_c']}°C")
        st.metric("Feels Like", f"{current['feelslike_c']}°C")
        st.metric("Humidity", f"{current['humidity']}%")
 
    with col2:
        st.image(f"https:{current['condition']['icon']}", width=100)
        st.write(f"**{current['condition']['text']}**")
        st.metric("Wind", f"{current['wind_kph']} km/h {current['wind_dir']}")
 
    st.subheader("Additional Information")
    col3, col4, col5 = st.columns(3)
 
    with col3:
        st.metric("Precipitation", f"{current['precip_mm']} mm")
    with col4:
        st.metric("Pressure", f"{current['pressure_mb']} mb")
    with col5:
        st.metric("UV Index", current["uv"])
 
    last_updated = datetime.datetime.strptime(current["last_updated"], "%Y-%m-%d %H:%M")
    st.write(f"Last updated: {last_updated.strftime('%B %d, %Y at %I:%M %p')}")
 
    if current["precip_mm"] > 0:
        st.warning(f"Rain detected! Current precipitation: {current['precip_mm']} mm")
    elif "rain" in current["condition"]["text"].lower():
        st.info("Possibility of rain. Keep an umbrella handy!")
 
    # AQI Information
    st.subheader("Air Quality Index (AQI)")
 
    # Overall AQI
    overall_aqi = aqi["overall_aqi"]
    aqi_category = get_aqi_category(overall_aqi)
    st.metric("Overall AQI", overall_aqi, aqi_category, delta_color="normal")
 
    # Display individual AQI components
    col_aqi1, col_aqi2, col_aqi3 = st.columns(3)
 
    with col_aqi1:
        st.metric(
            "CO", f"{aqi['CO']['concentration']} µg/m³", f"AQI: {aqi['CO']['aqi']}"
        )
    with col_aqi2:
        st.metric(
            "NO2", f"{aqi['NO2']['concentration']} µg/m³", f"AQI: {aqi['NO2']['aqi']}"
        )
    with col_aqi3:
        st.metric(
            "O3", f"{aqi['O3']['concentration']} µg/m³", f"AQI: {aqi['O3']['aqi']}"
        )
 
    col_aqi4, col_aqi5, col_aqi6 = st.columns(3)
 
    with col_aqi4:
        st.metric(
            "SO2", f"{aqi['SO2']['concentration']} µg/m³", f"AQI: {aqi['SO2']['aqi']}"
        )
    with col_aqi5:
        st.metric(
            "PM2.5",
            f"{aqi['PM2.5']['concentration']} µg/m³",
            f"AQI: {aqi['PM2.5']['aqi']}",
        )
    with col_aqi6:
        st.metric(
            "PM10",
            f"{aqi['PM10']['concentration']} µg/m³",
            f"AQI: {aqi['PM10']['aqi']}",
        )
 
    # Emphasizing AQI categories based on the overall AQI
    if overall_aqi <= 50:
        st.success("Air quality is good!")
    elif overall_aqi <= 100:
        st.warning("Air quality is moderate.")
    elif overall_aqi <= 150:
        st.warning("Air quality is unhealthy for sensitive groups.")
    elif overall_aqi <= 200:
        st.warning("Air quality is unhealthy.")
    elif overall_aqi <= 300:
        st.warning("Air quality is very unhealthy.")
    else:
        st.error("Air quality is hazardous!")
 
 
def get_aqi_category(aqi):
    """Return AQI category based on the value."""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
 
 
def fetch_suggestions(input_value):
    if not input_value:
        return []
 
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={input_value}&addressdetails=1&limit=10"
    headers = {
        "User-Agent": "MyApp/1.0 (your-email@example.com)",
        "Accept-Language": "en",
    }
 
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return []
 
 
def on_input_change():
    st.session_state.suggestions = fetch_suggestions(st.session_state.input_value)
 
 
def fetch_location_by_coordinates(label, lat, lon):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={label}&lat={lat}&lon={lon}&addressdetails=1&limit=1&polygon_geojson=1"
 
    headers = {
        "User-Agent": "MyApp/1.0 (your-email@example.com)",
        "Accept-Language": "en",
    }
 
    try:
        response = requests.get(url, headers=headers)
 
        if response.status_code != 200:
            st.error(f"Error fetching data: {response.status_code}")
            return None
        return response.json()[0] if response.json() else None
 
    except requests.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return None
 
 
def get_json_from_query_params(label, lat, lon):
    if "data" in st.query_params:
        try:
            json_data = json.loads(st.query_params["data"])
            if (
                isinstance(json_data, dict)
                and "label" in json_data
                and "lat" in json_data
                and "lon" in json_data
            ):
                location = fetch_location_by_coordinates(
                    json_data["label"], json_data["lat"], json_data["lon"]
                )
                return location
            else:
                return None
        except json.JSONDecodeError:
            st.error("Invalid JSON data in URL")
            return None
    return None
 
 
############## FUNCTION ##############
 
selected_place = {"display_name": "", "lat": "", "lon": ""}
 
# Interactive Map
m = geemap.Map(
    center=[current_location[0], current_location[1]],
    # basemap="HYBRID",
    # plugin_Draw=True,
    # locate_control=True,
    # plugin_LatLngPopup=False,
    zoom_start=10,
    tiles="CartoDB Positron",
)
# m.add_basemap("ROADMAP")
 
# Weather Info Section
col1, col2 = st.columns([2, 2])
st.session_state["roi"] = None
selected_lat = ""
selected_lng = ""
 
 
st.subheader("🔍 Search Location and View Temperature Heatmap!")
row1_col1, row1_col2 = st.columns([2, 1])
 
if st.session_state.get("zoom_level") is None:
    st.session_state["zoom_level"] = 10
 
st.session_state["ee_asset_id"] = None
st.session_state["bands"] = None
st.session_state["palette"] = None
st.session_state["vis_params"] = None
 
keyword = st.text_input("Search for a location:", "")
if keyword:
    locations = geemap.geocode(keyword)
 
    if locations is not None and len(locations) > 0:
        str_locations = [str(g)[1:-1] for g in locations]
        location = st.selectbox("Select a location:", str_locations)
 
        loc_index = str_locations.index(location)
        selected_loc = locations[loc_index]
        lat, lng = selected_loc.lat, selected_loc.lng
        selected_lat, selected_lng = lat, lng
        st.write("Latitude: ", lat, "Longitude: ", lng)
 
        selected_place["display_name"] = location
        selected_place["lat"] = lat
        selected_place["lon"] = lng
 
        # folium.Marker(location=[lat, lng], popup=location).add_to(m)
 
        m.set_center(lng, lat, 12)
        m.location = [lat, lng]
        st.session_state["zoom_level"] = 10
 
 
if selected_lat and selected_lng:
    with st.status("Fetching Data...", expanded=False) as status:
        info = get_weather_and_aqi_data(selected_lat, selected_lng)
        if info:
            display_weather_and_aqi_info(info)
 
        status.update(label="Done", state="complete", expanded=True)
 
 
location_data = fetch_location_by_coordinates(
    selected_place["display_name"], selected_place["lat"], selected_place["lon"]
)
 
if location_data:
    lat, lon = float(location_data["lat"]), float(location_data["lon"])
    geojson_data = location_data.get("geojson", {})
 
    m.location = [lat, lon]
    
 
    if geojson_data:
 
        border = ee.Geometry(
            {"type": geojson_data["type"], "coordinates": geojson_data["coordinates"]}
        )
 
        modis = (
            ee.ImageCollection("MODIS/061/MOD11A1")
            .filterDate("2024-06-23", "2024-09-23")
            .select("LST_Day_1km")
        )
 
        modCel = modis.map(
            lambda img: img.multiply(0.02)
            .subtract(273.15)
            .copyProperties(img, ["system:time_start"])
        )
 
        mean_lst = modCel.mean().clip(border)
 
        imageVisParam = {
            "min": 20,
            "max": 40,
            "palette": ["#08a70b", "#07ff16", "#e9ff03", "#ffc305", "#ff290e"],
        }
 
        gee_layer = geemap.ee_tile_layer(mean_lst, imageVisParam, "LST Mean")
        m.add_child(gee_layer)
 
        folium.LayerControl().add_to(m)
 
    folium.Marker([lat, lon], popup=location_data).add_to(m)
 
st.subheader("🗺️ Interactive Map")
output = st_folium(m, height=500, width=1000)
 
# Add a "Features" section below the map
st.markdown("---")
st.header("📊 Key Features")
 
feature1, feature2, feature3, feature4, feature5 = st.columns(5)
 
with feature1:
    st.markdown("### 🧑 Human Caused Emission Exploration")
    st.write("Visualize Human Caused Emission Impact on GHG")
 
with feature2:
    st.markdown("### 🌍 Natural Sources & Sinks of GHG")
    st.write("Visualize Natural Activity Impact on GHG")
 
with feature3:
    st.markdown("### 📈 Large Emission Exploration")
    st.write("Explore Large Methane Emission Across the World")
 
with feature4:
    st.markdown("### 🤖 Personalized Chatbot")
    st.write("Get more Intuitive insights with our personalized chatbot")
 
with feature5:
    st.markdown("### 🗺️ Area-wise Statistics")
    st.write("Explore Selected area-wise statistics")
 
# Add a footer
st.markdown("---")
st.markdown(
    """
    <p style='text-align: center; color: #777;'>
        Developed by Team_Ogrodut
    </p>
    """,
    unsafe_allow_html=True,
)