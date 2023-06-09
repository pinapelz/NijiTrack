"""
Flask app for serving the static files
"""
from flask import Flask, send_file, send_from_directory, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def main_page():
    return send_from_directory('stats','index.html')

@app.route('/stats/<path:path>')
def send_static(path):
    return send_from_directory('stats', path+".html")

@app.route('/tables/<path:path>')
def send_niji_table(path):
    return send_from_directory('tables', path+".html")

@app.route('/pettantrack')
def send_pettan():
    return send_file('/home/pinapelz/PettanTrack/index.html')

@app.route('/pettantracker/stats/<path:path>')
def send_pettan_stats(path):
    return send_from_directory('/home/pinapelz/PettanTrack/stats', path+".html")

@app.route('/pettantracker/tables/<path:path>')
def send_table_pettan(path):
    return send_from_directory('/home/pinapelz/PettanTrack/tables', path+".html")

@app.route('/sitemap.xml')
def send_sitemap():
    return send_file('assets/sitemap.xml')

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404

if __name__ == "__main__":
    app.run(debug=True)