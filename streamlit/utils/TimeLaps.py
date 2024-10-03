   collection = st.selectbox(
        "Select a satellite image collection: ",
        [
            "Any Earth Engine ImageCollection",
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
            "Geostationary Operational Environmental Satellites (GOES)",
            "MODIS Vegetation Indices (NDVI/EVI) 16-Day Global 1km",
            "MODIS Gap filled Land Surface Temperature Daily",
            "MODIS Ocean Color SMI",
            "USDA National Agriculture Imagery Program (NAIP)",
        ],
        index=1,
    )

    if collection == "MODIS Gap filled Land Surface Temperature Daily":
        with st.expander("Show dataset details", False):
            st.markdown(
                """
            See the [Awesome GEE Community Datasets](https://samapriya.github.io/awesome-gee-community-datasets/projects/daily_lst/).
            """
            )

        MODIS_options = ["Daytime (1:30 pm)", "Nighttime (1:30 am)"]
        MODIS_option = st.selectbox("Select a MODIS dataset:", MODIS_options)
        if MODIS_option == "Daytime (1:30 pm)":
            st.session_state["ee_asset_id"] = (
                "projects/sat-io/open-datasets/gap-filled-lst/gf_day_1km"
            )
        else:
            st.session_state["ee_asset_id"] = (
                "projects/sat-io/open-datasets/gap-filled-lst/gf_night_1km"
            )

        palette_options = st.selectbox(
            "Color palette",
            cm.list_colormaps(),
            index=90,
        )
        palette_values = cm.get_palette(palette_options, 15)
        palette = st.text_area(
            "Enter a custom palette:",
            palette_values,
        )
        st.write(cm.plot_colormap(cmap=palette_options, return_fig=True))
        st.session_state["palette"] = json.loads(palette.replace("'", '"'))


#  newGeoJSon = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "properties": {},
#                 "geometry": {
#                     "type": "Polygon",
#                     "coordinates": [
#                         [
#                             [85.634651, 25.264258],
#                             [85.634651, 25.362952],
#                             [85.737305, 25.362952],
#                             [85.737305, 25.264258],
#                             [85.634651, 25.264258],
#                         ]
#                     ],
#                 },
#             }
#         ],
#     }

"""

    if collection in ["MODIS Gap filled Land Surface Temperature Daily"]:

        with st.form("submit_ts_form"):
            with st.expander("Customize timelapse"):

                title = st.text_input(
                    "Enter a title to show on the timelapse: ",
                    "Surface Temperature",
                )
                start_date = st.date_input(
                    "Select the start date:", datetime.date(2018, 1, 1)
                )
                end_date = st.date_input(
                    "Select the end date:", datetime.date(2020, 12, 31)
                )
                frequency = st.selectbox(
                    "Select a temporal frequency:",
                    ["year", "quarter", "month", "week", "day"],
                    index=2,
                )
                reducer = st.selectbox(
                    "Select a reducer for aggregating data:",
                    ["median", "mean", "min", "max", "sum", "variance", "stdDev"],
                    index=0,
                )

                vis_params = st.text_area(
                    "Enter visualization parameters",
                    "",
                    help="Enter a string in the format of a dictionary, such as '{'min': 23, 'max': 32}'",
                )

                speed = st.slider("Frames per second:", 1, 30, 5)
                add_progress_bar = st.checkbox("Add a progress bar", True)
                progress_bar_color = st.color_picker("Progress bar color:", "#0000ff")
                font_size = st.slider("Font size:", 10, 50, 30)
                font_color = st.color_picker("Font color:", "#ffffff")
                font_type = st.selectbox(
                    "Select the font type for the title:",
                    ["arial.ttf", "alibaba.otf"],
                    index=0,
                )
                add_colorbar = st.checkbox("Add a colorbar", True)
                colorbar_label = st.text_input(
                    "Enter the colorbar label:", "Surface Temperature (°C)"
                )
                fading = st.slider(
                    "Fading duration (seconds) for each frame:", 0.0, 3.0, 0.0
                )
                mp4 = st.checkbox("Save timelapse as MP4", True)

            empty_text = st.empty()
            empty_image = st.empty()
            empty_video = st.container()

            roi = newGeoJSon
            # if st.session_state.get("roi") is not None:
            #     roi = st.session_state.get("roi")
            out_gif = geemap.temp_file_path(".gif")

            submitted = st.form_submit_button("Submit")
            if submitted:

                empty_text.text("Computing... Please wait...")
                try:
                    if collection == "MODIS Gap filled Land Surface Temperature Daily":
                        out_gif = geemap.create_timelapse(
                            st.session_state.get("ee_asset_id"),
                            start_date=start_date.strftime("%Y-%m-%d"),
                            end_date=end_date.strftime("%Y-%m-%d"),
                            region=roi,
                            bands=None,
                            frequency=frequency,
                            reducer=reducer,
                            date_format=None,
                            out_gif=out_gif,
                            palette=st.session_state.get("palette"),
                            vis_params=None,
                            dimensions=768,
                            frames_per_second=speed,
                            crs="EPSG:3857",
                            overlay_data=overlay_data,
                            overlay_color=overlay_color,
                            overlay_width=overlay_width,
                            overlay_opacity=overlay_opacity,
                            title=title,
                            title_xy=("2%", "90%"),
                            add_text=True,
                            text_xy=("2%", "2%"),
                            text_sequence=None,
                            font_type=font_type,
                            font_size=font_size,
                            font_color=font_color,
                            add_progress_bar=add_progress_bar,
                            progress_bar_color=progress_bar_color,
                            progress_bar_height=5,
                            add_colorbar=add_colorbar,
                            colorbar_label=colorbar_label,
                            loop=0,
                            mp4=mp4,
                            fading=fading,
                        )
                except:
                    empty_text.error(
                        "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                    )

                if out_gif is not None and os.path.exists(out_gif):

                    geemap.reduce_gif_size(out_gif)

                    empty_text.text("Right click the GIF to save it to your computer👇")
                    empty_image.image(out_gif)

                    out_mp4 = out_gif.replace(".gif", ".mp4")
                    if mp4 and os.path.exists(out_mp4):
                        with empty_video:
                            st.text("Right click the MP4 to save it to your computer👇")
                            st.video(out_gif.replace(".gif", ".mp4"))

                else:
                    st.error(
                        "Something went wrong. You probably requested too much data. Try reducing the ROI or timespan."
                    )

"""
