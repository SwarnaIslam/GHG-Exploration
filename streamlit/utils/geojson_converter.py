import geojson

# Define the country name and its bounding box coordinates
country_name = "Bangladesh"
bounding_box = (88.0844222351, 20.670883287, 92.6727209818, 26.4465255803)

# Create a GeoJSON Feature for the bounding box
geojson_feature = geojson.Feature(
    geometry=geojson.Polygon(
        [
            [
                (bounding_box[0], bounding_box[1]),  # Southwest corner
                (bounding_box[2], bounding_box[1]),  # Southeast corner
                (bounding_box[2], bounding_box[3]),  # Northeast corner
                (bounding_box[0], bounding_box[3]),  # Northwest corner
                (bounding_box[0], bounding_box[1]),  # Closing the polygon
            ]
        ]
    ),
    properties={"name": country_name},
)

# Create a GeoJSON FeatureCollection
geojson_collection = geojson.FeatureCollection([geojson_feature])
print(geojson_collection)