from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from movie_recommendation_system import get_recommendations
from utils import fetch_movie_details
from datetime import datetime

TMDB_API_KEY = 'fc53c1f1fb70e9d2058b2473d2fdba03'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)  # TMDb movie ID
    movie_title = db.Column(db.String(255), nullable=False)  # Optional but helpful
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent duplicates: One user shouldn't have same movie twice
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='user_movie_uc'),)


with app.app_context():
    db.create_all()

def fetch_movie_details(movie_name, api_key):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': api_key,
        'query': movie_name
    }

    response = requests.get(url, params=params, timeout=10)  # Set timeout to 10 seconds
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            
            # Fetch the cast details from the movie's details endpoint
            movie_id = movie['id']
            cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
            cast_response = requests.get(cast_url, params={'api_key': api_key})
            if cast_response.status_code == 200:
                cast_data = cast_response.json()
                # Get only the top 5 cast members
                cast_list = [
                    {
                        'name': cast['name'],
                        'character': cast['character'],
                        'profile_url': f"https://image.tmdb.org/t/p/w500{cast['profile_path']}" if cast['profile_path'] else None
                    }
                    for cast in cast_data['cast'][:5]  # Limit to top 5 cast
                ]
                movie['cast'] = cast_list  # Add cast details to the movie data
                
            # Check for language
            movie['language'] = movie.get('original_language', 'Unknown')  # Fallback to 'Unknown' if not available
            
            # Check for rating
            movie['rating'] = movie.get('vote_average', 'N/A')  # Fallback to 'N/A' if not available
            
            # Check for reviews
            movie['reviews'] = movie.get('vote_count', 0)
            
            # Set a default value for the director
            movie['director'] = "Not Available"  
            
            # Check for director in the crew section
            for crew_member in cast_data['crew']:
                if crew_member['job'] == 'Director':
                    movie['director'] = crew_member['name']
                    break

            return movie
        else:
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None



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

    recommended_titles, find_match = get_recommendations(movie_name)
    enriched_movies = []
    print(recommended_titles)

    for title in recommended_titles:
        details = fetch_movie_details(title, TMDB_API_KEY)
        if details:
            enriched_movies.append(details)

    return render_template('recommendations.html', movie_recommendations=enriched_movies, movie_name=find_match)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('create_account'))

        existing_user = User.query.filter((User.email == email) | (User.phone == phone)).first()
        if existing_user:
            flash('Email or phone already registered.', 'error')
            return redirect(url_for('create_account'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('sign_in'))

    return render_template('create_account.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        login_input = request.form['login']  # can be email or phone
        password = request.form['password']

        user = User.query.filter((User.email == login_input) | (User.phone == login_input)).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Signed in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('sign_in'))

    return render_template('sign_in.html')

@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/add_to_watchlist/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    if 'user_id' not in session:
        flash('You need to sign in to add to your watchlist.', 'error')
        return redirect(url_for('sign_in'))

    movie_title = request.form.get('movie_title', '')  # get from hidden input
    user_id = session['user_id']

    # Check if it's already in watchlist
    existing = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing:
        flash('Movie already in watchlist.', 'info')
        return redirect(request.referrer or url_for('index'))

    new_entry = Watchlist(user_id=user_id, movie_id=movie_id, movie_title=movie_title)
    db.session.add(new_entry)
    db.session.commit()

    flash('Movie added to watchlist!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/view_watchlist')
def view_watchlist():
    if 'user_id' not in session:
        flash('You need to sign in to view your watchlist.', 'error')
        return redirect(url_for('sign_in'))

    user_id = session['user_id']
    entries = Watchlist.query.filter_by(user_id=user_id).all()

    movies = []
    for entry in entries:
        movie_details = fetch_movie_details(entry.movie_title, TMDB_API_KEY)  # You can also create a `fetch_movie_by_id()` to use movie_id directly
        if movie_details:
            movies.append(movie_details)

    return render_template('watchlist.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
