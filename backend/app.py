"""
Flask app for serving the static files
"""
from flask import Flask, send_file, jsonify
from flask_cors import CORS
from sql.pg_handler import PostgresHandler
import fileutil as fs
import datetime
import pandas
from sklearn.linear_model import Ridge
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Optional setting to use any of the custom options below
START_DATE = "2023-04-01" # 2023 April 1st

# Do not include datapoints before the START_DATE for any /api/subscribers/ endpoint
# For when you only want to serve actual data you collected at those specific endpoints
ALL_EXCLUDE_MANUAL_DATA = False

# Do not include datapoints before the START_DATE for any /api/subscribers/<channel_id> endpoint
# For when you only want to serve actual data you collected at those specific endpoints
INDIVIDUAL_EXCLUDE_MANUAL_DATA = True

def create_database_connection():
    """
    Creates a database connection using the environment variables
    :param: auth_append: str = "" - If you want to use a different set of variables for persisitance of sessions
    """
    hostname = os.environ.get("POSTGRES_HOST")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    database = os.environ.get("POSTGRES_DATABASE")
    return PostgresHandler(host_name=hostname, username=user, password=password, database=database, port=5432)

@app.route("/")
def index():
    try:
        return send_file("index.html")
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/subscribers")
def api_subscribers():
    server = create_database_connection()
    query = 'SELECT sd.*, h.* FROM subscriber_data sd INNER JOIN "24h_historical" h ON sd.channel_id = h.channel_id ORDER BY sd.subscriber_count DESC'
    data = server.execute_query(query)
    channel_data_list = [{"channel_name": row[3], "profile_pic": row[2], "subscribers": row[4], "sub_org": row[5], "video_count": row[6], "day_diff": int(row[4] - int(row[10]))} for row in data]
    subscriber_data = {"timestamp": datetime.datetime.now(), "channel_data": channel_data_list}
    return jsonify(subscriber_data)

@app.route("/api/subscribers/<channel_name>")
def api_subscribers_channel(channel_name):
    server = create_database_connection()
    query = "SELECT * FROM subscriber_data_historical WHERE name = %s AND timestamp > %s ORDER BY TO_CHAR(timestamp, 'YYYY-MM-DD')"
    data = server.execute_query(query, (channel_name, START_DATE))
    labels = []
    data_points = []
    seen_dates = set()
    for row in data:
        date_string = row[5].strftime("%Y-%m-%d")
        if date_string in seen_dates:
            continue
        labels.append(date_string)
        data_points.append(row[4])
        seen_dates.add(date_string)
    return jsonify({"labels": labels, "datasets": data_points})

@app.route("/api/subscribers/<channel_name>/7d")
def api_subscribers_channel_7d(channel_name):
    server = create_database_connection()
    query = "SELECT * FROM subscriber_data_historical WHERE name = %s ORDER BY TO_CHAR(timestamp, 'YYYY-MM-DD')"
    data = server.execute_query(query, (channel_name,))
    labels = []
    data_points = []
    seen_dates = set()
    for row in data:
        date_string = row[5].strftime("%Y-%m-%d")
        if date_string in seen_dates:
            continue
        labels.append(date_string)
        data_points.append(row[4])
        seen_dates.add(date_string)
    return jsonify({"labels": labels[-7:], "datasets": data_points[-7:]})

@app.route("/api/channel/<channel_name>")
def get_channel_information(channel_name):
    def find_next_milestone(subscriber_count):
        if subscriber_count < 100000:
            return ((subscriber_count // 10000) + 1) * 10000
        elif subscriber_count < 1000000:
            return ((subscriber_count // 100000) + 1) * 100000
        else:
            return ((subscriber_count // 1000000) + 1) * 1000000
    server = create_database_connection()
    query = "SELECT * FROM subscriber_data WHERE name = %s"
    data = server.execute_query(query, (channel_name,))
    channel_data = {"channel_id": data[0][1], "channel_name": data[0][3], "profile_pic": data[0][2], "subscribers": data[0][4], "sub_org": data[0][5], "video_count": data[0][6]}
    historical_data = server.execute_query("SELECT * FROM subscriber_data_historical WHERE name = %s", (channel_name,))
    current_subscriber_count = data[0][4]
    subscriber_points = []
    date_strings = []
    seen_dates = set()
    for row in historical_data:
        date_string = row[5].strftime("%Y-%m-%d")
        if date_string in seen_dates:
            continue
        subscriber_points.append(row[4])
        date_strings.append(date_string)
        seen_dates.add(date_string)
    data = {"subscribers": subscriber_points, "dates": date_strings}
    df = pandas.DataFrame(data=data)
    df['dates'] = pandas.to_datetime(df['dates'])
    df.set_index('dates', inplace=True)
    df.sort_index(inplace=True)
    three_months_ago = datetime.datetime.now() - datetime.timedelta(days=90)
    df = df[df.index > three_months_ago]
    try:
        model = Ridge(alpha=100)
        X = np.array(range(len(df))).reshape(-1, 1)
        y = df['subscribers']
        model.fit(X, y)
        next_milestone = find_next_milestone(current_subscriber_count)
        days_until_next_milestone = (next_milestone - model.intercept_) / model.coef_
        days_until_next_milestone_scalar = int(days_until_next_milestone[0])
        next_milestone_date = (df.index[0] + pandas.Timedelta(days=days_until_next_milestone_scalar)).date()
        time_until_next_milestone = (next_milestone_date - datetime.datetime.now().date()).days
        if time_until_next_milestone < 0:
            raise OverflowError
        channel_data["next_milestone_date"] = str(next_milestone_date)
        channel_data["days_until_next_milestone"] = str(time_until_next_milestone)
        channel_data["next_milestone"] = str(next_milestone)
    except OverflowError:
        channel_data["next_milestone_date"] = "N/A"
        channel_data["days_until_next_milestone"] = "N/A"
        channel_data["next_milestone"] = "N/A"
    return jsonify(channel_data)
@app.route("/api/announcement")
def api_announcement():
    announcement_data = {"message": "None", "show_message": False}
    return jsonify(announcement_data)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404

if __name__ == "__main__":
    app.run(debug=True)
