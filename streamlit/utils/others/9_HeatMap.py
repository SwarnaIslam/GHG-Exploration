import streamlit as st
import folium
from streamlit_folium import st_folium
import geemap.foliumap as geemap
import ee
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")

############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, "keys.json")
ee.Initialize(credentials)

dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
country_list = dataset.aggregate_array('country_na').getInfo()

def plot_lst_for_country(country_name):

    dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
    country_border = dataset.filter(ee.Filter.eq('country_na', country_name))

    # Import MODIS LST image collection.
    modis = ee.ImageCollection('MODIS/061/MOD11A2')

 
    start = ee.Date('2024-01-01')
    date_range = ee.DateRange(start, start.advance(10, 'month'))


    mod11a2 = modis.filterDate(date_range)


    modLSTday = mod11a2.select('LST_Day_1km')
    modLSTc = modLSTday.map(lambda img: img.multiply(0.02).subtract(273.15).copyProperties(img, ['system:time_start']))


    clippedLSTc = modLSTc.mean().clip(country_border)

 
    map_center = country_border.geometry().centroid().coordinates().getInfo()[::-1]
    folium_map = folium.Map(location=map_center, zoom_start=6)


    vis_params = {
        'min': 10, 'max': 45,
        'palette': ['blue', 'limegreen', 'yellow', 'darkorange', 'red']
    }
    map_id_dict = geemap.ee_tile_layer(clippedLSTc, vis_params, 'Mean temperature, 2015')
    folium_map.add_child(map_id_dict)

    folium.GeoJson(data=country_border.geometry().getInfo(), name="Country Border").add_to(folium_map)


    return folium_map

st.title("MODIS LST Time Series Viewer")

country_name = st.selectbox('Select a country:', sorted(country_list))

if country_name:
    folium_map = plot_lst_for_country(country_name)
    st_data = st_folium(folium_map, width=700, height=500)
