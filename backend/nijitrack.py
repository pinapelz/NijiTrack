import time

import fileutil as fs
from sql.sql_handler import SQLHandler
from webapi.holodex import HolodexAPI
from webapi.youtube import YouTubeAPI
import graph
from decorators import *
import argparse


CONFIG = fs.load_config("config.ini")
DATA_SETTING = fs.load_json_file("sql_table_config.json")


@log("Initializing Database")
def initialize_database(server: SQLHandler):
    server.create_table(name = CONFIG["TABLES"]["live"], column = DATA_SETTING["LIVE_COLUMNS"])
    server.create_table(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["LIVE_COLUMNS"])
    server.create_table(name = CONFIG["TABLES"]["daily"], column = DATA_SETTING["DAILY_COLUMNS"])


@log("Inserting Live Data into Database")
def record_subscriber_data(data: list):
    def transform_sql_string(string: str) -> str:
        return string.encode("ascii", "ignore").decode().replace("'", "''")
    def record_diff_data(data_tuple: tuple, refresh_daily: bool):
        if not server.check_row_exists(CONFIG["TABLES"]["daily"], "channel_id", channel_id):
            # data_tuple = (channel_id, pfp, channel_name, sub_count, time.strftime('%Y-%m-%d %H:%M:%S'))
            server.insert_row(CONFIG["TABLES"]["daily"], DATA_SETTING["DAILY_HEADER"], (data_tuple[0], data_tuple[3]))
            server.insert_row(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
            return
        elif refresh_daily:
            server.update_row(CONFIG["TABLES"]["daily"], "channel_id", channel_id, "sub_diff", sub_count)
            server.insert_row(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
    
    exclude_channels = fs.get_excluded_channels()
    refresh_daily = fs.check_diff_refresh()
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
        data_tuple = (channel_id, pfp, channel_name, sub_count, sub_org, video_count, time.strftime('%Y-%m-%d %H:%M:%S'))
        server.insert_row(name = CONFIG["TABLES"]["live"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
        record_diff_data(data_tuple, refresh_daily)


@log("Running Holodex Generation")
def holodex_generation(server: SQLHandler):
    """
    Generates the data from the Holodex API
    """
    holodex_organizations = DATA_SETTING["HOLODEX_ORGS"].split(",")
    server.clear_table(CONFIG["TABLES"]["live"])
    server.reset_auto_increment(CONFIG["TABLES"]["live"])
    holodex = HolodexAPI(CONFIG["API"]["holodex"])
    for organization in holodex_organizations:
        holodex.set_organization(organization)
        subscriber_data = holodex.get_subscriber_data()
        record_subscriber_data(subscriber_data)
    #for channel in subscriber_data:
    #    print(channel["name"] + " " + channel["group"] + " " + channel["video_count"] )
    #input()
    return holodex.get_generated_channel_data(), holodex.get_inactive_channels()

@log("Running YouTube Generation")
def youtube_generation(server: SQLHandler):
    """
    Generates the data from the YouTube API
    """
    ytapi = YouTubeAPI(CONFIG["API"]["youtube"])
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NijiTrack - A Subscriber Tracker")
    parser.add_argument('--mode', choices=['yt', 'holodex'], help='Specify the data source to use (yt or holodex)')
    args = parser.parse_args()
    server = SQLHandler(CONFIG["SQL"]["host"], CONFIG["SQL"]["user"], CONFIG["SQL"]["password"], CONFIG["SQL"]["database"])
    initialize_database(server)
    if args.mode == 'yt':
        print("Using YouTube API")
        channel_data = youtube_generation(server)
        inactive_channels = fs.get_excluded_channels()
    else:
        channel_data, inactive_channels = holodex_generation(server)
    fs.update_excluded_channels(inactive_channels)
    graph_html = graph.plot_subscriber_count_over_time(server, CONFIG["TABLES"]["historical"], exclude_channels=combine_excluded_channel_ids(inactive_channels, fs.get_excluded_channels()))
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(graph_html)