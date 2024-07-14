-- Create the database
CREATE DATABASE restaurantreviewdb;

-- Switch to the created database
USE restaurantreviewdb;

-- Create the Restaurants table
CREATE TABLE Restaurants (
    restaurant_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    plus_code VARCHAR(50),
    PRIMARY KEY (restaurant_id)
);

-- Create the Contact Information table
CREATE TABLE ContactInformation (
    restaurant_id INT NOT NULL,
    phone_number VARCHAR(20),
    website VARCHAR(255),
    email VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Create the Ratings / Reviews table
-- Create the Ratings / Reviews table with Image Path
CREATE TABLE RatingsReviews (
    review_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    review_text TEXT,
    rating FLOAT,
    image_path VARCHAR(255),
    PRIMARY KEY (review_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);


-- Create the Customers table
CREATE TABLE Customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    customer_email VARCHAR(255) UNIQUE,
    PRIMARY KEY (customer_id)
);
