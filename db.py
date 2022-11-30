from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    "association",
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("mood_id", db.Integer, db.ForeignKey("mood.id"))
)

class Artist(db.Model):
    """
    Has a one to many relationship with Albums
    """
    __tablename__="artist"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    albums = db.relationship("Album", cascade="delete")

    def __init__(self, **kwargs):
        """
        Creates an Artist Object
        """
        self.name = kwargs.get("name","")

    def serialize(self):
        """
        Serializes an Artist Object
        """
        return {
            "id": self.id,
            "name": self.name,
            "albums": [album.serialize() for album in self.albums]
        }

class Album(db.Model):
    """
    Has a One to Many relationship with Songs
    """
    __tablename__="album"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable = False)
    songs = db.relationship("Song", cascade="delete")

    def __init__(self,**kwargs):
        """
        Creates an Album object
        """
        self.name = kwargs.get("name","")
        self.artist_id = kwargs.get("artist_id")

    def serialize(self):
        """
        Serializes an Album Object
        """
        return {
            "id": self.id,
            "name": self.name,
            "songs": [song.serialize() for song in self.songs]
        }

class Song(db.Model):
    """
    Has a one to many relationship with comments
    Has a many to many relationship with moods
    """
    __tablename__="song"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    length = db.Column(db.Real, nullable = False)
    streams = db.Column(db.Integer, nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    comments = db.relationship("Comment", cascade="delete")
    moods = db.relationship("Mood", secondary=association_table,back_populates="songs")

    def __init__(self, **kwargs):
        """
        Creates a Song object
        """
        self.name = kwargs.get("name")
        self.length = kwargs.get("length")
        self.streams = kwargs.get("streams")
        self.album_id = kwargs.get("album_id")
    
    def serialize(self):
        """
        Serialize a song object
        """
        pass

    def simple_serialize(self):
        pass

class Comment(db.Model):
    pass

class Mood(db.Model):
    pass



class User(db.Model):
    """
    User model 
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)

