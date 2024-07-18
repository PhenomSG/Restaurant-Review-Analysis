import streamlit as st
import os
from dotenv import load_dotenv
import textwrap
import google.generativeai as genai
from IPython.display import Markdown
import mysql.connector as ms
from connection import is_connected, get_database_connection 

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI
genai.configure(api_key=google_api_key)

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

# Function to fetch reviews from the database based on selected restaurant
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

# Function to generate content using Gemini API
def generate_reviews_of_restaurants(reviews):
    try:
        # Initialize the generative model
        model = genai.GenerativeModel('gemini-pro')
        
        # Joining reviews into a single prompt
        full_reviews = " ".join(reviews)
        additional_info = "according to these reviews, tell what is good in the restaurant, what is bad, and how can we improve it.if data is not given just improvise and give something"
        prompt = full_reviews + additional_info
        
        # Generate content
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

# Streamlit app
st.title("Restaurant Review Generator")

# Fetch restaurant names from the database
restaurants = get_restaurant_names()

# Dropdown menu to select a restaurant
selected_restaurant = st.selectbox("Select a Restaurant", list(restaurants.keys()))

# Button to generate reviews
if st.button("Gemini Thinking"):
    # Get restaurant ID from selected restaurant name
    restaurant_id = restaurants[selected_restaurant]
    
    # Get reviews for the selected restaurant from the database
    reviews = get_reviews_for_restaurant(restaurant_id)
    
    if reviews:
        # Generate ratings based on reviews using Gemini API
        rating_content = generate_reviews_of_restaurants(reviews)
        
        # Display results
        st.markdown(textwrap.indent(rating_content, '> ', predicate=lambda _: True))
    else:
        st.write("No reviews found for this restaurant.")
