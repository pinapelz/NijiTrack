from datetime import datetime

import fileutil as fs
from sql.pg_handler import PostgresHandler
from webapi.holodex import HolodexAPI
from webapi.youtube import YouTubeAPI
from b2sdk.v2 import *
import graph
from decorators import *
import argparse
import os
import pytz
from dotenv import load_dotenv

load_dotenv()

DATA_SETTING = fs.load_json_file("sql_table_config.json")
CONFIG = fs.load_config("config.ini")

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

@log("Initializing Database")
def initialize_database(server: PostgresHandler):
    server.create_table(name = CONFIG["TABLES"]["live"], column = DATA_SETTING["LIVE_COLUMNS"])
    server.create_table(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["HISTORICAL_COLUMNS"])
    server.create_table(name = CONFIG["TABLES"]["daily"], column = DATA_SETTING["DAILY_COLUMNS"])


@log("Inserting Live Data into Database")
def record_subscriber_data(data: list, force_refresh: bool = False):
    def transform_sql_string(string: str) -> str:
        return string.encode("ascii", "ignore").decode().replace("'", "''")
    def record_diff_data(data_tuple: tuple, refresh_daily: bool):
        if not server.check_row_exists(CONFIG["TABLES"]["daily"], "channel_id", channel_id):
            # data_tuple = (channel_id, pfp, channel_name, sub_count, time.strftime('%Y-%m-%d %H:%M:%S'))
            server.insert_row(CONFIG["TABLES"]["daily"], DATA_SETTING["DAILY_HEADER"], (data_tuple[0], data_tuple[3]))
            server.insert_row(table_name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["HISTORICAL_HEADER"], data=data_tuple)
            return
        elif refresh_daily:
            server.update_row(CONFIG["TABLES"]["daily"], "channel_id", channel_id, "sub_diff", sub_count)
            server.insert_row(table_name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["HISTORICAL_HEADER"], data=data_tuple)
    
    def check_diff_refresh():
        last_updated = server.get_most_recently_added_row_time(CONFIG["TABLES"]["historical"])[0]
        if not last_updated:
            print("Failed to get the most recently added row time.")
            return False
        last_updated = pytz.timezone('US/Pacific').localize(last_updated)
        utc_now = datetime.now(pytz.timezone('UTC'))
        pst_now = utc_now.astimezone(pytz.timezone('US/Pacific'))
        time_diff = pst_now - last_updated
        if time_diff.days >= 1:
            return True
        elif time_diff.days == 0 and time_diff.seconds >= 85800:
            return True
        else:
            print("Skipping Daily Refresh. It has not been a day yet")
            return False
    exclude_channels = fs.get_excluded_channels()
    if force_refresh:
        refresh_daily = True
    else:
        refresh_daily = check_diff_refresh()
    for channel in data:
        channel_id = channel["id"]
        if channel_id in exclude_channels:
            continue
        pfp = channel["photo"]
        sub_count = channel["subscriber_count"]
        channel_name = channel["english_name"]
        sub_org = channel["group"]
        video_count = channel["video_count"]
        if channel_name is None:
            channel_name = channel["name"]
        if sub_org is None:
            sub_org = "Unknown"
        channel_name = transform_sql_string(channel_name)
        utc_now = datetime.now(pytz.timezone('UTC'))
        pst_now = utc_now.astimezone(pytz.timezone('US/Pacific'))
        formatted_time = pst_now.strftime('%Y-%m-%d %H:%M:%S')
        data_tuple = (channel_id, pfp, channel_name, sub_count, sub_org, video_count, formatted_time)
        historical_data_tuple = (channel_id, pfp, channel_name, sub_count, formatted_time)
        server.insert_row(table_name = CONFIG["TABLES"]["live"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
        record_diff_data(historical_data_tuple, refresh_daily)


@log("Running Holodex Generation")
def holodex_generation(server: PostgresHandler, force_refresh: bool = False):
    """
    Generates the data from the Holodex API
    """
    holodex_organizations = DATA_SETTING["HOLODEX_ORGS"].split(",")
    server.clear_table(CONFIG["TABLES"]["live"])
    server.reset_auto_increment(CONFIG["TABLES"]["live"])
    holodex = HolodexAPI(os.environ.get("HOLODEX_KEY"), organization="Phase%20Connect")
    for organization in holodex_organizations:
        holodex.set_organization(organization)
        subscriber_data = holodex.get_subscriber_data()
        record_subscriber_data(subscriber_data, force_refresh)
    return holodex.get_generated_channel_data(), holodex.get_inactive_channels()

@log("Running YouTube Generation")
def youtube_generation(server: PostgresHandler):
    """
    Generates the data from the YouTube API
    """
    ytapi = YouTubeAPI(os.environ.get("YOUTUBE_API_KEY"))
    server.clear_table(CONFIG["TABLES"]["live"])
    server.reset_auto_increment(CONFIG["TABLES"]["live"])
    data = ytapi.get_data_all_channels(fs.get_local_channels())
    record_subscriber_data(data)
    return data

def combine_excluded_channel_ids(inactive_channel_data: list, excluded_channels: list):
    """
    Combines the local excluded channels with the inactive channels from the API
    """
    channel_ids = []
    for inactive_channel in inactive_channel_data:
        if inactive_channel in excluded_channels:
            continue
        channel_ids.append(inactive_channel)
    return channel_ids

def uploadFileToBucket(filepath: str) -> bool:
    try:
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        application_key_id = os.environ.get("B2_APP_ID")
        application_key = os.environ.get("B2_APP_KEY")
        file_info = {'how': 'good-file'}
        b2_api.authorize_account("production", application_key_id, application_key)
        b2_file_name = "graph.html"
        bucket = b2_api.get_bucket_by_name("vtuber-rabbit-hole-archive")
        bucket.upload_local_file(local_file=filepath, file_name=b2_file_name, file_info=file_info)
        return True
    except Exception as e:
        print("An error occured while attempting to upload to B2")
        print(e)
        return False;

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NijiTrack - A Subscriber Tracker")
    parser.add_argument('--mode', choices=['yt', 'holodex'], help='Specify the data source to use (yt or holodex)')
    parser.add_argument('--b2', action='store_true', help="Upload graph html to Backblaze B2")
    parser.add_argument('--ff', action='store_true', help="Force a full refresh of all data (override daily refresh)")
    args = parser.parse_args()
    server = create_database_connection()
    initialize_database(server)
    if args.mode == 'yt':
        print("Using YouTube API")
        channel_data = youtube_generation(server)
        inactive_channels = fs.get_excluded_channels()
    else:
        if args.ff:
            print("Forcing a full refresh")
            channel_data, inactive_channels = holodex_generation(server, force_refresh=True)
        else:
            channel_data, inactive_channels = holodex_generation(server)
    fs.update_excluded_channels(inactive_channels)
    graph_html = graph.plot_subscriber_count_over_time(server, CONFIG["TABLES"]["historical"], exclude_channels=combine_excluded_channel_ids(inactive_channels, fs.get_excluded_channels()))
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(graph_html)
    if args.b2:
        uploadFileToBucket("index.html")
    else:
        print("Skipping B2 Upload")