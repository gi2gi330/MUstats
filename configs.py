from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mustats'
UPLOAD_FOLDER = 'static'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)


SPOTIFY_CLIENT_ID = "21a4b4fdde0c48aea3c5ecaa780d05c0"
SPOTIFY_CLIENT_SECRET = "94890ce606cc47a6b3eaa9d623b2830f"
