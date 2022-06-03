from flask import Flask, render_template, redirect, url_for, request, flash
from viewed import Viewed
from TMDB_access import TMDB
# from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship




# Basic use sequence:
# Input a movie or series name.
# Display a list of actor images.
# User chooses an actor.
# show a list of movies and shows, divided into those known by the user and those not.
# allow user to add movies to their list of known movies.

# possible additions:
# images of the actor, where available, in each work.
# more attractive, more usable front end
# user sign in.
# maintain lists of viewed works and prioritize results from those lists.
# I haven't added any "i've seen this" functionality at all, which was part of my original vision for this project.
# As good a choice as any. API interface -> basic web functionality -> refine API interface is a good start.
# fix secret key to identify session
# refactor api request functions into a class
# pull out formatting for api data

# use TMDB user sessions to facilitate user login and access the user's rated works.
# link to somewhere the user can rate a work?

# TODO: chart out user authentication process
# TODO: identify required changes and resources
# TODO: update css
# TODO: Add user database?
# TODO: add in-app viewed film database?
# TODO: code user authentication process

class UserSession:
    def __init__(self):
        self.token = None
        self.TMDB_signin = False
        self.TMDB_guest_signin = False
        self.session_id = None

    def TMDB_signin(self):
        request_body = {'request_token': self.token}
        session = TMDB.send_api_request('/authentication/session/new', json=request_body)
        if session:
            self.session_id = session['session_id']
            return self.session_id

    def TMDB_guest_signin(self):
        session = TMDB.send_api_request('/authentication/guest_session/new')
        if session:
            self.session_id = session['session_id']
            return self.session_id

    def TMDB_signout(self):
        request_body = {'session_id': self.session_id}
        session_end = TMDB.send_api_request('/authentication/guest_session/new', json=request_body)
        return session_end

    # def save_to_db(self):
    def get_token(self):
        self.token = TMDB.send_api_request('/authentication/token/new')['request_token']
        return self.token



#---------------- Site Functionality -----------------

# Flask App
app = Flask(__name__)
# the following secret key is a placeholder to bypass an error.
# Replace with a real secret key.
app.secret_key = '1818181818181818'

works = TMDB()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    TMDB_id = db.column(db.Integer, unique=True)
    viewed_movies = relationship("ViewedMovie", back_populates="user")
    viewed_tv = relationship("ViewedTV", back_populates="user")

class ViewedMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.column(db.Integer, unique=True, nullable=False)
    user = relationship("User", back_populates="viewed_movies")


class ViewedTV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tv_id = db.column(db.Integer, unique=True, nullable=False)
    user = relationship("User", back_populates="viewed_tv")



@app.route('/')
def index():
    return render_template("index.html", work_name=None)

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/work_input', methods=["GET", "POST"])
def work_input():
    work_name = request.form["work"]
    works_found = works.list_works_by_name(work_name)
    print(works_found)
    if works_found:
        return render_template("movie.html", works=works_found, work_name=None)
    else:
        flash(f'No results for {work_name}.')
        return redirect(url_for('index'))

@app.route('/cast_list/<medium>/<work_id>', methods=["GET", "POST"])
def cast_list(medium, work_id):

    return render_template("cast.html", cast=works.list_actors_with_images(medium, work_id))

@app.route('/other_works/<person_id>', methods=["GET", "POST"])
def other_works(person_id):
    return render_template("other_works.html", works=works.list_actors_other_works(person_id), person_id=person_id)

@app.route('/viewed/<medium>/<work_id>/<person_id>')
def viewed(medium, work_id, person_id):
    works.viewed.add_new(medium, work_id)
    print(f'add {work_id} to viewed works')
    return redirect(url_for('other_works', person_id=person_id))


if __name__ == '__main__':
    app.run(debug=True)
