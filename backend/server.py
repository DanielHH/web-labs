from flask import Flask, request, Response, jsonify, json
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
import database_helper as db_helper

app = Flask(__name__)
auth = HTTPTokenAuth(scheme=" ")
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

unauthorized = 401
bad_request = 400

@auth.verify_token
def verify_token(token):
    if db_helper.token_exists(token):
        return True
    return False


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
    if db_helper.get_user(user_info["email"]):
        return jsonify(success=False, message="User already exists"), bad_request
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
    token = request.args.get("token")
    if db_helper.remove_token(token):
        return jsonify(success=True, message="Successfully signed out.")
    else:
        return jsonify(success=False, message="You are not signed in."), unauthorized


@app.route("/changepassword", methods=["POST"])
@auth.login_required
def change_password():
    data = request.form
    print request.headers["Authorization"]
    user = db_helper.get_user_by_token(request.headers["Authorization"])
    if not user:
        return jsonify(success=False, message="You are not signed in."), unauthorized
    if not len(data["new_password"]) >= 8:
        return jsonify(success=False, message="new password must consist of at least 8 characters"), unauthorized
    if user.change_password(data["password"], data["new_password"]):
        return jsonify(success=True, message="Password changed.")
    else:
        return jsonify(success=False, message="Wrong password"), unauthorized


@app.route("/getuserbytoken", methods=["POST"])
def get_user_data_by_token():
    token = request.args.get("token")
    user = db_helper.get_user_by_token(token)
    if not user:
        return jsonify(success=False, message="You are not signed in."), unauthorized
    else:
        return jsonify(success=True, message="HERE YOU GO!", user=user.as_dict())


@app.route("/getuserbyemail", methods=["POST"])
def get_user_data_by_email():
    email = request.form["email"]
    token = request.args.get("token")
    if not db_helper.token_exists(token):
        return jsonify(success=False, message="You are not signed in."), unauthorized

    user = db_helper.get_user_by_email(email)
    if not user:
        return jsonify(success=False, message="User not found!"), bad_request
    else:
        return jsonify(success=True, message="HERE YOU GO!", user=user.as_dict())


@app.route("/getmessagesbytoken", methods=["POST"])
def get_user_messages_by_token():
    token = request.args.get("token")
    if not db_helper.token_exists(token):
        return jsonify(success=False, message="You are not signed in."), unauthorized
    user = db_helper.get_user_by_token(token)
    print user.received

    return "hej"

@app.route("/getmessagesbyemail", methods=["POST"])
def get_user_messages_by_email():
    return


@app.route("/postmessage", methods=["POST"])
def post_message():
    from_data = request.form
    token = request.args.get("token")
    return


if __name__ == "__main__":
    app.debug = True
    app.run()
    db_helper.db_reset(db)
