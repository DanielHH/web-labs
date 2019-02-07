from flask import Flask, request, Response, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import database_helper as db_helper
import os.path

app = Flask(__name__)

db = SQLAlchemy(app)

"""db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path) """

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

unauthorized = 401
bad_request = 400

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/signin", methods=["POST"])
def sign_in():
    user_info = request.form
    user = db_helper.get_user(user_info["email"])
    failed_response = jsonify(success=False, status_code="401",
        message="Email or password is not matching")
    if user is None:
        return failed_response, unauthorized
    elif user.check_password(user_info["password"]):
        #Perhaps check if user is already logged in (i.e. token already exists)
        return jsonify(success=True, message="Successfully signed in.",
            data=user.generate_auth_token())
    else:
        return failed_response, unauthorized


@app.route("/signup", methods=["POST"])
def sign_up():
    user_info = request.form
    if not db_helper.get_user(user_info["email"]):
        if (user_info["email"] and len(user_info["password"]) >= 8 and
        user_info["firstname"] and user_info["lastname"] and user_info["gender"] and
        user_info["city"] and user_info["country"]):
            user = db_helper.add_user(user_info)
            return jsonify(success=True, message="Successfully created a new user.", data=user.generate_auth_token())
        else:
            return jsonify(success=False, message="Form data missing or incorrect type."), bad_request
    else:
        return jsonify(success=False, message="User already exists"), bad_request



@app.route("/signout", methods=["POST"])
def sign_out():
    token = request.args.get("token")
    print token
    if db_helper.remove_token(token):
        return jsonify(success=True, message="Successfully signed out.")
    else:
        return jsonify(success=False, message="You are not signed in."), unauthorized


@app.route("/changepassword", methods=["POST"])
def change_password():
    return


@app.route("/getuser", methods=["GET"])
def get_user_data_by_email():
    return


@app.route("/getmessagesbytoken", methods=["GET"])
def get_user_messages_by_token():
    return


@app.route("/getmessagesbyemail", methods=["GET"])
def get_user_messages_by_email():
    return


@app.route("/postmessage", methods=["POST"])
def post_message():
    return



if __name__ == "__main__":
    app.debug = True
    app.run()
    db_helper.db_reset(db)
