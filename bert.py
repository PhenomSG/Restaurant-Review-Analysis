import mysql.connector
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

# Connect to the MySQL database
def get_reviews_from_db():
    conn = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT review_text FROM restaurant_reviews")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return [review[0] for review in reviews]

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

if __name__ == "__main__":
    main()
