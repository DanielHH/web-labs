from server import db
from models import User, Token, Post

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
        db.session.delete(token)
        db.session.commit()
    return token
"""        return True
    else:
        return False
"""

def get_user_by_token(token):
    token = Token.query.filter_by(token=token).first()
    return token.user #Q: is this an extra query????


def token_exists(token):
    return Token.query.filter_by(token=token).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def check_if_user_has_token(user):
    return Token.query.filter_by(user_id = user.id).first()

def get_user_tokens(user):
    return Token.query.filter_by(user_id = user.id).all()


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
