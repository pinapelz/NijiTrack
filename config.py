"""
This file contains all the constants used in the main.py file
"""

"""
0 = Holodex
1 = YouTube API
"""
MODE = 1

# General database configurations
DB_NAME = "pinapelz$nijitrack"
TABLE_NAME = "subscriber_data"
TABLE_COLUMNS = "id INT PRIMARY KEY AUTO_INCREMENT, channel_id VARCHAR(255), profile_pic VARCHAR(255), name VARCHAR(255), subscriber_count INT, timestamp DATETIME"
HISTORICAL_TABLE_NAME = "subscriber_data_historical"
DAY_DIFF_TABLE_NAME = "24h_historical" # Stores the difference in subscriber count for each channel in the past 24 hours
DIFF_COLUMNS = "id INT PRIMARY KEY AUTO_INCREMENT, channel_id VARCHAR(255), sub_diff INT" # Stores the difference in subscriber count for each channel in the past 24 hours
table_columns = "channel_id, profile_pic, name, subscriber_count, timestamp"
diff_columns = "channel_id, sub_diff"

HEADER_TITLE = "Nijitracker" # Shows at the top of the page

# Message at the bottom of the webpage
FOOTER_MESSAGE = """
This is a demo of Nijitrack, a way to track historical subscriber data for any set of channels on YouTube.<br>
This webpage is not affiliated with ANYCOLOR or any of the channels listed here in any way<br>
Date Started: 2023-03-26
"""

# (Optional) for things like Discord embeds or Twitter cards
META_DATA_TITLE = "Nijitracker"
META_DATA_DESCRIPTION = "A site that tracks the historical subscriber data for Nijisanji affiliated livers (demo)"
META_PROFILE_PIC = "https://raw.githubusercontent.com/pinapelz/NijiTrack/master/assets/icon.png"


COLOR_THEME = "2a4b71"
ROOT_URL = "https://nijitracker.com"
TIMEZONE = "PST"
TIMEZONE_STR = "Pacific Standard Time"

ROOT_STORAGE_PATH = ""

# Skip the options below if you are not using Holodex
HOLODEX_ORG = "Nijisanji"
ORG_MEMBER_COUNT = 300


