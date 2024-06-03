# hume aapki zarurat hai
# importing dependencies
import streamlit as st
import numpy as np
import pandas as pd
import PIL as img
import requests
from io import BytesIO      # ye kya hai bc

# Title
st.title("Restaurant Analysis System")

# Section 1: Review Collection
st.header("Review Collection")
st.write("Gather restaurant reviews from sources like Yelp and Google Reviews.")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [12.58, 77.35],
    columns=['lat', 'lon'])

st.map(map_data)