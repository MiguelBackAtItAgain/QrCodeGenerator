from flask import Flask, request, send_file, Response, jsonify
from create import create_qr_code
from functools import wraps
from io import BytesIO
from dotenv import load_dotenv
import base64
import os

load_dotenv()

app = Flask(__name__)

USERNAME = os.getenv('FLASK_USERNAME')
PASSWORD = os.getenv('PASSWORD')

def check_auth(username, password):
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

@app.route("/create_qr", methods=['GET', 'POST'])
@requires_auth
def create_qr():
    
    data = request.get_json()

    filtered_data = {f'"{key}"': f'"{value}"' for key, value in data.items() if key not in ['color', 'base64']}

    color = data.get('color')

    base64 = data.get('base64')

    img = create_qr_code(filtered_data, color)

    if base64:
        return send_base64_image(img)
    
    return send_image(img)


def send_image(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

def send_base64_image(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return jsonify({"image": img_base64})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=3000)
    