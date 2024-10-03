from datetime import datetime
import os
import branca
import ee
import folium
import geemap.foliumap as geemap
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import streamlit.components.v1 as components
from folium import Map, TileLayer
from streamlit_folium import st_folium
from streamlit_modal import Modal
from keys import credentials_json
from dotenv import load_dotenv
load_dotenv()

from utils.custom_chat_bot import create_chatbot

st.set_page_config(
    page_title="Human Caused Emission",
    page_icon="🧑",
    layout="wide",
)
st.sidebar.image(image="./static/gex_logo.png")


with open("styles.css") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)


# Set the TileJSON URL for the CO₂ emissions data from oCO₂ MIP and ODIAC
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
mip_tile = "https://earth.gov/ghgcenter/api/raster/collections/oco2-mip-co2budget-yeargrid-v1/items/oco2-mip-co2budget-yeargrid-v1-2018/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=ff&color_formula=gamma+r+1.05&colormap_name=purd&rescale=0%2C450"
odiac_tile = "https://earth.gov/ghgcenter/api/raster/collections/odiac-ffco2-monthgrid-v2023/items/odiac-ffco2-monthgrid-v2023-odiac2023_1km_excl_intl_202210/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=co2-emissions&color_formula=gamma+r+1.05&colormap_name=rainbow&rescale=-675.10,31415.44"

collection1 = "oco2-mip-co2budget-yeargrid-v1"
collection2 = "odiac-ffco2-monthgrid-v2023"
asset_name1 = "ff"
asset_name2 = "co2-emissions"

############ MAIN FUNCTION ##############


@st.cache_data
def generate_stats(item, asset_name, geojson):

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


# Initialize the Streamlit app
st.title("Human Caused reason for GHG Emissions")
st.write(
    "This app visualizes CO₂ emissions from human activities using satellite data."
)

# Add a date selector for MIP and ODIAC years
top_col1, top_col2 = st.columns([2, 2])
year_options_mip = list(range(2015, 2021))  # MIP years
year_options_odiac = list(range(2000, 2021))  # ODIAC years

with top_col1:
    # Select a year for MIP data
    selected_year_mip = st.selectbox(
        "Select Year for MIP Emissions (2015-2020):", year_options_mip
    )

with top_col2:
    # Select a year for ODIAC data
    selected_year_odiac = st.selectbox(
        "Select Year for ODIAC Fossil Fuel Emissions (2000-2002):", year_options_odiac
    )


# Update the TileJSON URLs to include the selected year
mip_tile_selected = mip_tile.replace(
    "oco2-mip-co2budget-yeargrid-v1-2018",
    f"oco2-mip-co2budget-yeargrid-v1-{selected_year_mip}",
)
odiac_tile_selected = odiac_tile.replace(
    "odiac-ffco2-monthgrid-v2023-odiac2023_1km_excl_intl_202210",
    f"odiac-ffco2-monthgrid-v2023-odiac2023_1km_excl_intl_{selected_year_odiac}01",
)

with st.container():

    main_col1, main_col2 = st.columns([3, 3])

    with main_col1:

        # # Initialize the leafmap map
        m = geemap.Map(center=[0, 0], zoom=2, google_map="HYBRID")

        # # Add the TileJSON layer for oCO₂ MIP Emissions
        folium.TileLayer(
            tiles=mip_tile,
            name="MIP-based Emissions",
            attr="NASA/NOAA oCO₂ MIP",
            opacity=0.6,
            overlay=True,
            legendEnabled=True,
        ).add_to(m)

        # Add the TileJSON layer for ODIAC Fossil Fuel CO₂ Emissions
        folium.TileLayer(
            tiles=odiac_tile,
            name="Fossil Fuel Emissions",
            attr="ODIAC",
            opacity=0.5,
            overlay=True,
            legendEnabled=True,
        ).add_to(m)

        # # Add a layer control to switch between map layers
        folium.LayerControl(collapsed=False).add_to(m)

        # # Add a colormap legend for CO₂ emissions (MIP-based)
        colormap_mip = branca.colormap.linear.PuRd_09.scale(0, 450)
        colormap_mip = colormap_mip.to_step(index=[0, 100, 200, 300, 400, 450])
        colormap_mip.caption = "CO₂ Emissions (gC/m²/year) - MIP"
        colormap_mip.add_to(m)

        output = st_folium(m, height=500, width=800)

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

    with main_col2:

        with st.status("Loading...", expanded=True) as status:
            st.info(
                """
                - ### **MIP Emissions (Top Layer):** 
                    - **Brown** color reflects the magnitude of the net *carbon exchange*, with **darker** shades indicating `higher CO₂ emissions or uptake`..
                
                - ### **Fossil Fuel CO₂ Emissions (Bottom Layer):**
                    - **Purple** indicate higher levels of emissions, commonly associated with densely `populated` urban areas or regions with heavy `industrial` activity.
                """
            )

            status.update(label="Done", state="complete", expanded=True)


