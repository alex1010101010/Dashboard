import pandas as pd
import numpy as np
from datetime import datetime
# from pandas_datareader import data as pdr
from pandas.tseries.offsets import BDay
import yfinance as yf
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash import callback


# Inputs

tickers = ['SPY', '^FTSE', '^IXIC', 'GBPUSD=X', 'GBPEUR=X',
           'EURUSD=X', 'BTC-USD', 'ETH-USD', '^TNX', '^VIX', 'USDT-USD']

data = {}
for i in tickers:
    data[i] = yf.Ticker(i).history(period='3y')['Close']


# Get FX rates
EURUSD_30d = yf.Ticker('EURUSD=X').history(period='30d')['Close']
GBPUSD_30d = yf.Ticker('GBPUSD=X').history(period='30d')['Close']
EURGBP_30d = yf.Ticker('EURGBP=X').history(period='30d')['Close']

# Prepare data series
t1 = pd.Series(EURUSD_30d, name='EURUSD_30d')
t2 = pd.Series(EURUSD_30d, name='GBPUSD_30d')
t3 = pd.Series(EURUSD_30d, name='EURGBP_30d')

# FX calcs
df = pd.concat([t1, t2, t3], axis=1)

monthly_change_EURUSD = df['EURUSD_30d'].iloc[-1]/df['EURUSD_30d'].iloc[0]-1
monthly_change_GBPUSD = df['GBPUSD_30d'].iloc[-1]/df['GBPUSD_30d'].iloc[0]-1
monthly_change_EURGBP = df['EURGBP_30d'].iloc[-1]/df['EURGBP_30d'].iloc[0]-1

two_week_change_EURUSD = df['EURUSD_30d'].iloc[-1]/df['EURUSD_30d'].iloc[14]-1
two_week_change_GBPUSD = df['GBPUSD_30d'].iloc[-1]/df['GBPUSD_30d'].iloc[14]-1
two_week_change_EURGBP = df['EURGBP_30d'].iloc[-1]/df['EURGBP_30d'].iloc[14]-1


one_week_change_EURUSD = df['EURUSD_30d'].iloc[-1]/df['EURUSD_30d'].iloc[7]-1
one_week_change_GBPUSD = df['GBPUSD_30d'].iloc[-1]/df['GBPUSD_30d'].iloc[7]-1
one_week_change_EURGBP = df['EURGBP_30d'].iloc[-1]/df['EURGBP_30d'].iloc[7]-1

latest_EURUSD = float("{:.2f}".format(df['EURUSD_30d'][-1]))
latest_GBPUSD = float("{:.2f}".format(df['GBPUSD_30d'][-1]))
latest_EURGBP = float("{:.2f}".format(df['EURGBP_30d'][-1]))

# TODO:Need to provide dates

internal_dates = t1.index

# SPY

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_SPY = go.Figure()
chart_SPY.add_trace(go.Scatter(x=data['SPY'].index, y=data['SPY'],
                    mode='lines',  # you can also use "lines+markers", or just "markers"
                    name='SPY'))

chart_SPY.layout.template = CHART_THEME
chart_SPY.layout.height = 500
# this will help you optimize the chart space
chart_SPY.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_SPY.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))



# FTSE

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_FTSE = go.Figure()
chart_FTSE.add_trace(go.Scatter(x=data['^FTSE'].index, y=data['^FTSE'],
                                mode='lines',  # you can also use "lines+markers", or just "markers"
                                name='FTSE'))

chart_FTSE.layout.template = CHART_THEME
chart_FTSE.layout.height = 500
# this will help you optimize the chart space
chart_FTSE.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_FTSE.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))


# NASDAQ

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_NASDAQ = go.Figure()
chart_NASDAQ.add_trace(go.Scatter(x=data['^IXIC'].index, y=data['^IXIC'],
                                  mode='lines',  # you can also use "lines+markers", or just "markers"
                                  name='NASDAQ'))

chart_NASDAQ.layout.template = CHART_THEME
chart_NASDAQ.layout.height = 500
# this will help you optimize the chart space
chart_NASDAQ.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_NASDAQ.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))


# BTC

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_BTC = go.Figure()
chart_BTC.add_trace(go.Scatter(x=data['BTC-USD'].index, y=data['BTC-USD'],
                    mode='lines',  # you can also use "lines+markers", or just "markers"
                    name='BTC'))

chart_BTC.layout.template = CHART_THEME
chart_BTC.layout.height = 500
# this will help you optimize the chart space
chart_BTC.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_BTC.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))



chart_USDT = go.Figure()
chart_USDT.add_trace(go.Scatter(x=data['USDT-USD'].index, y=data['USDT-USD'],
                                mode='lines',  # you can also use "lines+markers", or just "markers"
                                name='BTC'))

chart_USDT.layout.template = CHART_THEME
chart_USDT.layout.height = 500
# this will help you optimize the chart space
chart_USDT.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_USDT.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))


# ETH

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_ETH = go.Figure()
chart_ETH.add_trace(go.Scatter(x=data['ETH-USD'].index, y=data['ETH-USD'],
                    mode='lines',  # you can also use "lines+markers", or just "markers"
                    name='ETH'))

