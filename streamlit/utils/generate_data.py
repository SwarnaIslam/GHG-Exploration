"""
How to use this code to download data for any dataset and asset:

1. Set the desired collection name:
   collection_name = "your-desired-collection-name"

2. Adjust the world_geojson if needed to define a different area of interest.

3. Modify the limit parameter to control the number of items fetched:
   items = fetch_collection_items(collection_name, limit=your_desired_limit)

4. Choose the asset you want to analyze:
   asset_name = assets[your_desired_asset_index]

5. Run the script. It will fetch the items, generate statistics, clean the data,
   and save it to a CSV file in the "data" directory.
   
*NOTICE 1: 
We'll only consider either monthly or yearly data. NO DAILY DATA WE WILL USE

*NOTECE 2: 
And to know the limit you can visit any dataset website from nasa like this one https://earth.gov/ghgcenter/data-catalog/micasa-carbonflux-grid-v1
And you can see "Temporal Extent". From this value you can calculate how many years or month you need.

For example: in Micasa, 
Temporal Extent: January 1, 2001 - December 31, 2023
limits = 2023-2001 = (22 + 1) * 12 = 276 (+1 because we have to consider both 2001 and 2023)

Therefore for "micasa-carbonflux-monthgrid-v1" the limits=276 to fetch all data

By changing these parameters, you can easily adapt the code to download and
process data for any dataset and asset available through the STAC API.
"""

import csv
import json

import pandas as pd
import requests
import streamlit as st

RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"

############ FUNCTIONS ###############


def fetch_collection_items(collection_name, limit=100):
    """
    Function to fetch all items of a STAC collection.
    """
    url = f"{STAC_API_URL}/collections/{collection_name}/items"
    response = requests.get(url, params={"limit": limit})
    if response.status_code == 200:
        items = response.json().get("features", [])
        print(f"Found {len(items)} items for collection: {collection_name}")
        return items
    else:
        print(f"Failed to fetch items. Status code: {response.status_code}")
        return []


def generate_stats(item, geojson, asset_name, i):
    """
    Generate statistics for a given item and GeoJSON region.
    """
    try:
        result = requests.post(
            f"{RASTER_API_URL}/cog/statistics",
            params={"url": item["assets"][asset_name]["href"]},
            json=geojson,
        ).json()

        print(f">> DONE FETCHING STATS - {i+1}")

        return {
            **result["properties"],
            "datetime": item["properties"]["start_datetime"][:7],
        }
    except Exception as e:
        print(f"Error generating stats: {e}")
        return {}


def clean_stats(stats_json):
    """
    Clean and prepare stats for saving as a DataFrame.
    """
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["datetime"])
    return df


def save_stats_to_csv(df, collection_name):
    """
    Save the cleaned DataFrame to a CSV file.
    """
    csv_file = f"streamlit/data/{collection_name}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")
    return csv_file


def get_all_assets(items):

    try:
        return list(items[0]["assets"].keys())[:-1]

    except:
        return []


############ CUSTOMIZABLE PARAMS ###############


collection_name = "micasa-carbonflux-monthgrid-v1"
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

############ MAIN ###############

# Fetch items from the collection
items = fetch_collection_items(collection_name, limit=276)
assets = get_all_assets(items)

asset_name = assets[0]  # customizable

# Generate statistics for each item based on the world_geojson
stats = [
    generate_stats(item, world_geojson, asset_name, i) for i, item in enumerate(items)
]

# Clean the statistics data
df = clean_stats(stats)

# Save the cleaned data to a CSV file
csv_file = save_stats_to_csv(df, collection_name)
