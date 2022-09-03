from order_book_module import OrderBook
from csv_module import CSVHandler
import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from datetime import timedelta, datetime

order_book = OrderBook()
csv_handler = CSVHandler()


app = Dash(__name__)

app.layout = html.Div([
    html.Div(id='updater'),
    dcc.Interval('interval-update', interval=1000),
    dcc.Dropdown(options=[
        {'label': '1min', 'value': 1},
        {'label': '3min', 'value': 3},
        {'label': '5min', 'value': 5},
        {'label': '15min', 'value': 15},
        {'label': '30min', 'value': 30},
        {'label': '1hour', 'value': 60},
        {'label': '3hour', 'value': 180},
        {'label': '6hour', 'value': 360},
        {'label': '12hour', 'value': 720},
        {'label': '24hour', 'value': 1440}],
        value=3,
        id='time-filter'),
    dcc.Graph(id='live-graph'),
    dcc.Interval('interval-live', interval=1000),
    
])


@app.callback(
    Output('updater', 'children'),
    [
        Input('interval-update', 'n_intervals'),
    ]
)
def update_graph(n):
    data = order_book.get_current_volume()

    csv_handler.write(row=[data['date_time'], data['bids'], data['asks']])

    return 'Time Interval'


@app.callback(
    Output('live-graph', 'figure'),
    [
        Input('interval-live', 'n_intervals'),
        Input('time-filter', 'value')
    ]
)
def live_graph(n, value):

    # Load data
    df = pd.read_csv("data.csv")

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=list(df.date), y=list(df.bids), line=dict(color='#ff2f24'), name='bids'))

    fig.add_trace(
        go.Scatter(x=list(df.date), y=list(df.asks), line=dict(color='#139c06'), name='asks'))

    # Set title
    fig.update_layout(
        title_text="Bids & Asks Volume History"
    )

    delta = timedelta(minutes=value)

    current_date = datetime.now().replace(microsecond=0)

    forward = timedelta(seconds=10)

    # Add range slider
    fig.update_layout(
        xaxis=dict(range=[current_date - delta, current_date + forward])
    )

    return fig


if __name__ == '__main__':
    app.run_server()
