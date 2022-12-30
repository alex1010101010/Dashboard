import pandas as pd
import numpy as np
import yfinance as yf
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash import callback
import time as time

# Globals
CHART_THEME = 'plotly_white'
tickers = ['SPY', '^FTSE', '^IXIC', 'GBPUSD=X', 'GBPEUR=X',
           'EURUSD=X', 'BTC-USD', 'ETH-USD', '^TNX', '^VIX', 'USDT-USD']

# Globals used by functions - Can be improved using classes
data = {}
EURUSD_30d = None
GBPUSD_30d = None
EURGBP_30d = None
df = None
t1 = None
t2 = None
t3 = None
df = None


def prepareData():
    print("Data was loaded again at:", time.process_time(), "s (Time is seconds the process has been active)")
    global data
    for i in tickers:
        data[i] = yf.Ticker(i).history(period='3y')['Close']

    # Get FX rates
    global EURUSD_30d
    global GBPUSD_30d
    global EURGBP_30d

    EURUSD_30d = yf.Ticker('EURUSD=X').history(period='30d')['Close']
    GBPUSD_30d = yf.Ticker('GBPUSD=X').history(period='30d')['Close']
    EURGBP_30d = yf.Ticker('EURGBP=X').history(period='30d')['Close']

    # Prepare data series
    global t1
    global t2
    global t3
    t1 = pd.Series(EURUSD_30d, name='EURUSD_30d')
    t2 = pd.Series(EURUSD_30d, name='GBPUSD_30d')
    t3 = pd.Series(EURUSD_30d, name='EURGBP_30d')

    # FX calcs
    global df
    df = pd.concat([t1, t2, t3], axis=1)


# Call once to ensure it is called, should be called regardless when the page is loaded
prepareData()
internal_dates = t1.index


# Functions that return currency changes
def get_daily_change_currency(tickerName):
    return float("{:.2f}".format(df[tickerName].iloc[-1] / df[tickerName].iloc[0] - 1))


def get_two_week_change_currency(tickerName):
    return float("{:.2f}".format(df[tickerName].iloc[-1] / df[tickerName].iloc[14] - 1))


def get_weekly_change_currency(tickerName):
    return float("{:.2f}".format(df[tickerName].iloc[-1] / df[tickerName].iloc[7] - 1))


def get_monthly_change_currency(tickerName):
    return float("{:.2f}".format(df[tickerName].iloc[-1] / df[tickerName].iloc[0] - 1))


def get_latest_currency_value(tickerName):
    return float("{:.2f}".format(df[tickerName][-1]))


# Chart generation function
def get_chart(ticker_name, plot_name):
    chart = go.Figure()
    chart.add_trace(go.Scatter(x=data[ticker_name].index, y=data[ticker_name],
                               mode='lines',  # you can also use "lines+markers", or just "markers"
                               name=plot_name))

    chart.layout.template = 'plotly_white'
    chart.layout.height = 500
    # this will help you optimize the chart space
    chart.update_layout(margin=dict(t=50, b=50, l=25, r=25))
    chart.update_layout(
        #     title='Business indicators (USD $)',
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Value: $ USD',
            titlefont_size=14,
            tickfont_size=12,
        ))
    return chart


# Currency figure generation function
def get_currency_figure(ticker_name):
    figure = go.Figure()
    figure.layout.template = CHART_THEME

    figure.add_trace(go.Indicator(
        mode="number+delta",
        value=float("{:.2f}".format(get_weekly_change_currency(ticker_name) * 100)),
        number={'suffix': " %"},
        title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
        delta={'position': "bottom", 'reference': 0.02, 'relative': False},
        domain={'row': 0, 'column': 0}))

    figure.add_trace(go.Indicator(
        mode="number+delta",
        value=float("{:.2f}".format(get_two_week_change_currency(ticker_name) * 100)),
        number={'suffix': " %"},
        title={"text": "<span style='font-size:0.7em;color:gray'>15 Days</span>"},
        delta={'position': "bottom", 'reference': 0, 'relative': False},
        domain={'row': 1, 'column': 0}))

    figure.add_trace(go.Indicator(
        mode="number+delta",
        value=float("{:.2f}".format(get_monthly_change_currency(ticker_name) * 100)),
        number={'suffix': "%"},
        title={"text": "<br><span style='font-size:0.7em;color:gray'>30 Days</span>"},
        delta={'position': "bottom", 'reference': 0.02, 'relative': False},
        domain={'row': 2, 'column': 0}))

    figure.update_layout(
        grid={'rows': 3, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30)
    )
    return figure


