import json
from flask import Flask
from flask import request
from db import db, Artist, Album, Song
#from controller import """ """

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
def delete_user(artist_id):
    """
        delete an artist by id
    """
    artist = DB.get_artist_by_id(artist_id)
    deleted_transactions = DB.get_transactions_for_user(artist_id)
    if artist is None:
        return json.dumps({"error": "Artist not found"}), 404
    DB.delete_user_by_id(artist_id)
    return json.dumps({"id":artist.get("id"),"name":artist.get("name"),"username":artist.get("username")}), 200
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
