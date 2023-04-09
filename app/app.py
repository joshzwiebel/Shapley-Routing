import streamlit as st
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance
from shapleyrouting.rideshare import RideShare
from time import sleep
from random import randint
import requests

@st.cache_resource
def get_Nominatim():
    geolocator = Nominatim(user_agent="ShapleyRouting1")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=5)
    return geocode

geocode = get_Nominatim()
@st.cache_data
def geocode_location(location):
    return geocode(location)

@st.cache_data
def requests_geocode(location):
    # url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'
    url = f"https://geocode.maps.co/search?q={location}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()[0]
    else:
        return None

num_locations = st.sidebar.slider('Number of locations', 2, 10, 3)
locations = []
st.sidebar.write(
    """Enter Locations in the order they will be visited,
    where the first location is the starting location"""
)
for i in range(num_locations):
    location_option = st.sidebar.text_input(
        f'Enter Location {i + 1}', 'University of Waterloo'
    )
    location_geocoded = requests_geocode(location_option)
    locations.append(location_geocoded)
cost = st.sidebar.number_input("Total cost of ride", 0.0, 100000.0, 100.0, 0.01)
run_button = st.sidebar.button('Run')
if run_button:
    try:
        map_data = pd.DataFrame(
            {
                'lat': [float(location['lat']) for location in locations],
                'lon': [float(location['lon']) for location in locations],
            }
        )
        st.write(map_data)
    except AttributeError and TypeError:
        st.write('Please enter valid locations')
        st.stop()

    st.map(map_data)

    distance_matrix = np.zeros((num_locations, num_locations))
    if locations:
        for i in range(num_locations):
            for j in range(num_locations):
                distance_matrix[i][j] = distance(
                    (locations[i]['lat'], locations[i]['lon']),
                    (locations[j]['lat'], locations[j]['lon']),
                ).km

    st.write(distance_matrix)

    ride = RideShare(num_players=num_locations - 1, distances=distance_matrix)

    shap_vals = ride.fit()
    #normalize shap vals to sum to cost
    shap_vals = np.array(shap_vals) * cost / np.sum(shap_vals)

    st.write(f"For a trip of {cost} dollars starting at {locations[0]['display_name']}, the optimal split is as follows:")
    for i in range(num_locations - 1):
        st.write(f"Player {i + 1} pays {round(shap_vals[i],2)} dollars to travel to {locations[i + 1]['display_name']}")
    