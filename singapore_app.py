#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import html, dcc
import pymongo
import pandas as pd
import plotly.graph_objs as go
from bson import ObjectId

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://alattridge:2tE3MJaiuggQct6L@cluster0.ifouccc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["SingaporeWeather"]
collection = db["WeatherReadings"]

# Retrieve data from MongoDB and convert it to a DataFrame
data = list(collection.find())
for record in data:
    for key, value in record.items():
        if isinstance(value, ObjectId):
            record[key] = str(value)  # Convert ObjectId to string
df = pd.DataFrame(data)

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Prepare data for bar graph
traces = []
for station_id in df['station_id'].unique():
    station_data = df[df['station_id'] == station_id]
    traces.append(go.Bar(
        x=station_data['station_id'],  # Use station_id for x-axis
        y=station_data['value'],        # Use value for y-axis
        name=f'Station {station_id}'
    ))

# Define the layout
app.layout = html.Div([
    html.H1("Singapore Weather"),
    dcc.Graph(
        id='bar-graph',
        figure={
            'data': traces,
            'layout': {
                'title': 'Weather Readings by Station',
                'barmode': 'group'  # To display bars for different stations side by side
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

