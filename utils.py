import requests

def fetch_movie_details(query, TMDB_API_KEY):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    if not data.get('results'):
        return None

    movie = data['results'][0]
    movie_id = movie['id']

    credits_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    credits_params = {'api_key': TMDB_API_KEY}
    credits_response = requests.get(credits_url, params=credits_params)

    if credits_response.status_code != 200:
        director = 'Unknown'
        cast_list = []
        cast_string = ''
    else:
        credits_data = credits_response.json()
        directors = [member['name'] for member in credits_data.get('crew', []) if member['job'] == 'Director']
        director = ', '.join(directors) if directors else 'Unknown'

        top_cast = credits_data.get('cast', [])[:5]
        cast_string = ', '.join([member['name'] for member in top_cast])
        cast_list = [
            {
                'name': member['name'],
                'character': member['character'],
                'profile_url': f"https://image.tmdb.org/t/p/w185{member['profile_path']}" if member.get('profile_path') else '/static/default_profile.jpg'
            }
            for member in top_cast
        ]

    return {
        'title': movie['title'],
        'release_date': movie['release_date'],
        'overview': movie['overview'],
        'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else '',
        'rating': movie['vote_average'],
        'language': movie['original_language'],
        'reviews': movie['vote_count'],
        'adult': movie['adult'],
        'director': director,
        'cast_string': cast_string,
        'cast_list': cast_list
    }
