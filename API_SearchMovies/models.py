# coding: utf-8
from sqlalchemy.dialects.mysql import YEAR

from API_SearchMovies import db

# Base = declarative_base()
# metadata = Base.metadata


class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200))
    release_year = db.Column(YEAR)
    ratings = db.Column(db.DECIMAL(2, 1))
    genre = db.Column(db.String(255))

    def __repr__(self):
        return str(self.title)
