"""
Flask app for serving the static files
"""
from flask import Flask, send_file, send_from_directory, jsonify, abort
from flask_cors import CORS
from sql.sql_handler import SQLHandler
import fileutil as fs
import datetime

app = Flask(__name__)
CONFIG = fs.load_config("config.ini")
CORS(app)


@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/subscribers")
def api_subscribers():
    server = SQLHandler(CONFIG["SQL"]["host"], CONFIG["SQL"]["user"], CONFIG["SQL"]["password"], CONFIG["SQL"]["database"])
    data = server.execute_query("SELECT * FROM subscriber_data INNER JOIN 24h_historical ON subscriber_data.channel_id = 24h_historical.channel_id ORDER BY subscriber_count DESC")
    channel_data_list = [{"channel_name":row[3], "profile_pic": row[2], "subscribers": row[4], "sub_org": row[5], "video_count": row[6], "day_diff": int(row[10] - int(row[4]))} for row in data]
    subscriber_data = {"timestamp": datetime.datetime.now(),"channel_data":channel_data_list}
    
    return jsonify(subscriber_data)
    


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


if __name__ == "__main__":
    app.run(debug=True)
