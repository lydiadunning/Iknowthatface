from flask import Flask, render_template, redirect, url_for, request, flash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SECRET_KEY')
# the way I handle the api key in this code is a mess, revisit.

IMAGE_PREFIX = 'https://www.themoviedb.org/t/p/w220_and_h330_face'

# Basic use sequence:
# Input a movie or series name.
# Display a list of actor images.
# User chooses an actor.
# show a list of movies and shows, divided into those known by the user and those not.
# allow user to add movies to their list of known movies.

# possible additions:
# images of the actor, where available, in each work.
# more attractive, more usable front end
# user sign in.
# maintain lists of viewed works and prioritize results from those lists.
# I haven't added any "i've seen this" functionality at all, which was part of my original vision for this project.
# As good a choice as any. API interface -> basic web functionality -> refine API interface is a good start.
# fix secret key to identify session





def send_TMDB_api_request(api_request, params=None):
    if params:
        response = requests.get(api_request, params=params)
    else:
        response = requests.get(api_request)
    response.raise_for_status()
    return response.json()


def list_works_by_name(work_name):
    key = API_KEY
    movie_api_request = f"https://api.themoviedb.org/3/search/movie?api_key={key}"
    tv_api_request = f"https://api.themoviedb.org/3/search/tv?api_key={key}"
    params = {
        'query': work_name,
        'include_adult': 'false',
        'page': '1'
    }
    movie_response = send_TMDB_api_request(movie_api_request, params)["results"]
    tv_response = send_TMDB_api_request(tv_api_request, params)["results"]
    result = {}
    if movie_response:
        result['movie'] = [{
            'id': movie['id'],
            'original_title': movie['original_title'],
            'poster': f"{IMAGE_PREFIX}{movie['poster_path']}",
            'release_date': movie['release_date'],
            'overview': movie['overview']
        } for movie in movie_response]
    if tv_response:
        result['tv'] = [{
            'id': tv['id'],
            'name': tv['name'],
            'poster': f"{IMAGE_PREFIX}{tv['poster_path']}",
            'first_air_date': tv['first_air_date'],
            'overview': tv['overview']
        } for tv in tv_response]
    return result

def list_actors_with_images(medium, work_id):
    # medium is a string, either 'tv' or 'movie
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/{medium}/{work_id}/credits?api_key={key}&language=en-US"
    cast_list = send_TMDB_api_request(api_request)['cast']
    return [{
        'id': cast_member['id'],
        'name': cast_member['name'],
        'character': cast_member['character'],
        'image_url': f"{IMAGE_PREFIX}{cast_member['profile_path']}"
    } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']



def list_actors_other_works(person_id):
    key = API_KEY
    movie_api_request = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={key}&language=en-US"
    tv_api_request = f"https://api.themoviedb.org/3/person/{person_id}/tv_credits?api_key={key}&language=en-US"
    other_movies = send_TMDB_api_request(movie_api_request)['cast']
    other_tv = send_TMDB_api_request(tv_api_request)['cast']
    result = {}
    if other_movies:
        print(other_movies)
        result['movie'] = [{
            'id': movie['id'],
            'original_title': movie['original_title'],
            'poster': f"{IMAGE_PREFIX}{movie['poster_path']}",
            'release_date': movie['release_date'],
            'overview': movie['overview']
        } for movie in other_movies]
    if other_tv:
        print(other_tv)
        result['tv'] = [{
            'id': tv['id'],
            'name': tv['name'],
            'poster': f"{IMAGE_PREFIX}{tv['poster_path']}",
            'first_air_date': tv['first_air_date'],
            'overview': tv['overview']
        } for tv in other_tv]
    return result






#---------------- Site Functionality -----------------

# Flask App
app = Flask(__name__)
# the following secret key is a placeholder to bypass an error.
# Replace with a real secret key.
app.secret_key = '1818181818181818'

@app.route('/')
def index():
    return render_template("index.html", work_name=None)

@app.route('/work_input', methods=["GET", "POST"])
def work_input():
    work_name = request.form["work"]
    works_found = list_works_by_name(work_name)
    if works_found:
        return render_template("movie.html", works=works_found, work_name=None)
    else:
        flash(f'No results for {work_name}.')
        return redirect(url_for('index'))

@app.route('/cast_list/<medium>/<work_id>', methods=["GET", "POST"])
def cast_list(medium, work_id):

    return render_template("cast.html", cast=list_actors_with_images(medium, work_id))

@app.route('/other_works/<person_id>', methods=["GET", "POST"])
def other_works(person_id):
    return render_template("other_works.html", works=list_actors_other_works(person_id))

if __name__ == '__main__':
    app.run(debug=True)
