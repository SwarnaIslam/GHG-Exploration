import ee
import leafmap.foliumap as leafmap
import leafmap.maplibregl as leafmap
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")

############ AUTHENTICATION ##############
service_account = os.getenv("GEE_EMAIL")
credentials = ee.ServiceAccountCredentials(service_account, "keys.json")
ee.Initialize(credentials)


# row1_col1, row1_col2 = st.columns([3, 1])
width = 800
height = 800
tiles = None

# with row1_col2:

#     # checkbox = st.checkbox("Search Quick Map Services (QMS)")
#     # keyword = st.text_input("Enter a keyword to search and press Enter:")
#     # empty = st.empty()

#     # if keyword:
#     #     options = leafmap.search_xyz_services(keyword=keyword)
#     #     if checkbox:
#     #         options = options + leafmap.search_qms(keyword=keyword)

#     #     tiles = empty.multiselect("Select XYZ tiles to add to the map:", options)

#     with row1_col1:
#         # m = leafmap.Map()

#         # if tiles is not None:
#         #     for tile in tiles:
#         #         m.add_xyz_service(tile)

#         m = leafmap.Map(
#             center=[-120.4482, 38.0399],
#             zoom=13,
#             pitch=60,
#             bearing=30,
#             style="3d-terrain",
#         )
#         m.add_ee_layer(asset_id="MODIS/MCD43A4_006_NDVI", opacity=0.5)
#         m.add_legend(builtin_legend="MODIS/MCD43A4_006_NDVI", title="ESA Landcover")
#         m.add_layer_control()

#         m.layer_interact()

#         m.to_streamlit(width, height)


############### IGNORE #############
# markdown = """
# A Streamlit map template
# <https://github.com/opengeos/streamlit-map-template>
# """

# with st.expander("See demo"):
#     st.image("https://i.imgur.com/0SkUhZh.gif")


# st.title("Searching Basemaps")
# st.markdown(
#     """
# This app is a demonstration of searching and loading basemaps from [xyzservices](https://github.com/geopandas/xyzservices) and [Quick Map Services (QMS)](https://github.com/nextgis/quickmapservices). Selecting from 1000+ basemaps with a few clicks.
# """
# )


############# GEE #############
m = leafmap.Map(
    center=[-120.4482, 38.0399], zoom=13, pitch=60, bearing=30, style="3d-terrain"
)
m.add_ee_layer(asset_id="ESA/WorldCover/v200", opacity=0.5)
m.add_legend(builtin_legend="ESA_WorldCover", title="ESA Landcover")
m.add_layer_control()

m.to_streamlit(width, height)
