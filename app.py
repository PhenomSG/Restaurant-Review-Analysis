# importing dependencies
import streamlit as st
import time
import numpy as np
import pandas as pd
import PIL as img
import requests
from io import BytesIO 
import base64

# Set page configuration
st.set_page_config(
    page_title="Sahaj",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background("E:/Sentiment_Analysis_Using_NLP/foodie.jpg")

# Your Streamlit app content goes here
st.title("Welcome to Restaurant Review Analysis System!")


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

