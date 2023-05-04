import os.path
import json
import time


def _read_file(path: str, lines=True) -> list:
    # reads a file and returns a list of lines
    with open(path, "r", encoding="utf-8") as file:
        if not lines:
            return file.read()
        return file.read().splitlines()


def get_login_data(path="config.json"):
    # gets login data from config.json
    data = json.loads(_read_file(os.path.join(path), lines=False))
    try:
        return data["address"], data["user"], data["password"]
    except KeyError:
        raise Exception("Login data not found")


def get_api_key(api: str, path="config.json"):
    # gets api key from config.json
    data = json.loads(_read_file(os.path.join(path), lines=False))
    try:
        return data[api]
    except KeyError:
        raise Exception(f"API key for {api} not found")


def get_excluded_channels():
    # gets excluded channels from exclude_channel.txt
    if not os.path.exists(os.path.join("data","exclude_channel.txt")):
        open(os.path.join("data","exclude_channel.txt"), "w").close()
    excluded_channels = _read_file(os.path.join("data","exclude_channel.txt"))
    return excluded_channels


def save_local_channels(data: list, path: str = "data"):
    """
    Save the channel names and ids locally for when the API is down
    """
    path = os.path.join(path, "channels.txt")
    excluded_channels = get_excluded_channels()
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
    with open(path, "w", encoding="utf-8") as file:
        for channel in data:
            if channel['id'] in excluded_channels:
                continue
            file.write(f"{channel['id']},{channel['english_name']}\n")

def get_local_channels(path: str = "data"):
    """
    Get the channel names and ids locally for when the API is down
    """
    path = os.path.join(path, "channels.txt")
    if not os.path.exists(path):
        raise Exception("Local channel data not found")
    with open(path, "r", encoding="utf-8") as file:
        rows =  file.read().splitlines()
        return [tuple(row.split(",")) for row in rows]

def check_diff_refresh():
    if not os.path.exists(os.path.join("data","last_refresh.txt")):
        with open(os.path.join("data","last_refresh.txt"), "w", encoding="utf-8") as file:
            file.write(time.strftime("%Y-%m-%d"))
            return True
    with open(os.path.join("data","last_refresh.txt"), "r", encoding="utf-8") as file:
        last_refresh = file.read()
    if last_refresh != time.strftime("%Y-%m-%d"):
        with open(os.path.join("data","last_refresh.txt"), "w", encoding="utf-8") as file:
            file.write(time.strftime("%Y-%m-%d"))
        return True