# HTML Definition
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '12rem',
    'padding': '2rem 1 rem',
    'background-color': 'lightgray',
}

CONTENT_STYLE = {
    'margin-left': '15rem',
    'margin-right': '2rem',
    'padding': '2rem' '1rem',
}

sidebar_content = html.Div(
    [
        html.Hr(),
        html.P('Navigation Menu', className='text-center'),
        dbc.Nav(
            [
                dbc.NavLink('Market', href="/", active='exact'),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


def generate_page1():
    prepareData()
    page1_content = dbc.Container(
        [
            dbc.Row([
                dbc.Col([
                    html.H5('Equity data', className='text-center'),
                    dcc.Dropdown(['S&P', 'FTSE', 'NASDAQ'],
                                 'S&P', id='equity-dropdown'),
                    html.Div(id='equity-dynamic'),
                    html.Hr(),
                ],
                    width={'size': 6, 'offset': 0, 'order': 1}),

                dbc.Col([
                    html.H5('FX', className='text-center'),
                    dcc.Graph(id='EURUSD',
                              figure=get_currency_figure("EURUSD_30d"),
                              style={'height': 585}),
                    html.Hr()
                ], width={'size': 2, 'offset': 0, 'order': 2}),

                dbc.Col([
                    html.H5('GBPUSD', className='text-center'),
                    dcc.Graph(id='GBPUSD',
                              figure=get_currency_figure("GBPUSD_30d"),
                              style={'height': 585}),
                    html.Hr()
                ], width={'size': 2, 'offset': 0, 'order': 3}),

                dbc.Col([
                    html.H5('EURGBP', className='text-center'),
                    dcc.Graph(id='EURGBP', figure=get_currency_figure("EURGBP_30d"),
                              style={'height': 585}),
                    html.Hr()
                ], width={'size': 2, 'offset': 0, 'order': 4}),
            ]),

            dbc.Row([
                dbc.Col([
                    html.H5('Crypto', className='text-center'),
                    dcc.Dropdown(['BTC', 'ETH', 'USDT'],
                                 'BTC', id='crypto-dropdown'),
                    html.Div(id='crypto-dynamic'),
                    html.Hr(),
                ],
                    width={'size': 6, 'offset': 0, 'order': 1}),
            ])
        ], fluid=True)
    return page1_content


@callback(Output('page-content', 'children'), [Input("url", "pathname")])
def display_page_content(pathname):
    # updateData()
    if pathname == '/':
        page_id = 'page1'
        page_content = generate_page1()

    return html.Div([
        sidebar_content,
        html.Div(id=page_id, children=page_content, style=CONTENT_STYLE),
    ])


@callback(Output('equity-dynamic', 'children'), [Input('equity-dropdown', 'value')])
def display_page1_dynamic_equity_content(value):
    figure = None
    if value == 'S&P':
        figure = get_chart("SPY", "SPY")
    elif value == 'FTSE':
        figure = get_chart("^FTSE", "FTSE")
    elif value == 'NASDAQ':
        figure = get_chart("^IXIC", "NASDAQ")

    return dcc.Graph(figure=figure, style={'height': 550})


@callback(Output('crypto-dynamic', 'children'), [Input('crypto-dropdown', 'value')])
def display_page1_dynamic_crypto_content(value):
    figure = None
    if value == 'BTC':
        figure = get_chart("BTC-USD", "BTC")
    elif value == 'ETH':
        figure = get_chart("ETH-USD", "ETH")
    elif value == 'USDT':
        figure = get_chart("USDT-USD", "USDT")

    return dcc.Graph(figure=figure, style={'height': 550})


if __name__ == '__main__':
    app = JupyterDash(__name__, external_stylesheets=[
        dbc.themes.SPACELAB], suppress_callback_exceptions=True)
    app.layout = html.Div([
        dcc.Location(id='url'),
        html.Div(id='page-content')
    ])
    app.run_server(debug=True, port=8080)