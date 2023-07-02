def generate_html_table(server, table, diff_table, headers=["Rank", "Liver", "Subscriber", "Difference (24hr)"]):
    def get_daily_difference_subs(sub_count_str: str):
        diff_cursor = server.get_connection().cursor()
        diff_cursor.execute(query)
        diff_data = diff_cursor.fetchall()
        old_sub_count = int(diff_data[0][0])
        current_sub_count = int(sub_count_str)
        if old_sub_count > current_sub_count:
            return f"-{old_sub_count - current_sub_count}"
        else:
            return f"+{current_sub_count - old_sub_count}"
    cursor = server.get_connection().cursor()
    query = f"SELECT id, channel_id, name, subscriber_count, timestamp, profile_pic FROM {table} ORDER by subscriber_count DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    header = "<tr>"
    for h in headers:
        header += f"<th>{h}</th>"
    header += "</tr>"
    table_html = "<table>"
    table_html += header
    rank = 1
    for row in data:
        table_row = "<tr>"
        table_row += f"<td>{rank}</td>"
        rank += 1
        for i, col in enumerate(row):
            if cursor.description[i][0] == "name":
                channel_url = f"/stats/{row[2]}"
                profile_pic_url = row[5]
                table_row += f"<td><a href='{channel_url}'><img src='{profile_pic_url}' height='50px' width='50px'>{col}</a></td>"
            elif cursor.description[i][0] == "subscriber_count":
                formatted_sub_count = "{:,.0f}".format(int(col))
                table_row += f"<td>{formatted_sub_count}</td>"
            elif cursor.description[i][0] == "timestamp":
                query = f"SELECT sub_diff FROM {diff_table} WHERE channel_id = '{row[1]}'"
                try:
                    table_row += f"<td>{get_daily_difference_subs(row[3])}</td>"
                except IndexError:
                    raise Exception("Are you trying to use a new set of channels?\nPlease delete last_refresh.txt in data folder first!")
            elif cursor.description[i][0] not in ["id", "channel_id", "profile_pic"]:
                table_row += f"<td>{col}</td>"
        table_row += "</tr>"
        table_html += table_row
    table_html += "</table>"
    cursor.close()
    return table_html

def generate_individual_table(server, table_name, channel_name, param="LIMIT 7"):
    cursor = server.get_connection().cursor()
    query = f"SELECT subscriber_count, timestamp FROM {table_name} WHERE name=\"{channel_name}\" GROUP BY DATE(timestamp) ORDER by timestamp DESC " + param
    cursor.execute(query)
    data = cursor.fetchall()
    table = "<table>"
    header = "<tr>"
    header_cols = ["Subscribers", "Timestamp"]
    for col in header_cols:
        header += f"<th>{col}</th>"
    header += "</tr>"
    table += header
    for row in data:
        table += "<tr>"
        for i, col in enumerate(row):
            if cursor.description[i][0] == "subscriber_count":
                formatted_sub_count = "{:,.0f}".format(int(col))
                table += f"<td>{formatted_sub_count}</td>"
            else:
                table += f"<td>{col}</td>"
        table += "</tr>"
    table += "</table>"
    cursor.close()
    return table