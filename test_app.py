# importing dependencies
import folium
from streamlit_folium import st_folium
import streamlit as st
import numpy as np
import mysql.connector as ms
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# gemini api
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')


# Custom connection functions (replace with your own)
from connection import is_connected, get_database_connection

# Set page configuration
st.set_page_config(
    page_title="Sahaj",
    page_icon="🥘",  # rasode mein kaun tha
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

# Function to get restaurant names and IDs from the database
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
            cursor.execute("SELECT customer_id, review_text, rating FROM RatingsReviews WHERE restaurant_id = %s", (restaurant_id,))
            reviews = cursor.fetchall()
            cursor.close()
            return reviews
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

# Function to get address and plus code for a specific restaurant from the database
def get_address_pluscode_for_restaurant(restaurant_id):
    flag = is_connected()
    db = "restaurantreviewdb"
    if flag:
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(f"USE {db};")
            cursor.execute("SELECT address, plus_code FROM Restaurants WHERE restaurant_id = %s", (restaurant_id,))
            address_pluscode = cursor.fetchone()
            cursor.close()
            return address_pluscode
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
                for customer_id, review_text, rating in reviews:
                    st.write(f"**Customer ID:** {customer_id} | **Rating:** {rating}")
                    st.write(f"- {review_text}")
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

            st.header("Address and Location")
            address_pluscode = get_address_pluscode_for_restaurant(restaurant_id)
            if address_pluscode:
                address, plus_code = address_pluscode
                st.write(f"**Address:** {address}")
                st.write(f"**Plus Code:** {plus_code}")

                # Display map
                # Replace with accurate latitude and longitude from your database
                location_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
                folium.Marker([12.9716, 77.5946], tooltip="Restaurant Location").add_to(location_map)
                st_folium(location_map, width=700, height=500)
            else:
                st.write("No address information found.")
    else:
        st.write("No restaurants found.")

# About Us Page
elif choice == "About Us":
    st.write(
        """
        ## About Us

        Welcome to **Restaurant Reviews Analysis System**! We are passionate about food and dedicated to helping people discover the best dining experiences. Our mission is to provide valuable insights and information about restaurants to empower users in making informed decisions when choosing where to dine.

        At Restaurant Reviews Analysis System, we gather reviews from various sources, analyze them to extract meaningful insights, and present them to you in a user-friendly format.

        Whether you're searching for the top-rated restaurants in your city or exploring new dining options, we've got you covered.

        We believe that good food brings people together and creates unforgettable memories. Join us on our journey to explore the culinary world and discover your next favorite restaurant!

        *If you have any questions or feedback, please don't hesitate to reach out to us. We would love to hear from you!*

        **Happy dining!**

        *The Restaurant Reviews Analysis System Team*
        """
    )

# Contact Us Page
elif choice == "Contact Us":
    st.write(
        """
        ## Contact Us

        Have questions or feedback? We're here to help!

        - **Address:** Somewhere in Bangalore
        - **Phone:** +91 98076-XXXXX
        - **Email:** restraunt-reviews.com

        Feel free to reach out to us for any inquiries. We look forward to hearing from you!

        """
    )

# Analysis Page
elif choice == "Analysis":
    st.title("Restaurant Review Analysis System")
    st.header("Analysis")

    # Function to fetch restaurant names from the database
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

    # Function to fetch reviews for a specific restaurant from the database
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

    # Function to load BERT model and tokenizer
    def load_bert_model():
        model_name = "bert-base-uncased"
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
        return tokenizer, model

    # Function to perform sentiment analysis using BERT
    def analyze_sentiment(tokenizer, model, review):
        inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        positive_prob = probabilities[0][1].item()
        return positive_prob

    # Function to calculate average sentiment rating for reviews
    def calculate_average_sentiment(reviews, tokenizer, model):
        sentiments = []
        for review in reviews:
            sentiment = analyze_sentiment(tokenizer, model, review)
            sentiments.append(sentiment)
        if sentiments:
            return np.mean(sentiments)
        else:
            return None

    # Fetch restaurant names from database
    restaurants = get_restaurant_names()
    if restaurants:
        restaurant_names = list(restaurants.keys())
        selected_restaurant = st.selectbox("Select a Restaurant", restaurant_names)

        # Fetch reviews for selected restaurant
        restaurant_id = restaurants[selected_restaurant]
        reviews = get_reviews_for_restaurant(restaurant_id)

        if reviews:
            # Load BERT model and tokenizer
            tokenizer, model = load_bert_model()

            # Calculate average sentiment rating
            average_sentiment = calculate_average_sentiment(reviews, tokenizer, model)

            if average_sentiment is not None:
                # Normalize sentiment score to range 1-5
                normalized_score = np.interp(average_sentiment, [0, 1], [1, 5])
                integer_rating = round(normalized_score, 1)
                st.subheader(f"Average Sentiment Rating for {selected_restaurant}: {integer_rating}/5")
            else:
                st.subheader(f"Average Sentiment Rating for {selected_restaurant}: N/A")
        else:
            st.write("No reviews found for this restaurant.")
    else:
        st.write("No restaurants found in the database.")
