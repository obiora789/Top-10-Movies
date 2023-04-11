from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired
import requests
from sqlalchemy import asc
import os
import dotenv

new_file = dotenv.find_dotenv()
dotenv.load_dotenv(new_file)

number_of_movies = 0
api_key = os.getenv("API_KEY")
movie_response = {}
movie_list = []
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-ten-movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class AddMovieForm(FlaskForm):
    """Creates and handles the form where you can input the title of your desired movie."""
    movie_add = StringField(label="Movie Title", validators=[InputRequired()])
    submit = SubmitField(label="Add Movie")


class RateMovieForm(FlaskForm):
    """Creates and handles the form where you can input your rating snd review for a particular movie"""
    rating = FloatField(label="Your personal rating out of 10 (e.g., 7.5)", validators=[InputRequired()])
    review = StringField(label="Your personal review", validators=[InputRequired()])
    submit = SubmitField(label="Done")


class Movie(db.Model):
    """This is the model/blueprint through which the database builds the table and the records."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        """This line is a representation of each object(instance) when created in the database."""
        return '<Movie %r>' % self.title


with app.app_context():
    db.create_all()


    @app.route("/")
    def home():
        """Loads all the movies in the database"""
        global number_of_movies, movie_list
        number_of_movies = Movie.query.count()   # simply returns the number of records(movies) in the database
        if number_of_movies > 0:
            # faster form of count 👇🏾
            # db.session.execute(Table.query.filter_by(condition).statement.with_only_columns([func.count()]).order_by(None)).scalar()
            print(f"From home: {number_of_movies}")
            # to sort the database by Movie rating in ascending order
            movie_list = db.session.query(Movie).order_by(asc(Movie.rating)).all()
            current_rank = 0
            # The for loop determines the rank assigned to each record after it is sorted
            for i in range(number_of_movies, 0, -1):
                current_rank += 1
                movie_list[i-1].ranking = current_rank   # the rank displayed in descending order on the homepage.
                # gets the movie object to be updated using the title
                movie_update = Movie.query.filter_by(title=movie_list[i-1].title)
                movie_update.ranking = current_rank   # rank is assigned to the movie/record in the database
                db.session.commit()   # saves the changes in the database
            return render_template("index.html", movies=movie_list, sum_movies=number_of_movies)
        else:
            return render_template("index.html", sum_movies=number_of_movies)

    @app.route("/add", methods=["GET", "POST"])
    def add_movie():
        global movie_response
        # Creates the form to input your desired movie
        new_movie = AddMovieForm()
        # when the user clicks the submit button
        if new_movie.validate_on_submit():
            movie_title = new_movie.movie_add.data.lower()   # gets the movie title
            # uses the movie title to search the movie database API. The results are stored in movie_response
            movie_response = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&s={movie_title}").json()['Search']
            return redirect("/select")   # moves to the select route/function
        return render_template("add.html", add=new_movie)

    @app.route("/edit/<movie_title>/<render_position>", methods=["GET", "POST"])
    def edit(movie_title, render_position):   # movie title and render position are passed as arguments
        print(f"Render Position: {render_position}, Movie Title: {movie_title}")
        global number_of_movies   # gets the current number of movies and updates it when necessary
        rate_movie = RateMovieForm()   # creates the form to rate your desired movie
        number_of_movies = Movie.query.count()
        if rate_movie.validate_on_submit():   # is activated when the user clicks the submit button
            if int(render_position) < number_of_movies:   # if the value received is the render position of the movie.
                rank = number_of_movies - int(render_position) + 1   # equation to get the rank in the database.
                update_movie = Movie.query.filter_by(ranking=rank).first()   # query the database using the rank
                print(f"First trial: {update_movie}")
            else:    # if the value received is the id instead, then the database is queried with the movie id.
                update_movie = Movie.query.get(render_position)
                print(f"Second trial: {update_movie}")
            # Then compare the title of update movie with the argument passed into the function
            if update_movie.title.lower() == movie_title.lower():   # if the same, update info is saved in the database
                print("True")
                update_movie.rating = rate_movie.rating.data   # rating information provided by user
                update_movie.review = rate_movie.review.data   # review information provided by user
                db.session.commit()   # the changes are saved
            else:
                print("False")
            return redirect("/")   # return to homepage to see the updated movie list
        return render_template("edit.html", num=int(render_position), title=movie_title, sum_movies=number_of_movies, edit_movie=rate_movie)

    @app.route("/delete/<movie_title>/<render_position>")
    def delete(movie_title, render_position):   # movie title and render position are passed as arguments
        rank = number_of_movies - int(render_position) + 1   # equation to get the movie rank in the database.
        movie_to_delete = Movie.query.filter_by(ranking=rank).first()   # query the database using the rank derived
        print(movie_to_delete.title.lower(), movie_title)
        if movie_to_delete.title.lower() == movie_title.lower():   # if the same, the movie is deleted from the database
            print(f"First try: {movie_to_delete}")
            db.session.delete(movie_to_delete)   # the movie is deleted from the database
            db.session.commit()   # the changes are saved
        return redirect("/")   # return to homepage to see the updated movie list

    @app.route("/select")
    def select_movie():
        """This displays the list of initial search results(possible movies) obtained from the API and activates the
        selected_movie function when a selection is made."""
        print(f"From select: {movie_response}")
        return render_template("select.html", movies=movie_response)

    @app.route("/selected/<select_id>")
    def selected_movie(select_id):
        """This method/route uses the select_id to perform a more detailed search of the selected
        movie and renders its result on the screen"""
        actual_movie = requests.get(f"http://www.omdbapi.com/?apikey={api_key}&i={select_id}").json()
        print(actual_movie)
        # Uses the database model to populate the fields for each record in the database.
        movie_to_add = Movie(
            title=actual_movie['Title'],  # movie title
            year=actual_movie['Year'],   # year movie was produced
            description=actual_movie['Plot'],   # movie description
            rating=actual_movie['imdbRating'],   # imdb rating of movie
            ranking=None,    # Ranking and review are none for now
            review=None,
            img_url=actual_movie['Poster']   # image of the movie
        )
        db.session.add(movie_to_add)   # Add each instance to the database as a record
        db.session.commit()    # Save the record
        # The database_ID of each movie is sent to the edit route so the ranking and review can be updated by the user.
        print(f"Movie ID: {movie_to_add.id}")
        return redirect(f"/edit/{movie_to_add.title}/{movie_to_add.id}")   # movie title & id passed to the edit route


if __name__ == '__main__':
    app.run(debug=True)
