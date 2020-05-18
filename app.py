import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dataset 'Loading'

# Load the Olympics Games DataFrame into pandas
df = pd.read_csv('OlympicGames1896to2014.csv',
                 quotechar='"',
                 header=0,
                 delimiter=",")



######## Plot 1 - Gender Representation per Year ######### 
# -- Step 1 -- Define the data
df_GenderPerYear = pd.pivot_table(df, values='Athlete', index=['Year'], columns=['Gender'], aggfunc=len)

# -- Step 2 -- Prepare Data to plot

data_Men = (dict(type='bar',
                     x=df_GenderPerYear.index,
                     y=df_GenderPerYear['Men'],
                     text=df_GenderPerYear['Men'],
                     textposition='auto',
                     name="Men",
                     marker_color="#87CEFA",
                     hovertemplate="Year: <b>%{x}</b><br>"+
                                   "Number of Medals: <b>%{y}</b><br>" +
                                   "Gender: <b>Men</b><br>",
                    )
               )

data_Women = (dict(type='bar',
                     x=df_GenderPerYear.index,
                     y=df_GenderPerYear['Women'],
                     text=df_GenderPerYear['Women'],
                     textposition='auto',
                     name="Women",
                     marker_color="#FFC0CB",
                     hovertemplate="Year: <b>%{x}</b><br>"+
                                   "Number of Medals: <b>%{y}</b><br>" +
                                   "Gender: <b>Women</b><br>",
                    )
               )
    

data_bar =[data_Men,data_Women]
    
    
# Define the Layout
layout_bar = dict(title=dict(text='Number of Medals per Gender'),
                 yaxis=dict(title='Number of Medals', tickfont = dict(size = 9)),
                 xaxis=dict(title="Year", tickfont = dict(size = 9)),
                 )


# -- Step 3 -- Show Figure

# Show the Figure
fig_bar = go.Figure(data=data_bar, layout=layout_bar)
fig_bar.show() 



# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('My First DashBoard'),

    html.Div('Example of html Container'),

    dcc.Graph(
        id='example-graph',
        figure=fig_bar
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
