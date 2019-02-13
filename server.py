from flask import Flask, request, Response, jsonify, json, g
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import database_helper as db_helper

app = Flask(__name__)
cors = CORS(app)
auth = HTTPTokenAuth(scheme="Bearer")
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'Tjelvararlitetokig utropstecken'

unauthorized = 401
bad_request = 400


@auth.verify_token
def verify_token(token):
    if db_helper.token_exists(token):
        g.token = token
        return True
    return False


@auth.error_handler
def auth_error():
    return jsonify(success=False, message="You are not signed in.")


@app.route('/',methods=["GET"])
def hello_world():
    return 'Hello, World!'


@app.route("/signin", methods=["POST"])
def sign_in():
    user_info = json.loads(request.data)
    user = db_helper.get_user(user_info["email"])
    if db_helper.check_if_user_has_token(user):
        return jsonify(success=False, message="User is already signed in"), bad_request
    failed_response = jsonify(success=False, status_code="401",
        message="Email or password is not matching")
    if user is None:
        return failed_response, unauthorized
    elif user.check_password(user_info["password"]):
        return jsonify(success=True, message="Successfully signed in.",
            data=user.generate_auth_token())
    else:
        return failed_response, unauthorized


@app.route("/signup", methods=["POST"])
def sign_up():
    user_info = json.loads(request.data)

    if db_helper.get_user(user_info["email"]):
        response = jsonify(success=False, message="User already exists")
        response.status_code = bad_request
        return response
    if (user_info["email"] and len(user_info["password"]) >= 8 and
    user_info["firstname"] and user_info["lastname"] and user_info["gender"] and
    user_info["city"] and user_info["country"]):
        user = db_helper.add_user(user_info)
        return jsonify(success=True, message="Successfully created a new user.", data=user.generate_auth_token())
    else:
        return jsonify(success=False, message="Form data missing or incorrect type."), bad_request


@app.route("/signout", methods=["POST"])
@auth.login_required
def sign_out():
    if db_helper.remove_token(g.token):
        return jsonify(success=True, message="Successfully signed out.")


@app.route("/changepassword", methods=["POST"])
@auth.login_required
def change_password():
    data = request.form
    user = db_helper.get_user_by_token(g.token)
    if not len(data["new_password"]) >= 8:
        return jsonify(success=False, message="new password must consist of at least 8 characters"), unauthorized
    if user.change_password(data["password"], data["new_password"]):
        return jsonify(success=True, message="Password changed.")
    else:
        return jsonify(success=False, message="Wrong password"), unauthorized


@app.route("/getuserbytoken", methods=["POST"])
@auth.login_required
def get_user_data_by_token():
    user = db_helper.get_user_by_token(g.token)
    return jsonify(success=True, message="User data retrieved.", user=user.as_dict())


@app.route("/getuserbyemail", methods=["POST"])
@auth.login_required
def get_user_data_by_email():
    data = json.loads(request.data)
    email = data["email"]
    user = db_helper.get_user_by_email(email)
    if not user:
        return jsonify(success=False, message="User not found!"), bad_request
    else:
        return jsonify(success=True, message="User data retrieved.", user=user.as_dict())


@app.route("/getmessagesbytoken", methods=["POST"])
@auth.login_required
def get_user_messages_by_token():
    user = db_helper.get_user_by_token(g.token)
    messages = []
    for post in user.received:
        messages.append(post.message)
    return jsonify(success=True, message="User messages retrieved.", messages=messages)


@app.route("/getmessagesbyemail", methods=["POST"])
@auth.login_required
def get_user_messages_by_email():
    email = request.form["email"]
    user = db_helper.get_user_by_email(email)
    messages = []
    for post in user.received:
        messages.append(post.message)
    return jsonify(success=True, message="User messages retrieved.", messages=messages)


@app.route("/postmessage", methods=["POST"])
@auth.login_required
def post_message():
    message = request.form["message"]
    to_email = request.args.get("to_email")
    to_user = db_helper.get_user_by_email(to_email)
    if not to_user:
        return jsonify(success=False, message="User not found!"), bad_request
    from_user = db_helper.get_user_by_token(g.token)
    db_helper.create_post(message, from_user, to_user)
    return jsonify(success=True, message="Message posted")


if __name__ == "__main__":
    app.debug = True
    app.run()
    db_helper.db_reset()
