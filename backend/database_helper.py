from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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

    def generate_auth_token(self, expiration=604800):

        """
        Generates authentication token if check_password returns true.
        Makes the generated token json-serializable by decoding it with ascii.
        Commits it to the database and returns generated token in a json object

        :param expiration:
        :return: JsonObject
        """

        s = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        token = s.dumps({"id": self.id})
        token = Token(token.decode("ascii"), self.id)
        db.session.add(token)
        db.session.commit()
        token = s.dumps({"id": self.id})
        token = token.decode("ascii")
        return token

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.String)
    from_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=false)
    to_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=false)


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
