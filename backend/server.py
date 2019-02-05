from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import database_helper as db_helper
import os.path

app = Flask(__name__)

"""db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path) """

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

if __name__ == "__main__":
    app.debug = True
    db_helper.db_reset()
    app.run()
