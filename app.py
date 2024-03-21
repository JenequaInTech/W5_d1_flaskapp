from flask import Flask

app = Flask(__name__)

movies = []

@app.route('/')
def index():
    return "Welcome to My Movie Collection App!"

@app.route('/movies')
def list_movies():
    return str(movies)

if __name__ == '__main__':
    app.run(debug=True)
    from flask import request

# ...

@app.route('/add_movie', methods=['GET'])
def add_movie():
    title = request.args.get('title')
    director = request.args.get('director')
    release_date = request.args.get('release_date')
    
    if not title or not director or not release_date:
        return "Missing information", 400  # Bad request
    
    movie = {
        'title': title,
        'director': director,
        'release_date': release_date
    }
    movies.append(movie)
    return f"Added movie: {movie}", 201

@app.route('/update_movie', methods=['GET'])
def update_movie():
    title = request.args.get('title')
    new_title = request.args.get('new_title')
    director = request.args.get('director')
    release_date = request.args.get('release_date')
    
    # Find the movie by title
    movie = next((m for m in movies if m['title'] == title), None)
    if not movie:
        return "Movie not found", 404
    
    # Update movie details
    if new_title:
        movie['title'] = new_title
    if director:
        movie['director'] = director
    if release_date:
        movie['release_date'] = release_date
    
    return f"Updated movie: {movie}", 200