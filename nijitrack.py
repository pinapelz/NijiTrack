import os
import sys
import time

import fileutil as fs
from sql.sql_handler import SQLHandler
from webapi.holodex import HolodexAPI
from webapi.youtube import YouTubeAPI
from decorators import *
import html_builders.builder as builder
import sys




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
    def record_diff_data(data_tuple: tuple):
        refresh_daily = fs.check_diff_refresh()
        if not server.check_row_exists(CONFIG["TABLES"]["daily"], "channel_id", channel_id):
            # data_tuple = (channel_id, pfp, channel_name, sub_count, time.strftime('%Y-%m-%d %H:%M:%S'))
            server.insert_row(CONFIG["TABLES"]["daily"], DATA_SETTING["DAILY_HEADER"], (data_tuple[0], data_tuple[3]))
            server.insert_row(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
            return
        elif refresh_daily:
            server.update_row(CONFIG["TABLES"]["daily"], "sub_count", sub_count, "channel_id", channel_id)
            server.insert_row(name = CONFIG["TABLES"]["historical"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
    
    exclude_channels = fs.get_excluded_channels()
    for channel in data:
        channel_id = channel["id"]
        if channel_id in exclude_channels:
            continue
        pfp = channel["photo"]
        sub_count = channel["subscriber_count"]
        channel_name = channel["english_name"]
        if channel_name is None:
            channel_name = channel["name"]
        channel_name = transform_sql_string(channel_name)
        data_tuple = (channel_id, pfp, channel_name, sub_count, time.strftime('%Y-%m-%d %H:%M:%S'))
        server.insert_row(name = CONFIG["TABLES"]["live"], column = DATA_SETTING["LIVE_HEADER"], data=data_tuple)
        record_diff_data(data_tuple)

@log("Generating Indvidual Channel Pages")
def generate_individual_pages(server: SQLHandler, data: list):
    if not os.path.exists("stats"):
        os.mkdir("stats")
    if not os.path.exists("tables"):
        os.mkdir("tables")
    excluded_channels = fs.get_excluded_channels()
    for channel in data:
        if channel["id"] in excluded_channels:
            continue
        try:
            builder.build_individual_page(server, CONFIG, channel)
            builder.build_table_page(server, CONFIG, channel)
        except Exception as e:
            print(f"ERROR: {e} - {channel['name']}")
            continue



@log("Running Holodex Generation")
def holodex_generation(server: SQLHandler):
    holodex_organizations = DATA_SETTING["HOLODEX_ORGS"].split(",")
    server.clear_table(CONFIG["TABLES"]["live"])
    server.reset_auto_increment(CONFIG["TABLES"]["live"])
    holodex = HolodexAPI(CONFIG["API"]["holodex"])
    for organization in holodex_organizations:
        holodex.set_organization(organization)
        record_subscriber_data(holodex.get_subscriber_data())
    return holodex.get_generated_channel_data(), holodex.get_inactive_channels()

@log("Running YouTube Generation")
def youtube_generation(server: SQLHandler):
    ytapi = YouTubeAPI(CONFIG["API"]["youtube"])
    server.clear_table(CONFIG["TABLES"]["live"])
    server.reset_auto_increment(CONFIG["TABLES"]["live"])
    data = ytapi.get_data_all_channels(fs.get_local_channels())
    record_subscriber_data(data)
    return data

def get_excluded_channel_ids(inactive_channel_data: list, excluded_channels: list):
    channel_ids = []
    for inactive_channel in inactive_channel_data:
        if inactive_channel in excluded_channels:
            continue
        channel_ids.append(inactive_channel)
    return channel_ids


if __name__ == "__main__":
    server = SQLHandler(CONFIG["SQL"]["host"], CONFIG["SQL"]["user"], CONFIG["SQL"]["password"], CONFIG["SQL"]["database"])
    initialize_database(server)
    channel_data, inactive_channels = holodex_generation(server) # channel_data = youtube_generation(server)
    generate_individual_pages(server, channel_data)
    builder.build_ranking_page(server, CONFIG, get_excluded_channel_ids(inactive_channels, fs.get_excluded_channels()))
