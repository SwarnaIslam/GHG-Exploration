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

from utils.basic_stats import generate_basic_stats
from utils.custom_chat_bot import create_chatbot
from keys import credentials_json
load_dotenv()

# st.set_page_config(layout="wide")
st.set_page_config(
    page_title="Natural Sources and Sinks of CO₂ and CH₄",
    page_icon="🌿",
    layout="wide",
)
st.sidebar.image(image="app/static/gex_logo.png")

with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

############ AUTHENTICATION ##############
service_account = st.secrets["general"]["GEE_EMAIL"]
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)

############ MAIN FUNCTION ##############

# Set the TileJSON URLs for the data
ECCO_DARWIN = "https://earth.gov/ghgcenter/api/raster/collections/eccodarwin-co2flux-monthgrid-v5/items/eccodarwin-co2flux-monthgrid-v5-202104/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=co2&color_formula=gamma+r+1.05&colormap_name=magma&rescale=-0.0007%2C0.0007"
MiCASA_Land = "https://earth.gov/ghgcenter/api/raster/collections/micasa-carbonflux-daygrid-v1/items/micasa-carbonflux-daygrid-v1-20230101/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=rh&color_formula=gamma+r+1.05&colormap_name=purd&rescale=-0.35656991600990295%2C7.2141876220703125"
GOSAT = "https://earth.gov/ghgcenter/api/raster/collections/gosat-based-ch4budget-yeargrid-v1/items/gosat-based-ch4budget-yeargrid-v1-2019/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=prior-total&color_formula=gamma+r+1.05&colormap_name=rainbow&rescale=0.0%2C2.121816635131836"
LPJ_EOSIM = "https://earth.gov/ghgcenter/api/raster/collections/lpjeosim-wetlandch4-daygrid-v2/items/lpjeosim-wetlandch4-daygrid-v2-20240101/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=ensemble-mean-ch4-wetlands-emissions&color_formula=gamma+r+1.05&colormap_name=magma&rescale=0.0%2C0.0003"

# Map layers and information
layer_options = {
    "ECCO-Darwin CO₂ Fluxes 2021": ECCO_DARWIN,
    "MiCASA Land Carbon Flux 2023": MiCASA_Land,
    "GOSAT CH₄ Budget 2019": GOSAT,
    "LPJ-EOSIM Wetland CH₄ Emissions 2024": LPJ_EOSIM,
}

layer_dataset = {
    "ECCO-Darwin CO₂ Fluxes 2021": [
        "data/eccodarwin-co2flux-monthgrid-v5.csv",
        "Absorption",
        "Air-Sea CO₂ Flux: Global Ocean Carbon Absorption",
    ],
    "MiCASA Land Carbon Flux 2023": [
        "data/micasa-carbonflux-monthgrid-v1.csv",
        "Emission",
        "MiCASA Land Carbon Flux: Global Carbon Fluxes",
    ],
    "GOSAT CH₄ Budget 2019": "",
    "LPJ-EOSIM Wetland CH₄ Emissions 2024": [
        "data/lpjeosim-wetlandch4-monthgrid-v2.csv",
        "Emission",
        "Global Methane Emissions from Wetlands",
    ],
}

layer_info = {
    "ECCO-Darwin CO₂ Fluxes 2021": """
    - ### **ECCO-Darwin CO₂ Fluxes (2021):**
        - **Illustrates** air-sea *:red[CO₂ fluxes]* from the ECCO-Darwin model.
        - **Brighter colors** indicate higher **CO₂ absorption** by the ocean, highlighting its role as a **carbon sink**.
    """,
    "MiCASA Land Carbon Flux 2023": """
    - ### **MiCASA Land Carbon Flux (2023):**
        - **Presents** :red[carbon] flux parameters, showing data on **net primary production** and *heterotrophic respiration*.
        - **Brighter shades** represent areas with **high carbon uptake** (net primary production); darker shades indicate **higher CO₂ respiration**.
    """,
    "GOSAT CH₄ Budget 2019": """
    - ### **GOSAT CH₄ Budget (2019):**
        - **Displays** annual *:blue[CH4] emissions* derived from satellite observations.
        - **Vibrant colors** indicate significant **CH₄ emissions**, especially from **wetlands** or **agricultural activities**.
    """,
    "LPJ-EOSIM Wetland CH₄ Emissions 2024": """
    - ### **LPJ-EOSIM Wetland CH₄ Emissions (2024):**
        - **Estimates** :blue[CH4] emissions from *wetlands*, showing natural contributions to the global *methane budget*.
        - **Brighter colors** signify regions with **higher CH₄ emissions** from wetlands.
    """,
}

# Initialize the Streamlit app
st.title("Natural Sources and Sinks of CO₂ and CH₄")
st.write(
    "This app shows concentrated methane sources from tropical and high latitude ecosystems."
)

# Dropdown menu for selecting layers
selected_layers = st.multiselect(
    "Select layers to view on the map (you can select multiple):",
    list(layer_options.keys()),
    default=["ECCO-Darwin CO₂ Fluxes 2021"],  # Default one layer
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

    This page displays a map of natural sources and sinks of greenhouse gases, primarily CO₂ and CH₄ (carbon dioxide and methane). The map shows various natural processes and ecosystems that contribute to or absorb these gases across the globe. Users can select from different layers to view on the map:

    1. ECCO-Darwin CO₂ Fluxes: Shows air-sea CO₂ fluxes, illustrating how oceans act as carbon sinks. Brighter colors indicate higher CO₂ absorption by the ocean.

    2. MiCASA Land Carbon Flux: Presents carbon flux parameters for land, showing data on net primary production and heterotrophic respiration. Brighter shades represent areas with high carbon uptake, while darker shades indicate higher CO₂ respiration.

    3. GOSAT CH₄ Budget: Displays annual CH₄ emissions derived from satellite observations, highlighting natural methane sources such as wetlands.

    4. LPJ-EOSIM Wetland CH₄ Emissions: Estimates CH₄ emissions from wetlands, showing natural contributions to the global methane budget. Brighter colors signify regions with higher CH₄ emissions from wetlands.

    The map is interactive, allowing users to toggle between layers and zoom in/out. Each layer provides insights into different aspects of natural greenhouse gas sources and sinks, helping to visualize the complex interactions within the global carbon cycle.
    """

    create_chatbot("Natural Sources and Sinks Chat", specific_context, "OgrodutBot")
