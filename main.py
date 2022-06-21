from flask import Flask, render_template, redirect, url_for, request, flash
from TMDB_access import TMDB
import os
from dotenv import load_dotenv

load_dotenv()

# Basic use sequence:
# Input a movie or series name.
# Display a list of actor images.
# User chooses an actor.
# show a list of movies and shows, divided into those known by the user and those not.
# XXX-removed-XXX allow user to add movies to their list of known movies.

# possible additions:
# images of the actor, where available, in the role, to make them easier to recognize.
# more attractive, more usable front end
# XXX-removed-XXX maintain lists of viewed works and prioritize results from those lists.

# I took out my "I've seen this" functionality, which was part of my original vision for this project.
# It's in a previous commit if I want to put it back.

#---------------- Site Functionality -----------------

# Flask App
app = Flask(__name__)
# the following secret key is a placeholder to bypass an error.
# Replace with a real secret key.
app.secret_key = os.getenv('APP_SECRET_KEY')

works = TMDB()

@app.route('/')
def index():
    return render_template("index.html", work_name=None)


@app.route('/work_input', methods=["GET", "POST"])
def work_input():
    # rename this url: '/watching/<search term>'
    # use url encoding to make the search term work
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


if __name__ == '__main__':
    app.run(debug=True)
