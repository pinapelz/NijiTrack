from jinja2 import Environment, FileSystemLoader
import html_builders.elements as elements
import html_builders.graphs as graphs
import html_builders.tables as tables
import os
import time

MENU_ITEMS = [
    ("Nijitracker", "https://www.nijitracker.com"),
    ("Pettantracker", "https://nijitracker.com/pettantrack")
]


def build_ranking_page(server, CONFIG: dict, exclude_channels: list = []):
    page_path = os.path.join(CONFIG["PATH"]["root_html"], "index.html")
    if not os.path.exists(page_path):
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("ranking.html")

    input_dict = {
        "meta_image_url": CONFIG["WEBSITE"]["icon"],
        "meta_description": CONFIG["WEBSITE"]["description"],
        "meta_title": CONFIG["WEBSITE"]["title"],
        "title_banner": elements.build_title_banner(
            CONFIG["WEBSITE"]["title"],
            MENU_ITEMS
        ),
        "ranking_graph": graphs.plot_subscriber_count_over_time(server, CONFIG["TABLES"]["historical"], exclude_channels=exclude_channels),
        "divider": "Last Updated: " + time.strftime('%Y-%m-%d %H:%M:%S') + " " + CONFIG["WEBSITE"]["timezone"],
        "ranking_table": tables.generate_html_table(server, CONFIG["TABLES"]["live"], CONFIG["TABLES"]["daily"]),
        "footer": CONFIG["WEBSITE"]["footer_message"]
    }
    output = template.render(input_dict)
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(output)

def build_individual_page(server, CONFIG: dict, channel_data: str):
    def transform_sql_string(string: str) -> str:
        return string.encode("ascii", "ignore").decode().replace("'", "''")
    channel_id = channel_data["id"]
    desc = channel_data["description"]
    pfp = channel_data["photo"]
    sub_count = channel_data["subscriber_count"]
    channel_name = channel_data["english_name"]
    if channel_name is None:
        channel_name = channel_data["name"]
    channel_name = transform_sql_string(channel_name)
    sub_count_str = "{:,.0f}".format(int(sub_count))
    page_path = os.path.join(CONFIG["PATH"]["root_html"], channel_name + ".html")
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("individual.html")
    input_dict = {
        "meta_image_url": CONFIG["WEBSITE"]["icon"],
        "meta_description": CONFIG["WEBSITE"]["description"],
        "meta_title": channel_name + " - " + CONFIG["WEBSITE"]["title"],
        "homepage_url": CONFIG["WEBSITE"]["homepage"],
        "sub_text": sub_count_str + " Subscribers",
        "name": channel_name,
        "profile_pic": pfp,
        "description": desc,
        "channel_id": channel_id,
        "projection_card": elements.build_projection_card(server, CONFIG["TABLES"]["historical"], int(sub_count), channel_name, timezone = CONFIG["WEBSITE"]["timezone"]),
        "subscriber_trend": graphs.plot_subscriber_count_over_time(server, CONFIG["TABLES"]["historical"], gtitle = "Subscriber Count Over Time for " + channel_name, overrideQuery = f"SELECT name, subscriber_count, timestamp, channel_id FROM {CONFIG['TABLES']['historical']} WHERE channel_id = '{channel_id}' ORDER by timestamp DESC", markers = "lines+markers"),
        "divider": "Recent Subscriber Data:",
        "weekly_trend": graphs.plot_subscriber_count_over_time(server, CONFIG["TABLES"]["historical"], gtitle = "Weekly Subscriber Count Over Time for " + channel_name, overrideQuery = f"SELECT name, subscriber_count, timestamp, channel_id FROM {CONFIG['TABLES']['historical']} WHERE channel_id = '{channel_id}' AND timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY) ORDER by timestamp DESC", markers = "lines+markers"),
        "full_table_url": "/tables/"+channel_name
    }
    output = template.render(input_dict)
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(output)

def build_table_page(server, CONFIG: dict, channel_data: str):
    def transform_sql_string(string: str) -> str:
        return string.encode("ascii", "ignore").decode().replace("'", "''")
    channel_id = channel_data["id"]
    desc = channel_data["description"]
    pfp = channel_data["photo"]
    sub_count = channel_data["subscriber_count"]
    channel_name = channel_data["english_name"]
    if channel_name is None:
        channel_name = channel_data["name"]
    channel_name = transform_sql_string(channel_name)

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("full_table.html")
  
    input_dict = {
        "meta_image_url": CONFIG["WEBSITE"]["icon"],
        "meta_description": CONFIG["WEBSITE"]["description"],
        "meta_title": channel_name + " - " + CONFIG["WEBSITE"]["title"],
        "homepage_url": CONFIG["WEBSITE"]["homepage"],
        "sub_text": channel_name,
        "full_table": tables.generate_individual_table(server, CONFIG["TABLES"]["historical"], channel_name),
        "name": channel_name,
        "profile_pic": pfp,
        "description": desc,
        "channel_id": channel_id,
    }
    output = template.render(input_dict)
    page_path = os.path.join("tables", channel_name + ".html")
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(output)


    