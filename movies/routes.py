from flask import request, jsonify, json
from flask.views import MethodView
from flask_smorest import abort
from uuid import uuid4

from . import bp
from schemas import movieSchema
from db import users, movies

@bp.route('/movie')
class movieList(MethodView):
    
    @bp.arguments(movieSchema)
    def movie(self, movie_data):
        if movie_data['author'] not in users:
            return {"message": "user does not exist"}, 400
        movie_id = uuid4().hex
        movies[movie_id] = movie_data

        return {
            'message': "movie created",
            'movie-id': movie_id
            }, 201

    @bp.response(200, movieSchema(many=True))
    def get(self):
        return list(movies.values())

@bp.route('/movie/<movie_id>')
class movie(MethodView):

    @bp.response(200, movieSchema)
    def get(self, movie_id):
        try: 
            return movies[movie_id]
        except KeyError:
            return {'message':"invalid movie"}, 400

    @bp.arguments(movieSchema)
    def put(self, movie_data, movie_id):
        if movie_id in movies:
            movies[movie_id] = {k:v for k,v in movie_data.items() if k != 'id'} 

            return {'message': f'movie: {movie_id} updated'}, 201
        
        return {'message': "invalid movie"}, 400

    def delete(self, movie_id):

        if movie_id not in movies:
            return { 'message' : "Invalid movie"}, 400
        
        movies.pop(movie_id)
        return {'message': f'movie: {movie_id} deleted'}