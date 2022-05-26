from flask import Flask, render_template, redirect, url_for, request, flash
from viewed import Viewed
from TMDB_access import TMDB

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


# add "I've seen this" functionality for a single user
# use a simple data structure, list or dict
# embed access in functions or class methods




#---------------- Site Functionality -----------------

# Flask App
app = Flask(__name__)
# the following secret key is a placeholder to bypass an error.
# Replace with a real secret key.
app.secret_key = '1818181818181818'

works = TMDB()


@app.route('/')
def index():
    return render_template("index.html", work_name=None)

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