with st.container():

    # Read the CSV file
    df = pd.read_csv("data/oco2-mip-co2budget-yeargrid-v1.csv")

    st.title("OCO-2 MIP Annual carbon dioxide emissions and removals")

    # Calculate statistics
    mean = df["mean"].mean()
    stddev = df["std"].mean()
    minimum = df["min"].mean()
    maximum = df["max"].mean()

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Emission", f"{df['mean'].mean():.2f} g CO₂/m²/yr")
    col2.metric("Max Emission", f"{df['max'].max():.2f} g CO₂/m²/yr")
    col3.metric("Min Emission", f"{df['min'].min():.2f} g CO₂/m²/yr")

    # Trend over years
    yearly_avg = df.groupby("datetime")["max"].mean().reset_index()
    fig_trend = px.line(
        yearly_avg, x="datetime", y="max", title="CO2 Emission Trend Over Years"
    )
    st.plotly_chart(fig_trend)

    # Create data for the plot
    x = np.linspace(minimum, maximum, 1000)
    y = (1 / (stddev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / stddev) ** 2)

    # Create the figure
    fig = go.Figure()

    # Add the normal distribution curve
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="lines", name="Normal Distribution", line=dict(color="blue")
        )
    )

    # Add mean, stddev, min, max as vertical lines
    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="green",
        annotation_text=f"Mean: {mean:.2f}",
    )
    fig.add_vline(
        x=mean + stddev,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Stddev: {stddev:.2f}",
    )
    fig.add_vline(
        x=minimum,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Min: {minimum:.2f}",
    )
    fig.add_vline(
        x=maximum,
        line_dash="dash",
        line_color="purple",
        annotation_text=f"Max: {maximum:.2f}",
    )

    # Add title and labels
    fig.update_layout(
        title="Normal Distribution of CO2 Emission Data",
        xaxis_title="Emission (g CO₂/m²/yr)",
        yaxis_title="Density",
        # width=800,
        height=500,
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


################## CHAT BOT #####################

# Add the chatbot to this page

modal = Modal(
    "Demo Modal",
    key="demo-modal",
    # Optional
    padding=20,  # default value
    max_width=744,  # default value
)

open_modal = st.button("Chat with OgrodutBot", use_container_width=True, type="primary")

if open_modal:
    modal.open()

if modal.is_open():

    specific_context = """
    This page displays a map of natural sources and sinks of CO₂ and CH₄ (carbon dioxide and methane). The map shows concentrated methane sources from tropical and high latitude ecosystems. Users can select from four different layers to view on the map:

    1. ECCO-Darwin CO₂ Fluxes 2021: Shows air-sea CO₂ fluxes, with brighter colors indicating higher CO₂ absorption by the ocean.

    2. MiCASA Land Carbon Flux 2023: Displays carbon flux parameters, including net primary production and heterotrophic respiration. Brighter areas represent high net primary production (carbon uptake), while darker areas indicate higher CO₂ respiration.

    3. GOSAT CH₄ Budget 2019: Illustrates annual methane emissions derived from satellite observations, with vibrant colors indicating significant methane emissions from wetlands or agricultural activities.

    4. LPJ-EOSIM Wetland CH₄ Emissions 2024: Estimates methane emissions from wetlands, showing natural contributions to the global methane budget. Brighter colors signify regions with higher methane emissions.

    The map is interactive, allowing users to toggle between layers and zoom in/out. Each layer provides insights into different aspects of greenhouse gas emissions and absorption, helping to visualize the complex interactions between natural systems and the global carbon cycle.
    """

    create_chatbot("Natural Sources and Sinks Chat", specific_context, "OgrodutBot")
