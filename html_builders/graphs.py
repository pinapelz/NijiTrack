import plotly.graph_objs as go
import pandas as pd
import warnings
import math
from datetime import datetime, timedelta
import numpy as np
import mysql.connector
from mysql.connector import errorcode

def plot_subscriber_count_over_time(server, table_name, gtitle = "Subscriber Count Over Time for Nijisanji Members",
                                    overrideQuery = None, markers = "lines", exclude_channels = []):
    warnings.filterwarnings('ignore')  # Ignore pandas warning regarding pyodbc
    query = f"SELECT name, subscriber_count, timestamp, channel_id FROM {table_name} ORDER by timestamp DESC" if overrideQuery is None else overrideQuery
    df = pd.read_sql_query(query, server.get_connection())
    groups = df.groupby("name")
    fig = go.Figure()
    config = dict({'responsive': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['pan2d', 'zoomIn2d', 'zoomOut2d']})
    for channel, group in groups:
        if len(exclude_channels) != 0 and group['channel_id'].iloc[0] in exclude_channels:
            continue
        fig.add_trace(go.Scattergl(
            x = group["timestamp"], y = group["subscriber_count"], name = channel, mode = markers,
            showlegend = True))
    fig.update_layout(
        title = {'text': gtitle, 'x': 0.5, 'xanchor': 'center',
                 'yanchor': 'top', 'font': {'family': 'Arial', 'size': 30}},
        xaxis_title = "Timestamp",
        yaxis_title = "Subscribers",
        legend = dict(font = dict(size = 16), title = dict(text = "Channels")),
        height = 950,
    )
    return fig.to_html(config = config)