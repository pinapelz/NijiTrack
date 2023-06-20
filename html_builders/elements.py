import math
import pandas as pd
import warnings
from datetime import datetime, timedelta

def build_title_banner(text: str, menu_items):
    banner_html = f"""
    <div class="banner-container">
        <div class="banner-text">{text}</div>
    </div>
    <div class="menu-bar">
    """
    for item in menu_items:
        banner_html += f"""
            <a href="{item[1]}">{item[0]}</a>

        """
    banner_html += "</div>"
    return banner_html

def build_projection_card(server, table_name, curr_subscribers, channel_name,
                        timezone = "Pacific Standard Time"):
    def get_next_milestone(subscriber_count):
        num_digits = len(str(subscriber_count))
        if num_digits <= 4:
            milestone_interval = 10000
        else:
            milestone_interval = 10 ** (num_digits - 1)
        next_milestone = math.ceil(
            subscriber_count / milestone_interval) * milestone_interval

        return next_milestone

    warnings.filterwarnings('ignore')  # Ignore pandas warning regarding pyodbc
    def create_milestone_card(time_until_milestone, next_milestone, not_enough_data = False,
                              declining = False):
        now = datetime.now()
        milestone_date = (
                now + timedelta(seconds = time_until_milestone)).strftime('%Y-%m-%d')
        relative_time = now + timedelta(seconds = time_until_milestone) - now
        next_milestone_str = "{:,}".format(next_milestone)
        if relative_time.days > 1:
            relative_time_str = f"In {relative_time.days} days"
        elif relative_time.days == 1:
            relative_time_str = f"In {relative_time.days} day"
        elif relative_time.days < 0:
            relative_time_str = f"{-relative_time.days} days ago"
        elif not_enough_data:
            relative_time_str = "Not enough data"
        elif declining:
            relative_time_str = "Declining"
        else:
            relative_time_str = "Today"
        card = f"""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); font-family: 'Poppins', sans-serif;">
            <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Next Milestone</div>
            <div style="font-size: 18px; margin-bottom: 10px;">{next_milestone_str}</div>
            <div style="display: flex; flex-direction: row; justify-content: space-between; margin-bottom: 10px;">
                <div style="font-size: 16px;">Estimated Date:</div>
                <div style="font-size: 16px; font-weight: bold;">{milestone_date}</div>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: space-between; color: #888;">
                <div style="font-size: 16px;">{relative_time_str}</div>
                <div style="font-size: 16px;">{timezone}</div>
            </div>
        </div>
        <br>
        """
        return card
    query = f"SELECT name, subscriber_count, timestamp FROM {table_name} WHERE timestamp >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND name = \"{channel_name}\" ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, server.get_connection())
    df = df.sort_values(by = 'timestamp')
    # get the rate of change from first data point to last data point
    first_data = df.iloc[0]
    last_data = df.iloc[-1]
    delta_sub_count = last_data['subscriber_count'] - first_data['subscriber_count']
    delta_time = (last_data['timestamp'] - first_data['timestamp']).total_seconds()

    # Calculate the average rate of change of subscriber_count over time
    avg_rate_of_change = delta_sub_count / delta_time
    next_milestone = get_next_milestone(curr_subscribers)
    if avg_rate_of_change == 0 or math.isnan(avg_rate_of_change) or math.isinf(avg_rate_of_change):
        return create_milestone_card(0, next_milestone, not_enough_data = True)
    if avg_rate_of_change < 0:
        return create_milestone_card(0, next_milestone, declining = True)
    time_to_next_milestone = (
                                     next_milestone - curr_subscribers) / avg_rate_of_change
    return create_milestone_card(time_to_next_milestone, next_milestone)



