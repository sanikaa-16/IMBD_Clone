from flask import Flask, render_template, request, redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from movie_recommendation_system import get_recommendations
from utils import fetch_movie_details

TMDB_API_KEY = '307d5a14824d0b215d8b0734e45c62cb'

# app = Flask(__name__)
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)

# class User(db.Model):



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return render_template('index.html', error='Please enter a search term.')

    movie_data = fetch_movie_details(query, TMDB_API_KEY)

    if not movie_data:
        return render_template('index.html', error='No results found or error fetching data.')

    return render_template('reviews.html', movie=movie_data)


@app.route('/recommend', methods=['GET'])
def recommend():
    return render_template('recommendations.html')

@app.route('/recommendations', methods=['GET'])
def recommendations():
    movie_name = request.args.get('movie_name')
    if not movie_name:
        return render_template('recommendations.html', error='Please enter a movie name.')

    recommended_titles,find_match = get_recommendations(movie_name)
    enriched_movies = []

    for title in recommended_titles:
        details = fetch_movie_details(title, TMDB_API_KEY)
        if details:
            enriched_movies.append(details)

    return render_template('recommendations.html', movie_recommendations=enriched_movies, movie_name = find_match)
    


if __name__ == '__main__':
    app.run(debug=True)