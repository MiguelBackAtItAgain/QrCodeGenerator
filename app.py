from flask import Flask, request, send_file, jsonify, Response
from create import create_qr_code
from functools import wraps
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

USERNAME = os.getenv('FLASK_USERNAME')
PASSWORD = os.getenv('PASSWORD')

def check_auth(username, password):
    print(f"Received username: {username}, password: {password}")
    print(f"Expected username: {USERNAME}, password: {PASSWORD}")
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Incorrect login credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def validate_info(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return validate_info

@app.route("/")
def main():
    return "Hello!"

@app.route("/create_qr", methods=['GET'])
@requires_auth
def create_qr():
    data = request.args.get('data')
    color = request.args.get('color')
    img = create_qr_code(data, color)
    return send_image(img)

def send_image(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
    