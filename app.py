# importing dependencies
import streamlit as st
import time
import numpy as np
import pandas as pd
import PIL as img
import requests
from io import BytesIO 
import base64
import mysql.connector as ms
#from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
from connection import is_connected, get_database_connection
import base64

# Set page configuration
st.set_page_config(
    page_title="Sahaj",
    page_icon="🥘",     # rasode mein kaun tha
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Welcome to Restaurant Review Analysis System!")

sidebar_options = ["Home", "Reviews", "Analysis", "About Us", "Contact Us"]

choice = st.sidebar.selectbox("Menu", sidebar_options)

# Home Page
if choice == "Home":
    st.write("## RESTAURANT")
    st.write("Welcome to our platform, where we review delicious dishes from around the world.")
    
    st.write("## Why We're Making This Project")
    st.write(
        """
        Many restaurant owners struggle to understand what is working and what needs improvement in their establishments. 
        Our project aims to bridge this gap by providing comprehensive reviews and actionable insights. Unlike typical reviews 
        on Google or Yelp, which often highlight only the extremes, our analysis delves deeper into the nuances of customer feedback.
        """
    )
    
    st.write("## Our Unique Approach")
    st.write(
        """
        - Detailed analysis of customer reviews to uncover hidden trends.
        - Clear reasoning behind the ratings provided.
        - Suggestions for improvement tailored to each restaurant's unique challenges.
        """
    )
    
    st.write("## Features")
    st.write(
        """
        - Comprehensive rating system based on sentiment analysis.
        - Insightful breakdown of strengths and weaknesses.
        - Actionable advice for restaurant owners to improve their services.
        """
    )
    
    st.write("## How We Differ from Google or Yelp Reviews")
    st.write(
        """
        Our reviews are not just about star ratings or brief comments. We provide:
        - In-depth analysis using advanced natural language processing techniques.
        - A balanced view that considers both positive and negative feedback.
        - Professional recommendations for enhancing the dining experience.
        """
    )

# Function to get restaurant names from the database
def get_restaurant_names():
    flag = is_connected()
    db = "restaurantreviewdb"
    if flag:
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(f"USE {db};")
            cursor.execute("SELECT restaurant_id, name FROM Restaurants")
            restaurants = cursor.fetchall()
            cursor.close()
            return {name: restaurant_id for restaurant_id, name in restaurants}
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    else:
        print("Failed to connect to MySQL")
    return {}

# Function to get reviews for a specific restaurant from the database
def get_reviews_for_restaurant(restaurant_id):
    flag = is_connected()
    db = "restaurantreviewdb"
    if flag:
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(f"USE {db};")
            cursor.execute("SELECT review_text FROM RatingsReviews WHERE restaurant_id = %s", (restaurant_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return [review[0] for review in reviews]
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    else:
        print("Failed to connect to MySQL")
    return []

# Function to get contact info for a specific restaurant from the database
def get_contact_info_for_restaurant(restaurant_id):
    flag = is_connected()
    db = "restaurantreviewdb"
    if flag:
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(f"USE {db};")
            cursor.execute("SELECT phone_number, website, email FROM RestrauContactInfo WHERE restaurant_id = %s", (restaurant_id,))
            contact_info = cursor.fetchone()
            cursor.close()
            return contact_info
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    else:
        print("Failed to connect to MySQL")
    return None

# Reviews Page
if choice == "Reviews":
    st.header("Select a Restaurant")
    restaurants = get_restaurant_names()
    if restaurants:
        selected_restaurant = st.selectbox("Choose a restaurant", list(restaurants.keys()))
        if selected_restaurant:
            restaurant_id = restaurants[selected_restaurant]
            
            st.header("Recent Reviews")
            reviews = get_reviews_for_restaurant(restaurant_id)
            if reviews:
                for review in reviews:
                    st.write(f"- {review}")
            else:
                st.write("No reviews found.")
            
            st.header("Contact Information")
            contact_info = get_contact_info_for_restaurant(restaurant_id)
            if contact_info:
                phone_number, website, email = contact_info
                st.write(f"**Phone Number:** {phone_number}")
                st.write(f"**Website:** {website}")
                st.write(f"**Email:** {email}")
            else:
                st.write("No contact information found.")
    else:
        st.write("No restaurants found.")

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

# Analysis Page
elif choice == "Analysis":
    st.write(
        """
        ## Analysis
        """
    )
