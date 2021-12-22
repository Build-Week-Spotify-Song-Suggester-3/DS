import pandas as pd
import spotipy
from flask import Flask, render_template, request
from .Spotify import get_all_data
from os import getenv


# Create a 'factory' for serving up the app when is launched
def create_app():
    # initializes our app
    app = Flask(__name__)

    # Database configurations
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Turn off verification when we request changes to db
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')

    # Give our APP access to our database
    DB.init_app(app)

    # Listen to a "route"
    # Make our "Home" "root" route. '/' is the home page route
    @app.route('/')
    def root():
        
        return render_template('index.html', title = 'Home')

    # @app.route('/search', methods=['POST'])
    # @app.route('/search/<user_input>', methods=['GET'])
    # def search(user_input=None):
    #     '''Resets DB, Search user-song, gather 30 related tracks and
    #     pull all the information we need for the model'''
    #     # remove everything from database
    #     DB.drop_all()

    #     # Create the database file initially
    #     DB.create_all()

    #     # Insert gatheres data into DB.
    #     songs_data = get_all_data(user_input)
    #     DB.session.add(songs_data)
    #     DB.session.commit()
    #     return render_template('index.html',title="Related songs search is complete")

    
    # @app.route('/suggestions', methods=['POST'])
    # def suggestions():
    #     #user0, user1 = sorted([request.values['user0'], request.values['user1']])

    #     # if user0 == user1:
    #     #     message = 'Cannot compare a user to themselves!'
    #     # else:
    #     #     tweet_text = request.values['tweet_text']
    #     #     prediction = predict_user(user0, user1, tweet_text)
    #     #     if prediction == 0:
    #     #         predicted_user = user0
    #     #         non_predicted_user = user1
    #     #     else:
    #     #         predicted_user = user1
    #     #         non_predicted_user = user0

    #     #     message = f'"{tweet_text}" is more likely to be said by {predicted_user} than {non_predicted_user}'

    #     return render_template('index.html',title="5 Suggestions")




    return app