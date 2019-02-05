from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import database_helper as db_helper
import os.path

app = Flask(__name__)

"""db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path) """

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

@app.route("/signin", methods=["POST"])
def sign_in():
    user_info = request.get_json()
    try_users = User.query.filter_by(email=user_info["email"]).first()
    failed_response = jsonify(success=False, status_code="401", message="User or password is not matching")
    if try_users is None:
        return failed_response
    elif try_users.check_password(user_info["password"]):
        return jsonify("success"=True, "message"="Successfully signed in.", "data"=try_users.generate_auth_token())
    else:
        return failed_response

@app.route("/signup", methods=["POST"])
def signUp():
    user = request.get_json()
    if not User.query.filter_by(email=user["email"]).first():
        # TODO: CHECK NONEMPTY FIELDS AND PASSWORD >= 8.
        user = User(user["email"], user["password"], user["firstname"],
         user["familyname"], user["gender"], user["city"], user["country"])
        db.session.add(user)
        db.session.commit()
    else:
        return jsonify("success"=false, "message"="Form data missing or incorrect type.")
    user_id = len(User.query.all())
    return jsonify("success"=true, "message"="Successfully created a new user.")


if __name__ == "__main__":
    app.debug = True
    db_helper.db_reset()
    app.run()
