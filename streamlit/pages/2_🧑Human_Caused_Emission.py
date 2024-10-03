import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
import os
from datetime import datetime

import branca
import requests

import json
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
from utils.get_area_temp import get_area_wise_temp
from utils.get_chart import draw_line_chart
from keys import credentials_json
load_dotenv()

st.set_page_config(
    page_title="Human Caused Emission",
    page_icon="🧑",
    layout="wide",
)

css = """
/* disable human running icon while loading starts */
div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}

div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}

div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}

#MainMenu {
    visibility: hidden;
    height: 0%;
}

header {
    visibility: hidden;
    height: 0%;
}

footer {
    visibility: hidden;
    height: 0%;
}

/* disable human running icon while loading ends */


/* disable loading fade effect */
.element-container {
    opacity: 1 !important
}

body {
    margin: 0;
    padding: 0;
}

.stApp {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.st-emotion-cache-keje6w {
    width: calc(50% - 1rem);
    flex: 1 1 calc(50% - 1rem);
    /* height: 20vh; */
}
"""

make_map_responsive = """
 <style>
 [title~="st.iframe"] { width: 100%}
 </style>
"""
st.markdown(make_map_responsive, unsafe_allow_html=True)

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

############ AUTHENTICATION ##############
service_account = st.secrets["general"]["GEE_EMAIL"]
credentials = ee.ServiceAccountCredentials(service_account, key_data=credentials_json)
ee.Initialize(credentials)

############ METHODS ###############


@st.cache_data
def generate_stats(
    item, geojson, asset_name, dateColumnKey="datetime", dateColumnValue="datetime"
):
    """
    Generate statistics for a given item and GeoJSON region.
    """

    result = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][asset_name]["href"]},
        json=geojson,
    ).json()

    # st.write(f">> DONE FETCHING STATS")
    # print("RESULT: ", result)
    # st.write("RESULT: ", result)

    return {
        **result["properties"],
        # "datetime": item["datetime"]["datetime"][:7],  # start_datetime or datetime
        # "datetime": item["properties"]["start_datetime"],
        dateColumnKey: item["properties"][dateColumnValue],
    }


def clean_stats(stats_json, datecolumn="datetime") -> pd.DataFrame:

    # Normalize the JSON data
    df = pd.json_normalize(stats_json)

    # Replace the naming "statistics.b1" in the columns
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]

    # Set the datetime format
    df["date"] = pd.to_datetime(df[datecolumn])  #!DYNAMIC KORTE HOBE

    # Return the cleaned format
    return df


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
        # st.code(geojson_str, language="json")
        ok = 1

        return geoJSON


############ CONSTANTS ###############

RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"

MIP_TILE = "https://earth.gov/ghgcenter/api/raster/collections/oco2-mip-co2budget-yeargrid-v1/items/oco2-mip-co2budget-yeargrid-v1-2018/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=ff&color_formula=gamma+r+1.05&colormap_name=purd&rescale=0%2C450"
ODIAC_TILE = "https://earth.gov/ghgcenter/api/raster/collections/odiac-ffco2-monthgrid-v2023/items/odiac-ffco2-monthgrid-v2023-odiac2023_1km_excl_intl_202210/tiles/WebMercatorQuad/{z}/{x}/{y}@1x?assets=co2-emissions&color_formula=gamma+r+1.05&colormap_name=rainbow&rescale=-675.10,31415.44"

MIP_START_DATE = "2015-01-01"
MIP_END_DATE = "2020-01-01"

ODIAC_START_DATE = "2000-01-01"
ODIAC_END_DATE = "2022-12-01"

# Map layers and information
layer_options = {
    "OCO-2 MIP Top-down CO₂ Budgets": MIP_TILE,
    "ODIAC Fossil Fuel CO₂ Emissions": ODIAC_TILE,
}

collections = {
    "OCO-2 MIP Top-down CO₂ Budgets": "oco2-mip-co2budget-yeargrid-v1",
    "ODIAC Fossil Fuel CO₂ Emissions": "odiac-ffco2-monthgrid-v2023",
}

collection_asset = {
    "OCO-2 MIP Top-down CO₂ Budgets": ["ff"],
    "ODIAC Fossil Fuel CO₂ Emissions": ["co2-emissions"],
}

collection_datetime_col = {
    "OCO-2 MIP Top-down CO₂ Budgets": ["datetime", "start_datetime"],
    "ODIAC Fossil Fuel CO₂ Emissions": ["start_datetime", "start_datetime"],
}

collection_frequency = {
    "OCO-2 MIP Top-down CO₂ Budgets": "yearly",
    "ODIAC Fossil Fuel CO₂ Emissions": "monthly",
}

layer_dataset = {
    "OCO-2 MIP Top-down CO₂ Budgets": [
        "data/oco2-mip-co2budget-yeargrid-v1.csv",
        "Budget",
        "OCO-2 MIP Top-down CO₂ Budgets",
    ],
    "ODIAC Fossil Fuel CO₂ Emissions": "",
}

layer_info = {
    "OCO-2 MIP Top-down CO₂ Budgets": """
    - ### **OCO-2 MIP Top-down CO₂ Budgets:**
        - **Brown** color reflects the magnitude of the net *carbon exchange*, with **darker** shades indicating `higher CO₂ emissions or uptake`.
    """,
    "ODIAC Fossil Fuel CO₂ Emissions": """
    - ### **ODIAC Fossil Fuel CO₂ Emissions:**
        - **Purple** indicate higher levels of emissions, commonly associated with densely `populated` urban areas or regions with heavy `industrial` activity
    """,
}

