import requests
from dotenv import load_dotenv

import json
import os

# Dotenv
load_dotenv('conf/.env')

api_key = os.getenv('apikey')


def template_list(movie_list: list[dict]) -> str:
    template = '{position}. {title} ({rating} :star:) Propuesto por <@{proposed_by}>\n'
    message = 'Usa `!pelicula <núm.>` para obtener información de la pelicula\n\n'

    for index, movie in enumerate(movie_list):
        message += template.format(position=index + 1, title=movie['title'], rating=movie['rating'], proposed_by=movie['user_id'])

    return message


def template_query(movie_list: list[dict]) -> str:
    template = '{position}. {title} (`{id}`)\n'
    message = 'Usa `!agregar <id imdb>` con alguno de los resultados\n\n'
    true_titles = filter(lambda data: data['id'].startswith('tt'), movie_list)

    for index, movie in enumerate(true_titles):
        message += template.format(position=index + 1, title=movie['title'], id=movie['id'])

    return message


def imdb_search(query: str) -> list[dict]:
    response = requests.get(f'https://v3.sg.media-imdb.com/suggestion/x/{query}.json')
    response_data = response.json()['d']

    processed = [{'id': movie['id'], 'title': movie['l']} for movie in response_data]

    if processed[0]['id'].startswith('/'):
        processed.pop(0)

    return processed


def imdb_metadata(imdb_id: str) -> tuple:
    response = requests.get(f'https://www.omdbapi.com/?i={imdb_id}&apikey={api_key}')
    response_data = response.json()

    return response_data['Title'], response_data['Plot'], response_data['imdbRating'], response_data['Poster']


def add_movie(imdb_id: str, user_id: str) -> None:
    with open('conf/movies.json') as movies:
        current_movie_list = json.load(movies)

    title, plot, rating, poster = imdb_metadata(imdb_id)

    current_movie_list.append({'title': title, 'synopsis': plot, 'rating': rating, 'poster': poster, 'id': imdb_id, 'user_id': user_id})

    with open('conf/movies.json', 'w') as movies:
        json.dump(current_movie_list, movies, indent=4)

    return title


def clear_movie_list() -> None:
    with open('conf/movies.json', 'w') as movies:
        json.dump([], movies)

    return None


def read_movie_list() -> list:
    with open('conf/movies.json') as movies:
        return json.load(movies)
