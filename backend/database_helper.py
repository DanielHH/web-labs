from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from server import app, db

app.config["SECRET_KEY"] = 'Tjelvararlitetokig utropstecken'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    #gender = db.Column(db.Enum('MALE', 'FEMALE', 'OTHER'), default='MALE', nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)

    token = db.relationship("Token", backref="user", lazy="dynamic")


    def __init__(self, email, password, first_name, last_name, gender, city, country):
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.city = city
        self.country = country


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
        save_to_db(token)
        token = s.dumps({"id": self.id})
        token = token.decode("ascii")
        return token


    def check_password(self, password):
        return check_password_hash(self.password, password)


    def change_password(self, password, new_password):
        if self.check_password(password):
            self.password = generate_password_hash(new_password)
            db.session.commit()
            return True
        else:
            return False


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password" }


    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    from_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    sender = db.relationship("User", foreign_keys=[from_user], backref='sent')
    receiver = db.relationship("User", foreign_keys=[to_user], backref='received')


    def __init__(self, message, from_user, to_user):
        self.message = message
        self.from_user = from_user
        self.to_user = to_user


    def __repr__(self):
        return "<message %r>" % self.message


class Token(db.Model):
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


def get_user(email):
    return User.query.filter_by(email=email).first()


def add_user(user):
    user = User(user["email"], user["password"], user["firstname"],
     user["lastname"], user["gender"], user["city"], user["country"])
    save_to_db(user)
    return user


def remove_token(token):
    token = Token.query.filter_by(token=token).first()
    if token:
        save_to_db(token)
        return True
    else:
        return False


def get_user_by_token(token):
    token = Token.query.filter_by(token=token).first()
    return token.user #Q: is this an extra query????


def token_exists(token):
    return Token.query.filter_by(token=token).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def check_if_user_has_token(user):
    return Token.query.filter_by(user_id = user.id).first()


def create_post(message, from_user, to_user):
    post = Post(message, from_user.id, to_user.id)
    save_to_db(post)
    return post


def save_to_db(entry):
    db.session.add(entry)
    db.session.commit()


def db_reset():
    db.drop_all()
    db.create_all()
