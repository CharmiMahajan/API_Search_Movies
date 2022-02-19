import os

import requests as requests
from flask import request, jsonify

from API_SearchMovies import db
from API_SearchMovies.Search_byID_api import api_id  # Blueprint
from API_SearchMovies.models import Movies


headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }


@api_id.route('/movies', methods=['GET', 'POST'])
def search():
    """
    search() will get the parameters from url and if key value is not empty than search by movie id, title,
    year released in, ratings and genres. [From Local DB]
    If User Search with title and title is not there in local db, then it will search for that movie title on omdb api.
    And if found then record of that movie will be added to the local db, else will raise an exception to Movie Not
    found.

    :return: JSON
    """
    movie_id = request.args.get('id')
    title = request.args.get('title')
    year = request.args.get('year')
    ratings = request.args.get('ratings')
    genre = request.args.get('genres')

    # SEARCH BY ID
    if movie_id:
        try:
            movie = Movies.query.with_entities(Movies.id, Movies.title, Movies.release_year, Movies.ratings,
                                               Movies.genre).filter_by(id=movie_id).all()
            result = generate_dicts(movie)
            if not result:
                return "CURRENTLY, NO DATA.."
            return jsonify(result, headers), 200
        except Exception as e:
            return "ID NOT FOUND" + str(e)

    # SEARCH BY TITLE
    if title:
        movie = Movies.query.filter(Movies.title.like(title)) \
            .with_entities(Movies.id, Movies.title, Movies.release_year, Movies.ratings, Movies.genre) \
            .order_by(Movies.id).all()

        # IF TITLE NOT IN DB, OMDB API CALL FROM HERE
        if not movie:
            try:
                result = get_data_from_omdb(title)
                save_to_db(result[0])
                if not result:
                    return "No Movie Found"
                return jsonify(result, headers), 200
            except Exception as e:
                return "Movie Name Not Found" + str(e)
        result = generate_dicts(movie)
        return jsonify(result, headers), 200

    # SEARCH BY YEAR
    if year:
        try:
            movie = Movies.query.filter(Movies.release_year.like(year)) \
                .with_entities(Movies.id, Movies.title, Movies.release_year, Movies.ratings, Movies.genre) \
                .order_by(Movies.id).all()
            result = generate_dicts(movie)
            if not result:
                return "CURRENTLY, NO DATA.."
            return jsonify(result, headers), 200
        except Exception as e:
            return "YEAR NOT FOUND" + str(e)

    # SEARCH BY RATINGS WHICH ARE GREATER THAN OR EQUAL
    if ratings:
        try:
            movie = Movies.query.filter(Movies.ratings >= ratings) \
                .with_entities(Movies.id, Movies.title, Movies.release_year, Movies.ratings, Movies.genre) \
                .order_by(Movies.id).all()
            result = generate_dicts(movie)
            if not result:
                return "CURRENTLY, NO DATA.."
            return jsonify(result, headers), 200
        except Exception as e:
            return "Wrong value entered or not found [Ratings:1 to 10]" + str(e)

    # SEARCH BY GENRES [ SEARCH IN STRING OF COLUMN ]
    if genre:
        try:
            movie = Movies.query.filter(Movies.genre.like('%,' + genre + ',%')) \
                .with_entities(Movies.id, Movies.title, Movies.release_year, Movies.ratings, Movies.genre) \
                .order_by(Movies.id).all()
            result = generate_dicts(movie)
            if not result:
                return "CURRENTLY, NO DATA.."
            return jsonify(result, headers), 200
        except Exception as e:
            return "GENRE NOT FOUND" + str(e)


def get_data_from_omdb(title):
    """
    If movie title searched not in db then route will come to this function.
    OMDB API is called using title and api_key as a passed parameters.
    Function will get the necessary data from JSON by JSON Manipulation and return result back to calling function.
    :param title: Movie title
    :return: result [type:dictionary]
    """
    api_key = os.getenv('API_KEY')
    url = "http://www.omdbapi.com/?t={}&type=movie&r=json&apikey={}"
    movie = requests.get(url.format(title, api_key)).json()
    result = []
    try:
        genre = list(movie['Genre'].split(','))
        genre = list(filter(None, genre))
        row = {
            'MovieID': movie['imdbID'],
            'Movie Title': movie['Title'],
            'Released in Year': movie['Year'],
            'Ratings': float(movie['imdbRating']),
            'Genres': genre
        }
        result.append(row)
        if not result:
            return "NO MOVIE FOUND"
        return result
    except Exception as e:
        return "NOT FOUND" + str(e)


def save_to_db(row):
    """
    data dictionary got from omdb api will be passed and data add to local db if not already available.
    :param row: movie data got from omdb api [type:dictionary]
    :return: "success" on "success" and exception on fail
    """
    try:
        movie = Movies.query.filter_by(id=row['MovieID']).first()
        if not movie:
            genre = ',' + ','.join(map(str, row['Genres'])) + ','
            new = Movies(id=row['MovieID'], title=row['Movie Title'], release_year=row['Released in Year'],
                         ratings=row['Ratings'], genre=genre)
            db.session.add(new)
            db.session.commit()
            return "Success"
    except Exception as e:
        return "Failed" + str(e)


def generate_dicts(movie):
    """
    To Generate List of dicts from db data, if multiple result dicts.
    :param movie: query results
    :return: result dict
    """
    if movie:
        result = []
        for i, val in enumerate(movie):
            genre = list(movie[i][4].split(","))
            genre = list(filter(None, genre))
            row = {
                'MovieID': movie[i][0],
                'Movie Title': movie[i][1],
                'Released in Year': movie[i][2],
                'Ratings': float(movie[i][3]),
                'Genres': genre
            }
            result.append(row)
            if not result:
                return "CURRENTLY, NO DATA.."
        return result
