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
    user = db_helper.get_user(user_info["email"])
    failed_response = jsonify(success=False, status_code="401",
        message="Email or password is not matching")
    if user is None:
        return failed_response
    elif user.check_password(user_info["password"]):
        #Perhaps check if user is already logged in (i.e. token already exists)
        return jsonify("success"=True, "message"="Successfully signed in.",
            "data"=user.generate_auth_token())
    else:
        return failed_response


@app.route("/signup", methods=["POST"])
def signUp():
    user = request.get_json()
    if not db_helper.get_user(user["email"]):
        if (user["email"] and len(user["password"]) >= 8 and
        user["firstname"] and user["familyname"] and user["gender"] and
        user["city"] and user["country"]):
            add_user(user)
    else:
        return jsonify("success"=false, "message"="Form data missing or incorrect type.")
    user_id = len(User.query.all()) # What's the point of this line?
    return jsonify("success"=true, "message"="Successfully created a new user.")



if __name__ == "__main__":
    app.debug = True
    db_helper.db_reset()
    app.run()
