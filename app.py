# hume aapki zarurat hai
# importing dependencies
import streamlit as st
import time
import numpy as np
import pandas as pd
import PIL as img
import requests
from io import BytesIO      # for images


# Title
st.title("Restaurant Analysis System")

# Menu
menu_options = ["Home", "Reviews", "About Us", "Contact Us"]
choice = st.sidebar.selectbox("Menu", menu_options)

# Section 1: Review Collection
st.header("Review Collection")
st.write("Gather restaurant reviews from sources like Yelp and Google Reviews.")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [12.58, 77.35],
    columns=['lat', 'lon'])

st.map(map_data)

''''Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
'''