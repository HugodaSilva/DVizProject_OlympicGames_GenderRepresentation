import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Dataset 'Loading'

# Load the Olympics Games DataFrame into pandas

path = 'https://raw.githubusercontent.com/HugodaSilva/DVizProject_OlympicGames_GenderRepresentation/master/'

df = pd.read_csv(path + 'OlympicGames1896to2014.csv',
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
                 hovertemplate="Year: <b>%{x}</b><br>" +
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
                   hovertemplate="Year: <b>%{x}</b><br>" +
                                 "Number of Medals: <b>%{y}</b><br>" +
                                 "Gender: <b>Women</b><br>",
                   )
              )

data_bar = [data_Men, data_Women]

# Define the Layout
layout_bar = dict(title=dict(text='Number of Medals per Gender'),
                  yaxis=dict(title='Number of Medals', tickfont=dict(size=9)),
                  xaxis=dict(title="Year", tickfont=dict(size=9)),
                  )

# -- Step 3 -- Show Figure

# Show the Figure
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

######## Plot 2 - Gender Representation Olympic Games #########
# Define the labels
label_Gender = df["Gender"].value_counts().keys().tolist()

# Define the values
value_Gender = df["Gender"].value_counts().values.tolist()

# Define the data to plot
data_Gender = dict(type='pie', labels=label_Gender, values=value_Gender, marker_colors=['#87CEFA', '#FFC0CB'],
                   hole=0.60)

layout_Gender = dict(title=dict(text='Gender Percentage in Olympic Games')
                     )

# Show Figure
fig_Gender = go.Figure(data=[data_Gender], layout=layout_Gender)


######## Plot 3 - Gender Representation Olympic Games per Year and Sport #########
# -- Step 1 -- Define the data
df_Plot_Woman = pd.pivot_table(df[df['Gender']=="Women"], values='Medal', index=['Year'], columns=['Sport'], aggfunc=len,dropna=False)
df_Plot_Woman[df_Plot_Woman>0]=2
df_Plot_Woman[np.isnan(df_Plot_Woman)] = 1
df_Plot_Men = pd.pivot_table(df[df['Gender']=="Men"], values='Medal', index=['Year'], columns=['Sport'], aggfunc=len)
df_Plot_Men[df_Plot_Men>0]=3
df_Plot_Men[np.isnan(df_Plot_Men)] = 1
df_Sport_Year=df_Plot_Men*df_Plot_Woman
df_Sport_Year[np.isnan(df_Sport_Year)]=df_Plot_Men
df_Sport_Year[np.isnan(df_Sport_Year)]=df_Plot_Woman
df_Sport_Year[df_Sport_Year==1]=0
df_Plot=df_Sport_Year.T
df_Sport_Year.replace(0,np.nan, inplace=True)
df_Sport_Year.replace(6,1, inplace=True)
df_Sport_Year.replace(3,0.5, inplace=True)
df_Sport_Year.replace(2,0.25, inplace=True)

# -- Step 2 -- Prepare Data to plot

# Define the Values of the Heatmap
y_corr = df_Plot.index
x_corr = df_Plot.columns
z_corr = df_Plot

data_corr = dict(type='heatmap',
                 x=x_corr,
                 y=y_corr,
                 z=z_corr,
                 colorscale=[[0, '#FFC0CB'], [0.33, '#FFC0CB'],[0.33, '#87CEFA'],[0.66, '#87CEFA'],[0.66,'#c3e4a1'],[1,'#c3e4a1']],
                 hovertemplate="Column: <b>%{x}</b><br>" +
                                "Line: <b>%{y}</b><br>"+
                                "Played by: <b>%{z}</b><br>",
                )

layout_corr = dict(title = "Sports played per Gender",
                        autosize = False,
                        height  = 800,
                        width   = 800,
                        yaxis   = dict(tickfont = dict(size = 9)),
                        xaxis   = dict(tickfont = dict(size = 9))
                  )
# -- Step 3 -- Show Figure

# Show the Figure
fig_corr = go.Figure(data=data_corr,layout=layout_corr)



# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.Div(
            html.Img(
                src=app.get_asset_url("Olympic_Rings.png"),
                alt="Olympic Ganmes logo",
                id="logo",
                width="20%",
                height="20%",
            ),
        ),
        html.Div(
            html.H1('Mind the gap: the underrepresentation of female athletes in Olympic Games (1896 to 2014)'),
        ),
    ]),

    html.Div('Number of Medals per Gender'),

        dcc.Graph(
            id='Number of Medals per Gender',
            figure=fig_bar
        ),

        html.Br(),

        dcc.Graph(
            id='Gender Percentage in Olympic Games',
            figure=fig_Gender
        ),

        html.Br(),

        dcc.Graph(
            id='Gender Representation Olympic Games per Year and Sport',
            figure=fig_corr
        )
])

if __name__ == '__main__':
    app.run_server(debug=True)
