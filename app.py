from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('./assets/imgs/out/', filename)

@app.route('/metadata/<path:filename>')
def serve_metadata(filename):
    return send_from_directory('./assets/json/', filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
