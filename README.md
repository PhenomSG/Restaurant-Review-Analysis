# Restaurant Review Analysis System

## Project Overview

This project aims to build a comprehensive system for collecting and analyzing restaurant reviews. The system will:
1. Collect reviews from various platforms.
2. Analyze the sentiment of the reviews to generate a rating.
3. Provide explanations for the generated ratings.
4. Create a word cloud highlighting key themes from the reviews.
5. Analyze restaurant images to classify them based on suitability for different dining experiences (e.g., family, casual, date) and suggest improvements.

## Features

- **Review Collection**: Gather restaurant reviews from sources like Yelp and Google Reviews.
- **Sentiment Analysis**: Analyze the sentiment of the reviews to derive a rating.
- **Rating Explanation**: Provide detailed explanations for the generated ratings.
- **Word Cloud Generation**: Identify common themes in the reviews to create a word cloud.
- **Image Analysis**: Classify the restaurant type based on images and suggest improvements.

## Technology Stack

- **Python**: Main programming language.
- **Gemini Pro API**: Used for NLP and image analysis tasks.
- **NLP Libraries**: For additional natural language processing.
- **Image Processing Libraries**: For analyzing restaurant images.
- **Web Scraping Tools**: To collect reviews from various platforms.

## Installation

### Prerequisites

- Python 3.7 or higher
- API key for Gemini Pro

### Setup

1. Clone the repository:
    ```bash
    git clone [https://github.com/SahajG009/Sentiment_Analysis_Using_NLP.git](https://github.com/SahajG009/Sentiment_Analysis_Using_NLP.git)
    cd restaurant-review-analysis
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Gemini Pro API key:
    ```bash
    export GEMINI_API_KEY='your_gemini_api_key'
    ```

## Usage

### Collecting Reviews

To collect reviews from a source (e.g., Yelp), use the provided `collect_reviews_from_source` function:

```python
from review_collector import collect_reviews_from_source

reviews = collect_reviews_from_source('yelp', 'restaurant_id')
```

### Analyzing Reviews

To analyze sentiment and generate a rating:

```python
from review_analysis import sentiment_analysis, aggregate_ratings, gemini_pro_explain_rating

ratings = sentiment_analysis(reviews, model='gemini_pro')
overall_rating = aggregate_ratings(ratings)
explanation = gemini_pro_explain_rating(reviews, overall_rating)
```

### Generating a Word Cloud

To generate a word cloud from the reviews:

```python
from word_cloud_generator import extract_keywords, generate_word_cloud

word_cloud_data = extract_keywords(reviews)
generate_word_cloud(word_cloud_data)
```

### Analyzing Images

To classify restaurant type and suggest improvements based on images:

```python
from image_analysis import classify_restaurant_type, assess_image_quality

for image in restaurant_images:
    category = classify_restaurant_type(image, model='gemini_pro')
    improvements = assess_image_quality(image, model='gemini_pro')
    print(f"Category: {category}, Improvements: {improvements}")
```

## Directory Structure

```
restaurant-review-analysis/
│
├── README.md                # Project overview and instructions
├── requirements.txt         # List of dependencies
├── collect_reviews.py       # Functions for collecting reviews
├── review_analysis.py       # Functions for analyzing reviews
├── word_cloud_generator.py  # Functions for generating word clouds
├── image_analysis.py        # Functions for analyzing images
└── main.py                  # Main script to run the analysis
```

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Special thanks to the developers of the Gemini Pro API for providing a robust platform for NLP and image analysis.
- Thanks to the contributors of the various Python libraries used in this project.
