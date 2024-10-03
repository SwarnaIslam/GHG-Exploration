import json
import os
from datetime import datetime
from urllib import response

import branca
import ee
import folium
import folium.plugins as plugins
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from keys import credentials_json
from pyexpat import features
from streamlit_folium import st_folium
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


############ MAIN FUNCTION ##############
# Initialize the Streamlit app
st.title("Natural Emissions and Sinks Visualization")

# Create a container for the map
with st.container():
    # Add description
    st.write(
        "This app visualizes methane emissions and natural sources (like wetlands) using satellite data."
    )

    # Initialize the leafmap map
    m = leafmap.Map(center=[0, 0], zoom=2, google_map="HYBRID")

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

# Create a container for the plot
with st.container():

    # Sample statistics data (replace these with actual values you received)
    # mean = 0.22315353155136108
    # stddev = 0.7086087172371052
    # maximum = 6.5816521644592285
    # minimum = -0.3509398102760315

    micasa_df = pd.read_csv("streamlit/data/micasa-carbonflux-monthgrid-v1.csv")
    micasa_df["datetime"] = pd.to_datetime(micasa_df["datetime"])

    mean = micasa_df["mean"].mean()
    maximum = micasa_df["max"].mean()
    minimum = micasa_df["min"].mean()
    stddev = micasa_df["std"].mean()

    # Display statistics and the plot immediately after the map
    st.title("MICASA Dataset Statistics: Respiration Heterotrophic (rh)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Mean", value=f"{mean:.3f}")
    with col2:
        st.metric(label="Std. Deviation", value=f"{stddev:.3f}")
    with col3:
        st.metric(label="Maximum", value=f"{maximum:.3f}")
    with col4:
        st.metric(label="Minimum", value=f"{minimum:.3f}")

    # Decision-making type interpretation
    st.write(
        f"""
    **Interpretation:**
    
    - **Mean ({mean:.2f} kg/m²/year):** Indicates moderate respiration activity, reflecting healthy soil conditions. Consistently high values may suggest potential greenhouse gas emission risks.
    
    - **Standard Deviation ({stddev:.2f}):** Highlights considerable variability across the region, pointing to areas that may require targeted management efforts.
    
    - **Maximum ({maximum:.2f} kg/m²/year) & Minimum ({minimum:.2f} kg/m²/year):** The maximum value suggests high microbial activity in certain locations, while the minimum indicates areas of low or negative respiration. 

    **Conclusion:** Regular monitoring of rh values is crucial for guiding soil health interventions and mitigating emission risks.
    """
    )

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
        title="Normal Distribution of 'rh' Asset Data",
        xaxis_title="Value",
        yaxis_title="Density",
        width=800,  # Adjust the width
        height=500,  # Adjust the height
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)
