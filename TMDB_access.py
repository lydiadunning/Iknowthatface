import requests
import os
from dotenv import load_dotenv

from test import error_insertion

load_dotenv()


class TMDB:
    def __init__(self):
        self.key = os.getenv('TMDB_SECRET_KEY')
        self.image_prefix = 'https://www.themoviedb.org/t/p/original'

    def send_api_request(self, api_request, params=None, headers=None, json=None):
        response = requests.get(f'https://api.themoviedb.org/3{api_request}', params=params, headers=headers, json=json)
        response.raise_for_status()
        return response.json()

    def organize_results(self, response_dict, **kwargs):
        # expects kwargs where the keyword is the desired key and the argument is the existing key
        return_dict = {}
        for key, value in kwargs.items():
            if value in response_dict.keys():
                if response_dict[value]:
                    if key == 'poster' or key == 'actor_image_url':
                        return_dict[key] = f"{self.image_prefix}{response_dict[value]}"
                    else:
                        return_dict[key] = response_dict[value]
                else:
                    return_dict[key] = None
            else:
                return_dict[key] = None
        return return_dict

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

            result['movie'] = [self.organize_results(
                movie,
                id='id',
                title='title',
                poster='poster_path',
                release_date='release_date',
                overview='overview') for movie in movie_response]

        if tv_response:
            result['tv'] = [self.organize_results(
                tv,
                id='id',
                name='name',
                poster='poster_path',
                first_air_date='first_air_date',
                overview='overview'
            ) for tv in tv_response]
        return result


    def list_actors_with_images(self, medium, work_id):
        # medium is a string, either 'tv' or 'movie
        query = 'aggregate_credits' if medium == 'tv' else 'credits'
        api_request = f"/{medium}/{work_id}/{query}?api_key={self.key}&language=en-US"
        cast_list = self.send_api_request(api_request)['cast']

        return [{
            'id': cast_member['id'],
            'name': cast_member['name'],
            'character': cast_member['character'] if 'character' in cast_member.keys() else cast_member['roles'][0]['character'],
            'actor_image_url': f"{self.image_prefix}{cast_member['profile_path']}" if cast_member['profile_path'] else None

        } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']

    
    def list_actors_other_works(self, person_id):
        movie_api_request = f"/person/{person_id}/movie_credits?api_key={self.key}&language=en-US"
        tv_api_request = f"/person/{person_id}/tv_credits?api_key={self.key}&language=en-US"
        other_movies = self.send_api_request(movie_api_request)['cast']
        other_tv = self.send_api_request(tv_api_request)['cast']
        result = {}
        if other_movies:
            result['movie'] = [self.organize_results(
                movie,
                id='id',
                title='title',
                character='character',
                poster='poster_path',
                release_date='release_date',
                overview='overview') for movie in other_movies]
        if other_tv:
            result['tv'] = [self.organize_results(
                tv,
                id='id',
                name='name',
                character='character',
                poster='poster_path',
                first_air_date='first_air_date',
                overview='overview'
            ) for tv in other_tv]
        return result
    
    
    
    
