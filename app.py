from flask import Flask, request, send_file
from create import create_qr_code
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello!"

@app.route("/create_qr", methods=['GET'])
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
    