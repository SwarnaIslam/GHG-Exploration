import ee
import folium
import geemap.foliumap as geemap
import requests
import streamlit as st
from streamlit_folium import st_folium
from dotenv import load_dotenv
import os
load_dotenv()

st.set_page_config(layout="wide")
with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.title("Location Search")

############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, "keys.json")
ee.Initialize(credentials)


############ CUSTOM FUNCTION ##############
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


############ SEARCH BAR ##################
if "input_value" not in st.session_state:
    st.session_state.input_value = ""
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

col1, col2 = st.columns((2, 2))
selected_place = {"display_name": "", "lat": "", "lon": ""}

with col1:
    st.text_input("Search for a location", key="input_value", on_change=on_input_change)

with col2:
    with st.spinner("Loading place suggestions..."):
        if st.session_state.suggestions:
            selected_location = st.selectbox(
                "Select a location",
                options=[
                    place["display_name"] for place in st.session_state.suggestions
                ],
                format_func=lambda x: x,
            )

            selected_place = next(
                (
                    place
                    for place in st.session_state.suggestions
                    if place["display_name"] == selected_location
                ),
                None,
            )

        elif st.session_state.input_value:
            st.write("No suggestions found.")


############ Create MAP ##################
default_lat, default_lon = 23.685, 90.3563
m = geemap.Map(
    location=[default_lat, default_lon], zoom_start=5, tiles="CartoDB Positron"
)

location_data = fetch_location_by_coordinates(
    selected_place["display_name"], selected_place["lat"], selected_place["lon"]
)

if location_data:
    lat, lon = float(location_data["lat"]), float(location_data["lon"])
    geojson_data = location_data.get("geojson", {})

    m.location = [lat, lon]
    m.zoom_start = 10

    if geojson_data:

        border = ee.Geometry(
            {"type": geojson_data["type"], "coordinates": geojson_data["coordinates"]}
        )

        modis = (
            ee.ImageCollection("MODIS/061/MOD11A1")
            .filterDate("2014-09-23", "2024-09-23")
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
            "palette": ["blue", "green", "yellow", "orange", "red"],
        }

        gee_layer = geemap.ee_tile_layer(mean_lst, imageVisParam, "LST Mean")
        m.add_child(gee_layer)

        folium.LayerControl().add_to(m)

    folium.Marker([lat, lon], popup=location_data).add_to(m)

st_folium(m, width=1200, height=600)
