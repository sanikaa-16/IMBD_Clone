import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the movie data
movies_data = pd.read_csv('movies.csv')

# Ensure 'index' column exists for identification
if 'index' not in movies_data.columns:
    movies_data.reset_index(inplace=True)

# Select relevant features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Fill missing values
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine features into a single string
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + \
                    movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + \
                    movies_data['director']

# Convert text to feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Cosine similarity
similarity = cosine_similarity(feature_vectors)

# Movie titles list
movie_list = movies_data['title'].tolist()

# Recommendation function
def get_recommendations(movie_title, num=10):
    find_close_match = difflib.get_close_matches(movie_title, movie_list)
    if not find_close_match:
        return []

    close_match = find_close_match[0]
    index_of_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    
    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_list = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for movie in sorted_list[1:num+1]:  # Skip the first one (it's the movie itself)
        index = movie[0]
        title = movies_data.iloc[index]['title']
        recommendations.append(title)

    return recommendations, find_close_match[0]