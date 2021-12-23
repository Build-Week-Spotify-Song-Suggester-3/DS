from flask import Flask, render_template, request


def create_app():

    # initializes our Flask app
    app = Flask(__name__)

    @app.route('/')
    def root():
        # Do this when somebody hits the home page
        return render_template("index.html")

    @app.route('/', methods=["POST"])
    def get_song_data():
        text=request.form.get['textbox']
        return text

    @app.route('/result', methods=["POST", "GET"])
    def result():

        return get_song_data()

    return app