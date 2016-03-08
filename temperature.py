#!/usr/bin/env python
"""reads temperature from relayr mqtt broker and plots on plot.ly."""

import time
import datetime
import json
import yaml

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

from relayr import Client
from relayr.dataconnection import MqttStream

# read config filename
with open('config.yml', 'r') as f:
    config = yaml.load(f)

print(config)

# how often to write to plot.ly in seconds
UPDATE_INTERVALL = config["update_intervall"]

# relayr auth and temperature sensor device
c = Client(token=config["relayr"]["token"])
dev = c.get_device(id=config["relayr"]["deviceid"])

# plot.ly auth
py.sign_in(config["plotly"]["user"], config["plotly"]["apikey"])

# one stream token per trace to be plotted
# https://plot.ly/settings/api
tls.set_credentials_file(stream_ids=config["plotly"]["stream_ids"])

stream_ids = tls.get_credentials_file()['stream_ids']

# plotly: Get first stream token from stream id list
stream_id = stream_ids[0]

# plotly: Make instance of stream id object
stream = go.Stream(
    token=stream_id,  # (!) link stream id to 'token' key
    maxpoints=1880      # (!) keep a max of n pts on screen
)

# setup plotly data
trace1 = go.Scatter(
    x=[],
    y=[],
    mode='lines',
    line=dict(
        shape='spline'
    ),
    stream=stream
)
data = go.Data([trace1])

# Define dictionary of axis style options
axis_style = dict(
    showgrid=False,    # remove grid
    showline=False,    # remove axes lines
    zeroline=False     # remove x=0 and y=0 lines
)

# Add title to layout object
layout = go.Layout(title='temperature',
                   xaxis=go.XAxis(
                       axis_style,   # add style options
                   ), yaxis=go.YAxis(
                       range=[18, 22]
                   ),)

# Make a figure object
fig = go.Figure(data=data, layout=layout)

# (@) Send fig to Plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='temperature')
print('%s' % (unique_url))

# remember last mqtt_callback
last_executed = int(round(time.time()))


def mqtt_callback(topic, payload):
    """execute only every UPDATE_INTERVALL."""
    global last_executed
    now = int(round(time.time()))
    tdelta = now - last_executed

    if tdelta > UPDATE_INTERVALL:
        last_executed = now
        writeToPlotly(payload)


def writeToPlotly(payload):
    """callback function from relayr."""
    parsed_json = json.loads(payload)

    # read temperature and time from relayr json
    temp = parsed_json['readings'][0]['value']
    time = parsed_json['readings'][0]['recorded']

    # convert to human readable time
    human_time = datetime.datetime.fromtimestamp(
        int(time) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print('%s: %s' % (human_time, temp))
    # print('%s %s' % (topic, payload))

    # write to plotly stream
    s.write(dict(x=human_time, y=temp))

# open plotly stream with the stream_id
s = py.Stream(stream_id)
s.open()

# open relayr mqtt connection
stream = MqttStream(mqtt_callback, [dev])
stream.start()

# loop until ctrl-c
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    # close relayr stream
    print('closing relayr stream')
    stream.stop()

    # close plotly stream
    print('closing plotly stream')
    s.close()
