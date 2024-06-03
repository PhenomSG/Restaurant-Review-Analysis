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


st.title("Welcome to Restaurant Review Analysis System!")

sidebar_options = ["Home", "Reviews", "About Us", "Contact Us"]

choice = st.sidebar.selectbox("Menu", sidebar_options)

# Home Page
if choice == "Home":
    st.write(
        """
        ## Hum Kaun hai!
        # chutiye --
        We review delicious dishes from around the world.
        """
    )

# SidePage
elif choice == "Reviews":

    def generate_restaurant_data(num_restaurants):
        data = {
            "Restaurant Name": [f"Restaurant {i+1}" for i in range(num_restaurants)],
            "Location": ["Bangalore" for _ in range(num_restaurants)],
            "Rating": np.random.randint(1, 6, size=num_restaurants),
            "Reviews": np.random.randint(50, 1000, size=num_restaurants)
        }
        return pd.DataFrame(data)

    bangalore_restaurants = generate_restaurant_data(10)

    st.title("Restaurant Reviews Analysis System")
    
    # recent reviews
    st.header("Recent Reviews")
    st.write("""
        Here are some of the most recent reviews from our users:

        - **Restaurant 1**: "Excellent food and service!"
        - **Restaurant 2**: "Average experience, could be better."
        - **Restaurant 3**: "Delicious food, but service was slow."
    """)

    # Reviews stats section
    st.header("Reviews Statistics")
    st.write(f"""
        ### Average Rating: {bangalore_restaurants['Rating'].mean():.2f}
        ### Total Reviews: {bangalore_restaurants['Reviews'].sum()}
    """)

    # dataframe of restrau
    st.header("Restaurants in Bangalore")
    st.dataframe(bangalore_restaurants)


# About Us Page
elif choice == "About Us":
    st.write(
        """
        ## About Us

        Welcome to Restaurant Reviews Analysis System! We are passionate about food and helping people discover the best dining experiences.

        Our mission is to provide valuable insights and information about restaurants to help users make informed decisions when choosing where to dine. 

        At Restaurant Reviews Analysis System, we aggregate reviews from various sources, analyze them to extract meaningful insights, and present them to you in a user-friendly format.

        Whether you're looking for the top-rated restaurants in your city or want to explore new dining options, we've got you covered. 

        We believe that good food brings people together and creates unforgettable memories. Join us in our journey to explore the culinary world and discover your next favorite restaurant!

        If you have any questions or feedback, feel free to reach out to us. We'd love to hear from you!

        Happy dining!

        The Restaurant Reviews Analysis System Team
        """
    )


# Contact Us Page
elif choice == "Contact Us":
    st.write(
        """
        ## Contact Us

        **Address:** Dayananda Sagar College of Engineering

        **Phone:** 6969-6969-6969

        **Email:** chutiye@rranalysis.com
        """
    )


