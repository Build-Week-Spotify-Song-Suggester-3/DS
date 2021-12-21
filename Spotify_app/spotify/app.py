from flask import Flask, render_template
#from .models import DB

#Factory Creation
def create_app():
    #initialize flask app
    app = Flask(__name__)

    #Configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

     # Connect database to the app object
    #DB.init_app(app)

    #Make Home and root route
    @app.route('/')
    def root():
        
        return render_template('index.html')


    # Test another route
    @app.route('/other')
    def other():
        # removes everything from the DB
        #DB.drop_all()
        # creates a new DB with indicated tables
        #DB.create_all()
        
        
        return 'Other Route'
    return app
