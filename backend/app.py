"""
Flask app for serving the static files
"""
from flask import Flask, send_file, send_from_directory, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def main_page():
    return "We are offline at the moment"


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


if __name__ == "__main__":
    app.run(debug=True)
