import requests
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SECRET_KEY')
# the way I handle the api key in this code is a mess, revisit.

# image prefix = https://www.themoviedb.org/t/p/w220_and_h330_face/

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
        'poster_path': film['poster_path'],
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
        'image_url': cast_member['profile_path']
    } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']


def list_actors_other_works(person_id):
    key = API_KEY
    api_request = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={key}&language=en-US"
    other_works = send_TMDB_api_request(api_request)['cast']
    return [{
        'id': film['id'],
        'original_title': film['original_title'],
        'poster_path': film['poster_path'],
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
