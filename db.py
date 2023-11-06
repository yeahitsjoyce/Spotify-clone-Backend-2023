from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association Tables
mood_table = db.Table(
    "mood",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("mood_id", db.Integer, db.ForeignKey("mood.id"))
)

likes_table = db.Table(
    "all_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"))
)

# Artist Model
class Artist(db.Model):
    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    albums = db.relationship("Album", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "albums": [album.serialize() for album in self.albums]
        }

# Album Model
class Album(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    songs = db.relationship("Song", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.artist_id = kwargs.get("artist_id")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "songs": [song.simple_serialize() for song in self.songs]
        }

# Song Model
class Song(db.Model):
    __tablename__ = "song"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer, nullable=False)  # Changed to Integer
    streams = db.Column(db.Integer, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    comments = db.relationship("Comment", cascade="delete")
    moods = db.relationship("Mood", secondary=mood_table, back_populates="songs")
    liked = db.relationship("User", secondary=likes_table, back_populates="liked")  # Corrected to "liked"

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.length = kwargs.get("length")
        self.streams = kwargs.get("streams")
        self.album_id = kwargs.get("album_id")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "streams": self.streams,
            "album_id": self.album_id,
            "comments": [comment.serialize() for comment in self.comments],
            "moods": [mood.simple_serialize() for mood in self.moods]
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "length": self.length,
            "streams": self.streams
        }

# Comment Model
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_comment = db.Column(db.String, nullable=False)  # Changed to String
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"), nullable=False)

    def __init__(self, **kwargs):
        self.user_comment = kwargs.get("comment")
        self.user_id = kwargs.get("user_id")
        self.song_id = kwargs.get("song_id")

    def serialize(self):
        return {
            "id": self.id,
            "user_comment": self.user_comment,
            "user_id": self.user_id,
            "song_id": self.song_id
        }

# Mood Model
class Mood(db.Model):
    __tablename__ = "mood"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    songs = db.relationship("Song", secondary=mood_table, back_populates="moods")

    def __init__(self, **kwargs):
        self.description = kwargs.get("description", "")
        self.color = kwargs.get("color")

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "color": self.color,
            "songs": [song.serialize

