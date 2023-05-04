import os
import sys
import time

import sql.graph_builder as gb
import sql.table_builder as tb
import fileutil as fs
import html_gen.html_gen as ht
from sql.sql_handler import SQLHandler
from webapi.holodex import HolodexAPI
from webapi.youtube import YouTubeAPI
from config import *

def update_database(server: SQLHandler, data):
    server.clear_table(TABLE_NAME)
    server.reset_auto_increment(TABLE_NAME)
    excluded_channels = fs.get_excluded_channels()
    refresh_diff_table = fs.check_diff_refresh()
    for channel in data:
        channel_id = channel['id']
        if channel_id in excluded_channels:
            continue
        pfp = channel['photo']
        name = channel['english_name']
        sub_count = channel['subscriber_count']

        if name is None: # if the channel doesn't have an english name, use the japanese name
            name = channel['name']
        name = name.encode("ascii", "ignore").decode()

        data_row = f"'{channel_id}', '{pfp}','{name}', {sub_count}, '{time.strftime('%Y-%m-%d %H:%M:%S')}'"
        server.create_table(DAY_DIFF_TABLE_NAME, DIFF_COLUMNS)

        # Difference should only be calculated every 24 hours
        # If the channel is new then calculate now, else then make sure 24 hours has passed since last reading
        if refresh_diff_table or not server.check_row_exists(DAY_DIFF_TABLE_NAME, "channel_id", channel_id):
            if not server.check_row_exists(DAY_DIFF_TABLE_NAME, "channel_id", channel_id):
                server.insert_data(DAY_DIFF_TABLE_NAME,
                                   diff_columns, f"'{channel_id}', {sub_count}")
            else:
                server.update_row(DAY_DIFF_TABLE_NAME, "channel_id", channel_id, "sub_diff", sub_count)
            server.insert_data(HISTORICAL_TABLE_NAME, table_columns, data_row)

        # make updates to the main table
        server.insert_data(TABLE_NAME, table_columns, data_row)
        name_table = "channel_"+channel_id.lower()+"_subscriber_data"
        name_table = name_table.replace("-", "$")
        server.create_table(name_table, TABLE_COLUMNS)
        server.insert_data(name_table, table_columns, data_row)
        # server.drop_table(name_table)

def generate_individual_stats(server: SQLHandler, data):
    for channel in data:
        channel_id = channel['id']
        if channel_id in fs.get_excluded_channels():
            continue
        name = channel['english_name']
        desc = channel['description']
        pfp = channel['photo']
        sub_count = channel['subscriber_count']
        sub_count_str = "{:,.0f}".format(int(sub_count))
        if name is None:
            name = channel['name']
        name = name.encode("ascii", "ignore").decode()
        print("GENERATING PAGE FOR "+name+"...")

        # Calculate table key name stored in the database
        table_key = "channel_"+channel_id.lower()+"_subscriber_data"
        table_key = table_key.replace("-", "$")

        # Generate missing directories
        if not os.path.exists("stats"):
            os.mkdir("stats")
        if not os.path.exists("tables"):
            os.mkdir("tables")

        with open(ROOT_STORAGE_PATH+"stats/"+name+".html", "w", encoding="utf-8") as file:
            range_query = f"SELECT name, subscriber_count, timestamp FROM {table_key} WHERE timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) ORDER BY timestamp DESC"
            group_query = f"SELECT name, subscriber_count, timestamp FROM {table_key} GROUP BY DATE(timestamp) ORDER BY timestamp DESC"
            file.write(ht.generate_meta_data(name + " - "+ META_DATA_TITLE, META_DATA_DESCRIPTION, META_PROFILE_PIC)+"\n"+
                       ht.side_swipe_header(sub_count_str + " Subscribers", COLOR_THEME, ROOT_URL)+"\n"+
                       ht.generate_info_card(name, channel_id, pfp, desc)+
                       gb.generate_projection(server.host_name, server.username, server.password, DB_NAME, table_key, int(sub_count), TIMEZONE_STR)+
                       gb.plot_subscriber_count_over_time(server.host_name, server.username, server.password, DB_NAME, table_name=table_key, gtitle=name+" Subscriber Trend", overrideQuery=group_query) +
                       ht.generate_html_divider("Recent Subscriber Data:") +
                       gb.plot_subscriber_count_over_time(server.host_name, server.username, server.password, DB_NAME, table_name=table_key, gtitle=name+" Last 7 Days Trend", overrideQuery=range_query, markers="lines+markers") +
                       tb.generate_individual_table(server.host_name, server.username, server.password, DB_NAME, table_key)+
                       ht.generate_full_table_button(ROOT_URL+"/tables/"+name) +
                       ht.generate_doctype_footer()
                       )
        with open(ROOT_STORAGE_PATH+"tables/"+name+".html", "w", encoding="utf-8") as file:
            file.write(ht.generate_meta_data(name + " - "+ META_DATA_TITLE, META_DATA_DESCRIPTION, META_PROFILE_PIC)+"\n"+
                       ht.side_swipe_header(name, COLOR_THEME, ROOT_URL)+"\n"+
                       ht.generate_info_card(name, channel_id, pfp, desc)+
                       tb.generate_individual_table(server.host_name, server.username, server.password, DB_NAME, table_key, param="") +
                       ht.generate_doctype_footer())


