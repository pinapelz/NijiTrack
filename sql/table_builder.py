import mysql.connector
from mysql.connector import errorcode

def sql_to_html_table(host, username, password, database_name, table_name,
                      diff_table="24h_historical", headers=["Rank", "Liver", "Subscribers", "Difference (24hr)"], root_url="https://nijitracker.com"):
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=host, database=database_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    query = f"SELECT id, channel_id, name, subscriber_count, timestamp, profile_pic FROM {table_name} ORDER by subscriber_count DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    table = "<table>"
    header = "<tr>"
    header_cols = headers
    for col in header_cols:
        header += f"<th>{col}</th>"
    header += "</tr>"
    table += header
    rank = 1
    for row in data:
        table += "<tr>"
        table += f"<td>{rank}</td>"
        rank += 1
        for i, col in enumerate(row):
            if cursor.description[i][0] == "name":
                channel_url = f"{root_url}/stats/{row[2]}"
                profile_pic_url = row[5]
                table += f"<td><a href='{channel_url}'><img src='{profile_pic_url}' height='50px' width='50px'>{col}</a></td>"
            elif cursor.description[i][0] == "subscriber_count":
                formatted_sub_count = "{:,.0f}".format(int(col))
                table += f"<td>{formatted_sub_count}</td>"
            elif cursor.description[i][0] == "timestamp":
                query = f"SELECT sub_diff FROM {diff_table} WHERE channel_id = '{row[1]}'"
                try:
                    diff_cursor = cnx.cursor()
                    diff_cursor.execute(query)
                    diff_data = diff_cursor.fetchall()
                    old_sub_count = int(diff_data[0][0])
                    current_sub_count = int(row[3])
                    if old_sub_count > current_sub_count:
                        difference = f"-{old_sub_count - current_sub_count}"
                    else:
                        difference = f"+{current_sub_count - old_sub_count}"
                    table += f"<td>{difference}</td>"
                except IndexError:
                    raise Exception("Are you trying to use a new set of channels?\nPlease delete last_refresh.txt in data folder first!")
            elif cursor.description[i][0] not in ["id", "channel_id", "profile_pic"]:
                table += f"<td>{col}</td>"

                
        table += "</tr>"
    table += "</table>"
    style = "<style>\
            table {\
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;\
                font-size: 16px;\
                border-collapse: separate;\
                border-spacing: 0;\
                width: 100%;\
                max-width: 1570px;\
                margin: 0 auto;\
                background-color: #fff;\
                border-radius: 5px;\
                overflow: hidden;\
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);\
            }\
            th, td {\
                text-align: left;\
                padding: 12px 15px;\
                font-size: 18px;\
                border-bottom: 1px solid #ddd;\
            }\
            th {\
                background-color: #2a4b71;\
                color: #fff;\
                font-weight: bold;\
                text-transform: uppercase;\
                letter-spacing: 0.03em;\
            }\
            td:nth-child(3), td:nth-child(4) {\
                text-align: left;\
                padding: 12px 15px;\
                font-size: 18px;\
                border-bottom: 1px solid #ddd;\
            }\
            tbody tr:nth-child(even) {\
                background-color: #f2f2f2;\
            }\
            tbody tr:hover {\
                background-color: #ddd;\
            }\
            a {\
                color: #3c8dbc;\
                text-decoration: none;\
            }\
            </style>"
    style += "<style>\
        @media screen and (max-width: 1024px) {\
            table {\
                font-size: 14px;\
            }\
            th, td {\
                padding: 8px 10px;\
                font-size: 16px;\
            }\
        }\
        @media screen and (max-width: 768px) {\
            th, td {\
                padding: 5px 8px;\
                font-size: 14px;\
            }\
        }\
        @media screen and (max-width: 600px) {\
            th, td {\
                padding: 3px 5px;\
                font-size: 10px;\
            }\
        }\
        @media screen and (max-width: 400px) {\
            th, td {\
                padding: 2px 4px;\
                font-size: 8px;\
            }\
        }\
        </style>"


    cursor.close()
    cnx.close()
    return table + style


def generate_individual_table(host, username, password, database_name, table_name, param="LIMIT 7"):
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=host, database=database_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    cursor = cnx.cursor()
    query = f"SELECT subscriber_count, timestamp FROM {table_name} GROUP BY DATE(timestamp) ORDER by timestamp DESC " + param
    
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
    style = "<style>\
            table {\
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;\
                font-size: 16px;\
                border-collapse: separate;\
                border-spacing: 0;\
                width: 100%;\
                max-width: 1570px;\
                margin: 0 auto;\
                background-color: #fff;\
                border-radius: 5px;\
                overflow: hidden;\
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);\
            }\
            th, td {\
                text-align: left;\
                padding: 12px 15px;\
                font-size: 18px;\
                border-bottom: 1px solid #ddd;\
            }\
            th {\
                background-color: #2a4b71;\
                color: #fff;\
                font-weight: bold;\
                text-transform: uppercase;\
                letter-spacing: 0.03em;\
            }\
            td:nth-child(3), td:nth-child(4) {\
                text-align: left;\
                padding: 12px 15px;\
                font-size: 18px;\
                border-bottom: 1px solid #ddd;\
            }\
            tbody tr:nth-child(even) {\
                background-color: #f2f2f2;\
            }\
            tbody tr:hover {\
                background-color: #ddd;\
            }\
            a {\
                color: #3c8dbc;\
                text-decoration: none;\
            }\
            </style>"
    style += "<style>\
        @media screen and (max-width: 1024px) {\
            table {\
                font-size: 14px;\
            }\
            th, td {\
                padding: 8px 10px;\
                font-size: 16px;\
            }\
        }\
        @media screen and (max-width: 768px) {\
            th, td {\
                padding: 5px 8px;\
                font-size: 14px;\
            }\
        }\
        @media screen and (max-width: 600px) {\
            th, td {\
                padding: 3px 5px;\
                font-size: 12px;\
            }\
        }\
        @media screen and (max-width: 400px) {\
            th, td {\
                padding: 2px 4px;\
                font-size: 10px;\
            }\
        }\
        </style>"

    cursor.close()
    cnx.close()
    return table + style
