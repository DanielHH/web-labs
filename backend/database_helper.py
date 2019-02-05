from flask_sqlalchemy import SQLAlchemy
from server import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.Enum('MALE', 'FEMALE', 'OTHER'), default='MALE', nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)

    token = db.relationship("Token", backref="user", lazy="dynamic")
    received_posts = db.relationship("Post", backref="recipient", lazy="dynamic")
    sent_posts = db.relationship("Post", backref="author", lazy="dynamic")


    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=false)
    receiver = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=false)


    def __repr__(self):
        return "<text_content %r>" % self.text_content

class Token(db.Model):

    """Class representing Tokens generated when logging in"""

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_token(self):
        return self.token

    def __repr__(self):
        return "<token %r>" % self.token + "<Id: %r>" % self.id

def db_reset():
    """Clear the database."""
    db.drop_all()
    db.create_all()