def main(mode=0):
    address, user, password = fs.get_login_data()
    server = SQLHandler(address, user, password, DB_NAME)
    server.create_table(TABLE_NAME, TABLE_COLUMNS)
    server.create_table(HISTORICAL_TABLE_NAME, TABLE_COLUMNS)
    server.create_table(DAY_DIFF_TABLE_NAME, DIFF_COLUMNS)
    excluded_channels = []
    data = []
    if mode == 0:
        holodex_organizations = HOLODEX_ORG.split(",")
        print("Running Holodex API Data Collection\n"+"Found "+str(len(holodex_organizations))+" organizations")
        for org in holodex_organizations:
            hldex = HolodexAPI(fs.get_api_key("holodex_api_key"), member_count = ORG_MEMBER_COUNT, organization = org)
            data += hldex.get_data_all_channels()
            excluded_channels += hldex.get_exclude_channels()

    elif mode == 1:
        print("Running YouTube API Data Collection")
        ytapi = YouTubeAPI(fs.get_api_key("youtube_api_key"))
        data = ytapi.get_data_all_channels(fs.get_local_channels())

    # Updating DB and generating HTML data
    update_database(server, data)
    excluded_channels += fs.get_excluded_channels()
    with open(ROOT_STORAGE_PATH+"index.html", "w", encoding="utf-8") as file:
        file.write(ht.generate_meta_data(META_DATA_TITLE, META_DATA_DESCRIPTION, META_PROFILE_PIC) +
                   ht.generate_title_banner(HEADER_TITLE, COLOR_THEME) +
                   gb.plot_subscriber_count_over_time(address, user, password, DB_NAME, HISTORICAL_TABLE_NAME, gtitle="Subscriber Count Over Time", exclude_channels=excluded_channels) +
                   "\n"+ht.generate_html_divider("Last Updated: "+time.strftime('%Y-%m-%d %H:%M:%S')+" "+ TIMEZONE) +
                   tb.sql_to_html_table(address, user, password, DB_NAME, TABLE_NAME, root_url=ROOT_URL) +
                   ht.build_footer_info(FOOTER_MESSAGE) +
                   ht.generate_doctype_footer())

    # Generating individual pages
    generate_individual_stats(server, data)

def generate_channel_files():
    """
    Generates the channels.txt and exclude_channels.txt files based on Holodex listings
    """
    if not UPDATE_LOCAL_RECORDS:
        return
    print("Running Channel Files Update")
    hldex = HolodexAPI(fs.get_api_key("holodex_api_key"), member_count = ORG_MEMBER_COUNT,
                       organization = HOLODEX_ORG)
    hldex.get_data_all_channels()
    if not os.path.exists("data"):
        os.mkdir("data")
    with open("data/channels.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(hldex.get_active_channels()))
    with open("data/exclude_channels.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(hldex.get_exclude_channels()))
    print("Success! Channel Files Updated!")


if __name__ == "__main__":
    MODE = 0
    if len(sys.argv) > 1:
        MODE = int(sys.argv[1])
        ROOT_STORAGE_PATH = sys.argv[2]
    main(MODE)
