# web crawler to retrieve images of actors.
# from TMDB_access import TMDB
import requests
import os
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

def get_image_search_result(*terms):
    # This list comprehension, given any number of strings, returns a list of words in each string except "(voice)"
    # middle layer, used to flatten the list, was adapted from python docs,
    words = [word for word in [word for elem in [term.split() for term in terms] for word in elem] if word != '(voice)']
    search_terms = "+".join(words)
    api_key = os.getenv('SERP_API_KEY')
    query_string = f'https://serpapi.com/search.json?q={search_terms}&tbm=isch&ijn=0&api_key={api_key}'
    response = requests.get(query_string)
    response.raise_for_status()
    return response.json()['images_results'][0]['thumbnail']

# search_1 = 'Rent+Anthony+Rapp+Mark+Cohen'
# search_2 = ['Laura', 'Dern', 'Dora', 'the', 'Explorer']
# image_data = get_image_search_result('Laura Dern (voice)', 'Dora the Explorer')
# pprint(image_data)
