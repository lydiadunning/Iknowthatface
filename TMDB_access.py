import requests
import os
from dotenv import load_dotenv
from viewed import Viewed

load_dotenv()


class TMDB:
    def __init__(self):
        self.key = os.getenv('SECRET_KEY')
        self.image_prefix = 'https://www.themoviedb.org/t/p/w220_and_h330_face'
        self.viewed = Viewed()

    def send_api_request(self, api_request, params=None, headers=None, json=None):
        response = requests.get(f'https://api.themoviedb.org/3{api_request}', params=params, headers=headers, json=json)
        response.raise_for_status()
        return response.json()


    def list_works_by_name(self, work_name):
        movie_api_request = f"/search/movie?api_key={self.key}"
        tv_api_request = f"/search/tv?api_key={self.key}"
        params = {
            'query': work_name,
            'include_adult': 'false',
            'page': '1'
        }
        movie_response = self.send_api_request(movie_api_request, params)["results"]
        tv_response = self.send_api_request(tv_api_request, params)["results"]
        result = {}
        if movie_response:
            movies = [{
                'id': movie['id'],
                'original_title': movie['original_title'],
                'poster': f"{self.image_prefix}{movie['poster_path']}",
                'release_date': movie['release_date'],
                'overview': movie['overview']
            } for movie in movie_response]
            result['movie'] = self.viewed.prioritize('movie', movies)

        if tv_response:
            tv_shows = [{
                'id': tv['id'],
                'name': tv['name'],
                'poster': f"{self.image_prefix}{tv['poster_path']}",
                'first_air_date': tv['first_air_date'],
                'overview': tv['overview']
            } for tv in tv_response]
            result['tv'] = self.viewed.prioritize('tv', tv_shows)
        return result
    
    def list_actors_with_images(self, medium, work_id):
        # medium is a string, either 'tv' or 'movie
        api_request = f"/{medium}/{work_id}/credits?api_key={self.key}&language=en-US"
        cast_list = self.send_api_request(api_request)['cast']
        return [{
            'id': cast_member['id'],
            'name': cast_member['name'],
            'character': cast_member['character'],
            'image_url': f"{self.image_prefix}{cast_member['profile_path']}"
        } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']
    
    
    
    def list_actors_other_works(self, person_id):
        movie_api_request = f"/person/{person_id}/movie_credits?api_key={self.key}&language=en-US"
        tv_api_request = f"/person/{person_id}/tv_credits?api_key={self.key}&language=en-US"
        other_movies = self.send_api_request(movie_api_request)['cast']
        other_tv = self.send_api_request(tv_api_request)['cast']
        result = {}
        if other_movies:
            movies = [{
                'id': movie['id'],
                'original_title': movie['original_title'],
                'character': movie['character'],
                'poster': f"{self.image_prefix}{movie['poster_path']}",
                'release_date': movie['release_date'],
                'overview': movie['overview']
            } for movie in other_movies if 'release_date' in movie.keys()]
            result['movie'] = self.viewed.prioritize('movie', movies)
        if other_tv:
            tv_shows = [{
                'id': tv['id'],
                'name': tv['name'],
                'character': tv['character'],
                'poster': f"{self.image_prefix}{tv['poster_path']}",
                'first_air_date': tv['first_air_date'],
                'overview': tv['overview']
            } for tv in other_tv if 'first_air_date' in tv.keys()]
            result['tv'] = self.viewed.prioritize('tv', tv_shows)
        print(result)
        return result
    
    
    
    
