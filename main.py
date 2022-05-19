from flask import Flask, render_template, redirect, url_for, request
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
# show a list of films and shows, divided into those known by the user and those not.
# allow user to add films to their list of known films.


def send_TMDB_api_request(api_request, params=None):
    if params:
        response = requests.get(api_request, params=params)
    else:
        response = requests.get(api_request)
    response.raise_for_status()
    return response.json()


def list_movies_by_name(movie_name):
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/search/movie?api_key={key}"
    params = {
        'query': movie_name,
        'include_adult': 'false',
        'page': '1'
    }
    response = send_TMDB_api_request(api_request, params)["results"]
    return [{
        'id': film['id'],
        'original_title': film['original_title'],
        'poster': f"{IMAGE_PREFIX}{film['poster_path']}",
        'release_date': film['release_date'],
        'overview': film['overview']
    } for film in response]


# Doesn't seem necessary
def get_actor_image(person_id):
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/person/{person_id}/images?api_key={key}"
    image = send_TMDB_api_request(api_request)
    return image


def list_actors_with_images(movie_id):
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={key}&language=en-US"
    cast_list = send_TMDB_api_request(api_request)['cast']
    return [{
        'id': cast_member['id'],
        'name': cast_member['name'],
        'character': cast_member['character'],
        'image_url': f"{IMAGE_PREFIX}{cast_member['profile_path']}"
    } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']


def list_actors_other_works(person_id):
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={key}&language=en-US"
    other_works = send_TMDB_api_request(api_request)['cast']
    return [{
        'id': film['id'],
        'original_title': film['original_title'],
        'poster_path': f"{IMAGE_PREFIX}{film['poster_path']}",
        'release_date': film['release_date'],
        'overview': film['overview'],
        'character': film['character']
    } for film in other_works]


movie_list = list_movies_by_name("RENT")
print(movie_list)
print(movie_list[0]['id'])
actor_list = list_actors_with_images(movie_list[0]['id'])
print(actor_list[0]['id'])
other_works = list_actors_other_works(actor_list[0]['id'])
print(other_works)


#---------------- Site Functionality -----------------

# Flask App
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", work_name=None)

@app.route('/work_input', methods=["GET", "POST"])
def work_input():
    work_name = request.form["work"]
    return render_template("movie.html", works=list_movies_by_name(work_name), work_name=None)

@app.route('/cast_list<work_id>', methods=["GET", "POST"])
def cast_list(work_id):
    return render_template("cast.html", cast=list_actors_with_images(work_id))

@app.route('/other_works<person_id>', methods=["GET", "POST"])
def other_works(person_id):
    return render_template("other_works.html", works=list_actors_other_works(person_id))

if __name__ == '__main__':
    app.run(debug=True)

# page to input a movie name, retrieve the cast list.


# process cast list selection, return a page of other works by that person.