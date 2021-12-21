from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Day(DB.Model):
    id = DB.Column(DB.String(50), primary_key=True, unique=True, nullable=False)
    artist_name = DB.Column(DB.String(50), nullable=False)
    album = DB.Column(DB.String(50), nullable=False)
    duration = DB.Column(DB.BigInteger, nullable=False)
    popularity = DB.Column(DB.BigInteger, nullable=False)
    uri = DB.Column(DB.String(50), unique=True, nullable=False)
    lyrics = DB.Column(DB.String(500), nullable=False)
