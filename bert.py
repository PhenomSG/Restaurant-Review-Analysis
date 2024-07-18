import mysql.connector as ms
from connection import is_connected, get_database_connection
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

# Connect to the MySQL database
def get_reviews_from_db():
    flag = is_connected()
    # print(flag)

    # Database to be used
    db = "restaurantreviewdb"
    db_tables = ["Restaurants","Customers","RestrauContactInfo","RatingsReviews"]
    print(f"Using {db} Database")
    print(f"All actions will happen inside {db} database")

    if flag:
        try:
            # Checking if connected
            connection = get_database_connection()
            cursor = connection.cursor()

            # Selecting the database
            cursor.execute(f"USE {db};")
            print(f"Database changed to {db}")

            # Sample query to test the connection
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("Tables in the database:", tables)
            cursor.execute("SELECT review_text FROM RatingsReviews")
            reviews = cursor.fetchall()
            cursor.close()
            ls =  [review[0] for review in reviews]
            for res in ls:
                print(res)
            return ls
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        print("Failed to connect to MySQL")

    #return [review[0] for review in reviews]

# Load pre-trained BERT model and tokenizer
def load_bert_model():
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    return tokenizer, model

# Perform sentiment analysis using BERT
def analyze_sentiment(tokenizer, model, review):
    inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    positive_prob = probabilities[0][1].item()
    return positive_prob

# Calculate average sentiment rating for all reviews
def calculate_average_sentiment(reviews, tokenizer, model):
    sentiments = []
    for review in reviews:
        sentiment = analyze_sentiment(tokenizer, model, review)
        sentiments.append(sentiment)
    return np.mean(sentiments)

# Main function
def main():
    reviews = get_reviews_from_db()
    tokenizer, model = load_bert_model()
    average_sentiment = calculate_average_sentiment(reviews, tokenizer, model)
    print(f"Average sentiment rating: {average_sentiment}")
    # Normalizing the score to the range 1-5
    # sentiment scores range from 0 to 1
    normalized_score = np.interp(average_sentiment, [0, 1], [1, 5])

    # Rounding normalized score to the nearest integer
    integer_rating = int(round(normalized_score))

    print(f"Average sentiment rating: {integer_rating}")

if __name__ == "__main__":
    main()
