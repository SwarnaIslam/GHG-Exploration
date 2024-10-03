import os
from datetime import datetime

import branca
import ee
import folium
import geemap.foliumap as geemap
import google.generativeai as gen_ai
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from folium import Map, TileLayer
from streamlit_folium import st_folium
from streamlit_modal import Modal
from keys import credentials_json

from utils.basic_stats import generate_basic_stats
from utils.custom_chat_bot import create_chatbot
load_dotenv()
# st.set_page_config(layout="wide")
st.set_page_config(
    page_title="Large Emission Events",
    page_icon="☁️",
    layout="wide",
)
st.sidebar.image(image="./app/static/gex_logo.png")


with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

############ AUTHENTICATION ##############
service_account =st.secrets["general"]["GEE_EMAIL"]
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)

############ MAIN FUNCTION ##############

# Set the TileJSON URLs for the data
DVAR_DATA = "https://earth.gov/ghgcenter/api/raster/collections/tm54dvar-ch4flux-monthgrid-v1/items/tm54dvar-ch4flux-monthgrid-v1-201612/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=fossil&color_formula=gamma+r+1.05&colormap_name=purd&rescale=0.0%2C202.8189294183266"

# Map layers and information
layer_options = {
    "TM5-4DVar Isotopic CH₄ Inverse Fluxes": DVAR_DATA,
}

layer_dataset = {
    "TM5-4DVar Isotopic CH₄ Inverse Fluxes": [
        "data/tm54dvar-ch4flux-mask-monthgrid-v1.csv",
        "Emission",
        "CH₄ Inverse Fluxes",
    ]
}

layer_info = {
    "TM5-4DVar Isotopic CH₄ Inverse Fluxes": """
    - ### **TM5-4DVar Isotopic CH₄ Inverse Fluxes (2016):**
        - **Displays** inverse fluxes of *:red[CH₄ (methane)]* based on the TM5-4DVar model.
        - **Brighter colors** represent areas with higher **CH₄ emissions**, indicating potential methane sources.
        - This layer helps identify regions with significant methane flux, which is crucial for understanding the global methane budget.
    """
}

# Initialize the Streamlit app
st.title("Large Emission Events")
st.write("This app shows large emission events due to natural factors")

# Dropdown menu for selecting layers
selected_layers = st.multiselect(
    "Select layers to view on the map (you can select multiple):",
    list(layer_options.keys()),
    default=["TM5-4DVar Isotopic CH₄ Inverse Fluxes"],  # Default one layer
)

col1, col2 = st.columns([3, 3])

with col1:

    # Initialize the map
    m = geemap.Map(
        center=[0, 0],
        zoom=2,
        basemap="HYBRID",
        plugin_Draw=True,
        # Draw_export=True,
        locate_control=True,
        plugin_LatLngPopup=False,
    )
    m.add_basemap("ROADMAP")

    # Add layers to the map based on the user's selection
    for layer in selected_layers:
        folium.TileLayer(
            tiles=layer_options[layer],
            name=layer,
            attr=layer,
            opacity=0.6,
            overlay=True,
            legendEnabled=True,
        ).add_to(m)

    # Add a layer control to enable toggling between layers
    folium.LayerControl(collapsed=False).add_to(m)

    # Display the map in Streamlit using st_folium
    st_folium(m, height=600, width=800)

with col2:

    with st.spinner("Loading..."):

        # Display the layer information based on selected layers
        if selected_layers:
            for layer in selected_layers:
                st.info(
                    f"""
                        {layer_info[layer]}
                        
                        """
                )

################## CHAT BOT #####################

for layer in selected_layers:

    if len(layer_dataset[layer]) > 0:
        generate_basic_stats(
            layer_dataset[layer][0],
            type=layer_dataset[layer][1],
            title=layer_dataset[layer][2],
            unit="g CH₄/m²/year",
            gas="CH4",
        )


################## CHAT BOT #####################

modal = Modal(
    "Demo Modal",
    key="demo-modal",
    # Optional
    padding=20,  # default value
    max_width=744,  # default value
)

open_modal = st.button("🤖 Chat with Ogrodut", use_container_width=True, type="primary")

if open_modal:
    modal.open()

if modal.is_open():

    specific_context = """

    This page displays a map of large emission events, focusing on CH₄ (methane) fluxes. The map shows various regions and processes that contribute to significant methane emissions across the globe. Users can select from different layers to view on the map:

    1. TM5-4DVar Isotopic CH₄ Inverse Fluxes (2016): Displays inverse fluxes of CH₄ based on the TM5-4DVar model. Brighter colors represent areas with higher CH₄ emissions, indicating potential methane sources. This layer helps identify regions with significant methane flux, which is crucial for understanding the global methane budget.

    The map is interactive, allowing users to toggle layers and zoom in/out. The layer provides insights into large methane emission events, helping to visualize the complex distribution of CH₄ sources across the globe.

    Additional features include:
    - A multiselect dropdown for choosing map layers
    - Informative descriptions for each selected layer
    - Basic statistics generation for the displayed data
    - An interactive chatbot (OgrodutBot) for user queries about the displayed information

    This visualization aids in understanding the spatial distribution of major methane emission events and their potential impact on the global greenhouse gas balance.
    """

    create_chatbot("Natural Sources and Sinks Chat", specific_context, "OgrodutBot")
