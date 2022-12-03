import json
from flask import Flask
from flask import request
from db import db, Artist, Album, Song

"""
What we need:

file.db
controller.py
"""
app = Flask(__name__)
db_filename = 'spotify.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code
comment_id_counter = 1
@app.route('/')
def start():
    return 'Spotify Clone'

@app.route("/api/artists/")
def get_all_artists():
    """
    Returns all artists
    """
    artists = Artists.query.all()
    res = {'success': True, 'data': {"artists": [artist.serialize() for artist in artists]}}
    return json.dumps(res), 200

@app.route('/api/artists/<int:artist_id>/')
def get_albums_by_artists(artist_id):
    """
    gets artist by id
    """
    artist = DB.get_artist_by_id(artist_id)
    if artist is None:
        return json.dumps({"error": "Artist not found"}), 404
    return json.dumps({"id":artist.get("id"),"name":artist.get("name"),"album":artist.get("username")}), 200

@app.route("/api/artists/<int:artist_id>/", methods=["DELETE"])
def delete_artist(artist_id):
    """
        delete an artist by id
    """
    artist = DB.get_artist_by_id(artist_id)
    deleted_artist = DB.get_(artist_id)
    if artist is None:
        return json.dumps({"error": "Artist not found"}), 404
    DB.delete_artist_by_id(artist_id)
    return json.dumps({"id":artist.get("id"),"name":artist.get("name"),"username":artist.get("username")}), 200

@app.route("/api/artists/albums/songs/<int:song_id>/comments/")
def get_song_comments(song_id):
    song = songs.get(song_id)
    if song is None:
        return json.dumps({"error": "Post not found!"}), 404

    alist = []
    for i in range(len(comments)):
        if comments[i].get("song_id") == song_id:

            id = comments[i].get("id")
            likes = comments[i].get("upvotes")
            text = comments[i].get("text")
            username = comments[i].get("username")

            alist.append({"id":id,
            "likes":upvotes,
            "text":text,
            "username":username
            })
    res = {"comments": list(alist)}
    return json.dumps(res), 200

@app.route("/api/artists/albums/songs/<int:song_id>/comments/", methods=["POST"])
def create_song_comment(song_id):
    global comment_id_counter
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")

    comment = {"songid": song_id,
    "id": comment_id_counter,
    "like": 1,
    "text": text,
    "username": username
    }
    comments[comment_id_counter] = comment
    comment_id_counter += 1
    return json.dumps(comment),200

@app.route("/api/artists/albums/songs/<int:song_id>/comments/<int:comment_id>/", methods=["POST"])
def editComment(song_id,comment_id):
    comment = comments.get(comment_id)
    if comment is None:
        return json.dumps({"error": "Comment not found"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    comment["text"] = text
    return json.dumps(comment), 200

@app.route("/albums/<int:album_id>/")
def get_album(album_id):
    """
    Endpoint for getting an album by ID
    """
    album = Album.query.filter_by(id=album_id).first()
    if album is None:
        return json.dumps({"error": "Album not found"}), 404
    return json.dumps(album.serialize()), 200


@app.route("/artist/<int:artist_id>/album/", methods=["Post"])
def add_album(artist_id):
    body = json.loads(request.data)
    artist = Artist.query.filter_by(id=artist_id).first()
    if artist is None:
        return json.dumps({"error":"Artist not found!"})
    new_album = Album(name = body.get("name"))
    db.session.add(new_album)
    db.session.commit()
    return json.dumps(new_album.serialize()), 200

# @app.route("/api/artists/<int:artist_id>/song/", methods=["POST"])
# def create_assignment(artist_id):
#     """
#     Endpoint for creating a new assignment(song) for a course(artist) by id
#     """
#     song = Song.query.filter_by(id=song_id).first()
#     if song is None:
#         return failure_response("Song not found!")
#     body = json.loads(request.data)
#     if body.get("Name") is None or body.get("album_id") is None:
#         return failure_response("Enter a title and due_date!",400)
#     title = body.get("title")
#     due_date = body.get("due_date")
#     new_assignment = Assignment(title=title, due_date=due_date, song_id=song_id)
#     db.session.add(new_assignment)
#     course.assignments.append(new_assignment)
#     db.session.commit()
#     return success_response(new_assignment.serialize(), 201)
#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