chart_ETH.layout.template = CHART_THEME
chart_ETH.layout.height = 500
# this will help you optimize the chart space
chart_ETH.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_ETH.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))

# VIX

CHART_THEME = 'plotly_white'  # others include seaborn, ggplot2, plotly_dark

chart_VIX = go.Figure()
chart_VIX.add_trace(go.Scatter(x=data['^VIX'].index, y=data['^VIX'],
                    mode='lines',  # you can also use "lines+markers", or just "markers"
                    name='VIX'))

chart_VIX.layout.template = CHART_THEME
chart_VIX.layout.height = 500
# this will help you optimize the chart space
chart_VIX.update_layout(margin=dict(t=50, b=50, l=25, r=25))
chart_VIX.update_layout(
    #     title='Business indicators (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))


# EURUSD

EURUSD = go.Figure()
EURUSD.layout.template = CHART_THEME

EURUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(one_week_change_EURUSD*100)),
    number={'suffix': " %"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 0, 'column': 0}))


EURUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(two_week_change_EURUSD*100)),
    number={'suffix': " %"},
    title={"text": "<span style='font-size:0.7em;color:gray'>15 Days</span>"},
    delta={'position': "bottom", 'reference': 0, 'relative': False},
    domain={'row': 1, 'column': 0}))


EURUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(monthly_change_EURUSD*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>30 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 2, 'column': 0}))

EURUSD.update_layout(
    grid={'rows': 3, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)


# GBPUSD

GBPUSD = go.Figure()
GBPUSD.layout.template = CHART_THEME

GBPUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(one_week_change_GBPUSD*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 0, 'column': 0}))

GBPUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(two_week_change_GBPUSD*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>15 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 1, 'column': 0}))


GBPUSD.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(monthly_change_GBPUSD*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>30 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 2, 'column': 0}))

GBPUSD.update_layout(
    grid={'rows': 3, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)

# EURGBP

EURGBP = go.Figure()
EURGBP.layout.template = CHART_THEME

EURGBP.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(one_week_change_EURGBP*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>7 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 0, 'column': 0}))

EURGBP.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(two_week_change_EURGBP*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>15 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 1, 'column': 0}))


EURGBP.add_trace(go.Indicator(
    mode="number+delta",
    value=float("{:.2f}".format(monthly_change_EURGBP*100)),
    number={'suffix': "%"},
    title={"text": "<br><span style='font-size:0.7em;color:gray'>30 Days</span>"},
    delta={'position': "bottom", 'reference': 0.02, 'relative': False},
    domain={'row': 2, 'column': 0}))

EURGBP.update_layout(
    grid={'rows': 3, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)



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


page1_content = dbc.Container(
    [
                # dbc.Row(dbc.Col(html.H2('OVERVIEW', className='text-center text-primary, mb-3'))),
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
                          figure=EURUSD,
                          style={'height': 585}),
                html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 2}),

            dbc.Col([
                html.H5('GBPUSD', className='text-center'),
                dcc.Graph(id='GBPUSD',
                          figure=GBPUSD,
                          style={'height': 585}),
                html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 3}),

            dbc.Col([
                html.H5('EURGBP', className='text-center'),
                dcc.Graph(id='EURGBP', figure=EURGBP, style={'height': 585}),
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

            dbc.Col([
                html.H5('VIX', className='text-center'),
                dcc.Graph(id='VIX', figure=chart_VIX, style={'height': 585}),
                # html.Div(id='crypto-dynamic'),
                html.Hr(),
            ],
                width={'size': 6, 'offset': 0, 'order': 1}),

        ]),


    ], fluid=True)



@callback(Output('page-content', 'children'), [Input("url", "pathname")])
def display_page_content(pathname):
    if pathname == '/':
        page_id = 'page1'
        page_content = page1_content


    return html.Div([
        sidebar_content,
        html.Div(id=page_id, children=page_content, style=CONTENT_STYLE),
    ])


@callback(Output('equity-dynamic', 'children'), [Input('equity-dropdown', 'value')])
def display_page1_dynamic_equity_content(value):

    figure = None
    if value == 'S&P':
        figure = chart_SPY
    elif value == 'FTSE':
        figure = chart_FTSE
    elif value == 'NASDAQ':
        figure = chart_NASDAQ

    return dcc.Graph(figure=figure, style={'height': 550})


@callback(Output('crypto-dynamic', 'children'), [Input('crypto-dropdown', 'value')])
def display_page1_dynamic_crypto_content(value):
    figure = None
    if value == 'BTC':
        figure = chart_BTC
    elif value == 'ETH':
        figure = chart_ETH
    elif value == 'USDT':
        figure = chart_USDT

    return dcc.Graph(figure=figure, style={'height': 550})


if __name__ == '__main__':
    app = JupyterDash(__name__, external_stylesheets=[
                      dbc.themes.SPACELAB], suppress_callback_exceptions=True)
    app.layout = html.Div([
        dcc.Location(id='url'),
        html.Div(id='page-content')
    ])

    app.run_server(debug=True, port=8080)

