from flask import Flask, request, Response, jsonify, json, g
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket import WebSocketError
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
import database_helper as db_helper
import hmac
import hashlib
import binascii
import base64

app = Flask(__name__)
cors = CORS(app)
auth = HTTPTokenAuth(scheme="Bearer")
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'Tjelvararlitetokig utropstecken'

app.debug = True
# SPARA WS MED USER TOKEN {token object: ws}
active_web_sockets = {}

@auth.verify_token
def verify_token(email):
    if not email or email == 'null':
        return False
    user = db_helper.get_user_by_email(email)
    if not user:
        return False

    hash = None
    client_hash = request.headers.get('Hash')
    for token in db_helper.get_user_tokens(user):
        if not request.data:
            hash = hmac.new(token.token, "null", hashlib.sha256).digest()
        else:
            hash = hmac.new(token.token, request.data, hashlib.sha256).digest()
        hash = base64.b64encode(hash)
        if client_hash == hash:
            g.token = token.token
            return True


@auth.error_handler
def auth_error():
    return jsonify(success=False, message="You are not signed in.")


@app.route('/openwebsocketconnection')
def open_web_socket_connection():
    if request.environ.get('wsgi.websocket'):
        current_ws = request.environ['wsgi.websocket']
        data = current_ws.receive()
        load_data = json.loads(data)

        current_token = db_helper.token_exists(load_data["token"])
        if current_token:
            for token, ws in active_web_sockets.iteritems(): # TODO: Byt ut for loop
                if token.user_id == current_token.user_id:
                    try:
                        ws.send(json.dumps({"action":"LOG_OUT"}))
                    except WebSocketError as e:
                        print repr(e)
                    #break
            active_web_sockets[current_token] = current_ws
        else:
            current_ws.close()

        while True:
            try:
                msg = current_ws.receive()
                current_ws.send(msg)
            except WebSocketError as e:
                print repr(e)
                break
    return ''


@app.route('/checklogin', methods=["POST"])
@auth.login_required
def check_login():
    return jsonify(success=True, message="You are signed in!")


@app.route('/',methods=["GET"])
def hello_world():
    return 'Hello, World!'


@app.route("/signup", methods=["POST"])
def sign_up():
    user_info = json.loads(request.data)

    if db_helper.get_user(user_info["email"]):
        response = jsonify(success=False, message="User already exists")
        return response
    if (user_info["email"] and len(user_info["password"]) >= 8 and
    user_info["firstname"] and user_info["lastname"] and user_info["gender"] and
    user_info["city"] and user_info["country"]):
        user = db_helper.add_user(user_info)
        return jsonify(success=True, message="Successfully created a new user.")
    else:
        return jsonify(success=False, message="Form data missing or incorrect type.")


@app.route("/signin", methods=["POST"])
def sign_in():
    user_info = json.loads(request.data)
    user = db_helper.get_user(user_info["email"])

    failed_response = jsonify(success=False, message="Wrong email or password")
    if user is None:
        return failed_response
    elif user.check_password(user_info["password"]):
        return jsonify(success=True, message="Successfully signed in.",
            data=user.generate_auth_token())
    else:
        return failed_response


@app.route("/signout", methods=["POST"])
@auth.login_required
def sign_out():
    token = db_helper.remove_token(g.token)
    if token:
        ws = active_web_sockets[token]
        ws.close()
        del active_web_sockets[token]
        return jsonify(success=True, message="Successfully signed out.")


@app.route("/changepassword", methods=["POST"])
@auth.login_required
def change_password():
    data = json.loads(request.data)
    user = db_helper.get_user_by_token(g.token)
    if not len(data["new_password"]) >= 8:
        return jsonify(success=False, message="new password must consist of at least 8 characters")
    if user.change_password(data["password"], data["new_password"]):
        return jsonify(success=True, message="Password changed.")
    else:
        return jsonify(success=False, message="Wrong password")


@app.route("/postmessage", methods=["POST"])
@auth.login_required
def post_message():
    request_data = json.loads(request.data);
    message = request_data["message"]
    to_email = request_data["to_email"]
    to_user = db_helper.get_user_by_email(to_email)
    if not to_user:
        return jsonify(success=False, message="User not found!")
    from_user = db_helper.get_user_by_token(g.token)
    db_helper.create_post(message, from_user, to_user)
    return jsonify(success=True, message="Message posted")


@app.route("/getmessagesbytoken", methods=["GET"])
@auth.login_required
def get_user_messages_by_token():
    user = db_helper.get_user_by_token(g.token)
    messages = []
    for post in user.received:
        messages.append(post.message)
    return jsonify(success=True, message="User messages retrieved.", messages=messages)


@app.route("/getmessagesbyemail", methods=["GET"])
@auth.login_required
def get_user_messages_by_email():
    email = request.args.get("email")
    user = db_helper.get_user_by_email(email)
    messages = []
    """
    if not user:
        return jsonify(success=False, message="There is no such user.")
        """
    for post in user.received:
        messages.append(post.message)
    return jsonify(success=True, message="User messages retrieved.", messages=messages)


@app.route("/getuserbytoken", methods=["GET"])
@auth.login_required
def get_user_data_by_token():
    user = db_helper.get_user_by_token(g.token)
    user=user.as_dict()
    del user["id"]
    return jsonify(success=True, message="User data retrieved.", user=user)


@app.route("/getuserbyemail", methods=["GET"])
@auth.login_required
def get_user_data_by_email():
    email = request.args.get("email")
    user = db_helper.get_user_by_email(email)
    if not user:
        return jsonify(success=False, message="User not found!")
    else:
        user=user.as_dict()
        del user["id"]
        return jsonify(success=True, message="User data retrieved.", user=user)


def run_server():
    if app.debug:
        application = DebuggedApplication(app)
    else:
        application = app
    server = WSGIServer(('', 5000), application,
                               handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == "__main__":
    db_helper.db_reset()
    run_with_reloader(run_server)