# Initialize the Streamlit app
st.title("Human Caused reason for GHG Emissions")
st.write(
    "This app visualizes CO₂ emissions from human activities using satellite data."
)

# Dropdown menu for selecting layers
selected_layers = st.multiselect(
    "Select layers to view on the map (you can select multiple):",
    list(layer_options.keys()),
    default=["OCO-2 MIP Top-down CO₂ Budgets"],  # Default one layer
)

with st.expander("Whats the Data about?"):

    with st.spinner("Loading..."):

        # Display the layer information based on selected layers
        if selected_layers:
            for layer in selected_layers:
                st.info(
                    f"""
                        {layer_info[layer]}  
                    """
                )


################## MAP #####################
st.info('Select any Area with Polygon tool to explore more', icon="ℹ️")
with st.container():

    # Initialize the map
    m = geemap.Map(
        center=[0, 0],
        zoom=3,
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
    output = st_folium(m, width=1600)


################## REGION WISE STATS #####################
with st.container():

    # show the geo json
    area_geojson = get_geojson(output)
    if area_geojson:
        st.code(area_geojson, language="json")

        # create selector for data
        selected_dataset = st.selectbox(
            "Select Dataset:",
            list(layer_options.keys()),
        )

        st.markdown(f"Dataset: :green[{selected_dataset}]")

        # show date range
        if selected_dataset == "OCO-2 MIP Top-down CO₂ Budgets":
            start_date = datetime.strptime(MIP_START_DATE, "%Y-%m-%d")
            end_date = datetime.strptime(MIP_END_DATE, "%Y-%m-%d")
        else:  # ODIAC Fossil Fuel CO₂ Emissions
            start_date = datetime.strptime(ODIAC_START_DATE, "%Y-%m-%d")
            end_date = datetime.strptime(ODIAC_END_DATE, "%Y-%m-%d")

        col1, col2 = st.columns(2)

        with col1:
            selected_start_date = st.date_input(
                "Select start date",
                value=start_date,
                min_value=start_date,
                max_value=end_date,
            )

        with col2:
            selected_end_date = st.date_input(
                "Select end date",
                value=end_date,
                min_value=start_date,
                max_value=end_date,
            )

        st.markdown(
            f"Selected date range: **{selected_start_date}** to **{selected_end_date}** as **{collection_frequency[selected_dataset].title()}**"
        )

        # Calculate total data points
        if collection_frequency[selected_dataset] == "yearly":
            total_items = selected_end_date.year - selected_start_date.year + 1
        else:  # monthly
            total_items = (
                (selected_end_date.year - selected_start_date.year) * 12
                + (selected_end_date.month - selected_start_date.month)
                + 1
            )

        st.markdown(f"Total data points to be fetched: **{total_items}**")

        # Fetch Data
        collection_name = collections[selected_dataset]

        # st.button("Get Data", type="primary")
        if st.button("Get Data", type="primary"):
            df = None
            
            chart_col1, chart_col2 = st.columns([3, 3])
            with chart_col1:
                with st.status("Getting Data...", expanded=True) as status:
                    url = f"{STAC_API_URL}/collections/{collection_name}/items?limit={total_items}"
                    items = requests.get(url).json()["features"]

                    # generating stats
                    progress_bar = st.progress(0)
                    stats = []

                    for i, item in enumerate(items):
                        stats.append(
                            generate_stats(
                                item,
                                area_geojson[0],
                                collection_asset[selected_dataset][0],
                                dateColumnKey=collection_datetime_col[selected_dataset][0],
                                dateColumnValue=collection_datetime_col[selected_dataset][
                                    1
                                ],
                            )
                        )
                        progress = (i + 1) / len(items)
                        progress_bar.progress(progress)

                    progress_bar.empty()

                    # st.write(stats)

                    df = clean_stats(
                        stats, datecolumn=collection_datetime_col[selected_dataset][0]
                    )
                    status.update(label="Done", state="complete", expanded=True)


                    # Create Output
                    generate_basic_stats(
                        layer_dataset[layer][0],
                        type=layer_dataset[layer][1],
                        title=f"Selected Region Data - {layer_dataset[layer][2]}",
                        unit="ton C/km²/month",
                        df=df,
                    )

            with chart_col2:
                with st.status("Getting Temperature Data..."):
                    temp_df = get_area_wise_temp(
                        area_geojson[0], selected_start_date, selected_end_date
                    )
                    status.update(label="Done", state="complete", expanded=True)

                    st.table(
                        temp_df
                    )  # col: Month	Average Temp (°C)	Min Temp (°C)	Max Temp (°C)	Std Dev (°C)

                draw_line_chart(
                    df=temp_df,
                    x_column="Month",
                    y_column="Average Temp (°C)",
                    title="Average Temperature Over Time",
                    x_label="Date",
                    y_label="Average Temperature (°C)",
                    color="blue",
                )

            # now make a plot using this temp_df and df where x would be month and y would be

################## REGION + WHOLE WISE VIZ #####################
with st.container():
    for layer in selected_layers:

        if len(layer_dataset[layer]) > 0:
            generate_basic_stats(
                layer_dataset[layer][0],
                type=layer_dataset[layer][1],
                title=layer_dataset[layer][2],
                unit="ton C/km²/month",
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
