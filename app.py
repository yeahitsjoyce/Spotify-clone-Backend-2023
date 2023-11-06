import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_filename = 'spotify.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

# Models (assuming you have these models defined somewhere)
# from models import Artist, Album, Song

# Helper Functions
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code

comment_id_counter = 1

@app.route('/')
def start():
    return 'Spotify Clone'

# Artists
@app.route("/api/artists/")
def get_all_artists():
    artists = Artist.query.all()
    res = {'success': True, 'data': [artist.serialize() for artist in artists]}
    return success_response(res)

@app.route('/api/artists/<int:artist_id>/')
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return failure_response("Artist not found")
    return success_response(artist.serialize())

@app.route("/api/artists/<int:artist_id>/", methods=["DELETE"])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist is None:
        return failure_response("Artist not found")
    db.session.delete(artist)
    db.session.commit()
    return success_response(artist.serialize())

# Albums
@app.route("/albums/<int:album_id>/")
def get_album(album_id):
    album = Album.query.get(album_id)
    if album is None:
        return failure_response("Album not found")
    return success_response(album.serialize())

@app.route("/artist/<int:artist_id>/album/", methods=["POST"])
def add_album(artist_id):
    body = json.loads(request.data)
    artist = Artist.query.get(artist_id)
    if artist is None:
        return failure_response("Artist not found")
    new_album = Album(name=body.get("name"), artist_id=artist_id)
    db.session.add(new_album)
    db.session.commit()
    return success_response(new_album.serialize())

# Add routes for songs and comments as needed

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

