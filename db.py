from main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    TMDB_id = db.Column(db.Integer, nullable=True)
    # viewed_movies = relationship("ViewedMovie", back_populates="user")
    # viewed_tv = relationship("ViewedTV", back_populates="user")
#

# viewed_movies = db.Table('viewed_movies',
#     db.Column('viewed_movies_id', db.Integer, primary_key=True),
#     db.column('movie_id', db.Integer, db.ForeignKey('') unique=True, nullable=False),
#     user_id = relationship("User", back_populates="viewed_movies")
# )
# #
# # class ViewedTV(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tv_id = db.column(db.Integer, unique=True, nullable=False)
#     user_id = relationship("User", back_populates="viewed_tv")

db.create_all()