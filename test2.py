import streamlit as st
import mysql.connector as ms
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()
db_user = "root"
db_password = "sahaj2003"
db_host = "localhost"
db_name = "restaurantreviewdb"

# Function to get database connection
def get_database_connection():
    return ms.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )

# Function to fetch restaurant names from the database
def get_restaurant_names():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT restaurant_id, name FROM Restaurants")
        restaurants = cursor.fetchall()
        cursor.close()
        return {name: restaurant_id for restaurant_id, name in restaurants}
    except ms.Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
    return {}

# Function to fetch reviews and images for a specific restaurant from the database
def get_reviews_for_restaurant(restaurant_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT customer_id, review_text, rating, image_path 
            FROM RatingsReviews 
            WHERE restaurant_id = %s
            """, 
            (restaurant_id,)
        )
        reviews = cursor.fetchall()
        cursor.close()
        return reviews
    except ms.Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
    return []

# Streamlit app
st.title("Restaurant Reviews and Images")

# Dropdown menu to select a restaurant
restaurants = get_restaurant_names()
if restaurants:
    selected_restaurant = st.selectbox("Select a Restaurant", list(restaurants.keys()))

    # Fetch reviews and images for the selected restaurant
    restaurant_id = restaurants[selected_restaurant]
    reviews = get_reviews_for_restaurant(restaurant_id)

    if reviews:
        for customer_id, review_text, rating, image_path in reviews:
            st.subheader("Review by Customer ID: " + customer_id)
            st.write(f"Rating: {rating}/5")
            st.write("Review:")
            st.write(review_text)
            
            if image_path:
                # Convert backslashes to forward slashes if needed
                image_path = image_path.replace('\\', '/')
                
                # Check if file exists and open the image
                if os.path.exists(image_path):
                    try:
                        with open(image_path, "rb") as image_file:
                            image = Image.open(image_file)
                            st.image(image, caption="Review Image", use_column_width=True)
                    except Exception as e:
                        st.write(f"Error loading image: {e}")
                else:
                    st.write("No image available for this review.")
    else:
        st.write("No reviews found for this restaurant.")
else:
    st.write("No restaurants found in the database.")
