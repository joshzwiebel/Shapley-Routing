import streamlit as st
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import distance
from shapleyrouting.rideshare import RideShare

geolocator = Nominatim(user_agent="ShapleyRouting")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

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
    location_geocoded = geocode(location_option)
    locations.append(location_geocoded)
try:
    map_data = pd.DataFrame(
        {
            'lat': [location.latitude for location in locations],
            'lon': [location.longitude for location in locations],
        }
    )
except AttributeError:
    st.write('Please enter valid locations')
    st.stop()

st.map(map_data)

st.write(locations)

distance_matrix = np.zeros((num_locations, num_locations))

for i in range(num_locations):
    for j in range(num_locations):
        distance_matrix[i][j] = distance(
            (locations[i].latitude, locations[i].longitude),
            (locations[j].latitude, locations[j].longitude),
        ).km

st.write(distance_matrix)

ride = RideShare(num_players=num_locations - 1, distances=distance_matrix)

st.write(ride.fit())
