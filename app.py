# -------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------- Import Packages ------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# -------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------- Dataset Loading ------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#

# Load the Olympics Games DataFrame into pandas

path = 'https://raw.githubusercontent.com/HugodaSilva/DVizProject_OlympicGames_GenderRepresentation/master/'
df = pd.read_csv(path + 'OlympicGames1896to2014.csv',
                 quotechar='"',
                 header=0,
                 delimiter=",")

# -------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------ Filters definition -----------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#


country_options = [dict(label=country.replace('_', ' '), value=country) for country in
                   sorted(df['Country_Name'].unique())]

dropdown_country = dcc.Dropdown(
    id='country_drop',
    options=country_options,
    value=[],
    multi=True
)

# create years dict
years_select = {str(i): '{}'.format(str(i)) for i in df['Year'].unique()}
years_select[str(1892)] = "All"

# -------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------- APP -----------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Img(
                src="assets/Olympic_Rings.png",
                alt="Olympic Games logo",
                id="logo",
                width="55%",
                height="55%",
            ),
        ],style={'width':'20%','height':'20%','vertical-align': 'middle','horizontal-align': 'middle'}),
        html.Div([
            html.H1(
                'Mind the gap: the underrepresentation of female athletes in Olympic Games (1896 to 2014)'
            ),
        ],style={'width':'85%'}),
    ],style={'display':'flex'}),

    html.Br(),

    html.Div([
        html.Div([
            html.H4(
                'Filters Menu'
            ),
        ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'middle'}),

        html.Br(),

        html.Div([
            html.Label('Country Choice'),
            dropdown_country,


        ],style={'width':'50%','display': 'inline-block'}),

        html.Br(),
        html.Br(),

        html.Div([
            html.Label('Year Slider'),
            html.Div([
                dcc.RangeSlider(
                    id='year_slider',
                    min=1896,
                    max=2014,
                    value=[1896, 2014],
                    marks={'1896' : '1896',
                            '1900' : '1900',
                            '1904' : '1904',
                            '1908' : '1908',
                            '1912' : '1912',
                            '1920' : '1920',
                            '1924' : '1924',
                            '1928' : '1928',
                            '1932' : '1932',
                            '1936' : '1936',
                            '1948' : '1948',
                            '1952' : '1952',
                            '1956' : '1956',
                            '1960' : '1960',
                            '1964' : '1964',
                            '1968' : '1968',
                            '1972' : '1972',
                            '1976' : '1976',
                            '1980' : '1980',
                            '1984' : '1984',
                            '1988' : '1988',
                            '1992' : '1992',
                            '1994' : '1994',
                            '1996' : '1996',
                            '1998' : '1998',
                            '2000' : '2000',
                            '2002' : '2002',
                            '2004' : '2004',
                            '2006' : '2006',
                            '2008' : '2008',
                            '2010' : '2010',
                            '2012' : '2012',
                            '2014' : '2014',},
                    step=None
                )
            ], id='slider'),
            html.Br(),
        ],style={'width':'100%','display': 'inline-block'}),
    ], className='box'),


    html.Div([
        html.Div([
            html.H4('After more than 100 years, gender equality is still more goal than reality'),
            'Use the Filter Menu to find the gap between men and women Olympic medalists',
        ]),

        html.Div([
            html.Div([
                dcc.Graph(id='Gender_Percentage')
            ],style={'width':'25%'}),
            html.Br(),

            html.Div([
                dcc.Graph(id='Gender_Year')
            ],style={'width':'75%'}),
            html.Br(),
        ],style={'display':'flex'})
    ],className='box'),

    html.Div([
        html.Div([
            html.H4('Women have not always been allowed to participate in the Olympic Games. '),
             'No women participated in Athens in 1896;  Women competed in 1900. Until 2014 not all sports had female or mixed categories (Baseball is the exception)',
        ]),

        html.Div([
            dcc.Graph(id='Gender_Participation'),
        ]),
    ],className='box'),
    html.Br(),

    html.Div([
        html.Div([
            'NOVA IMS | Data Visualisation | Spring Semester 2019-2020'
            ], style={'text-align': 'center'}),
        html.Div([
            'Professors: Pedro Cabral | Nuno Alpalhão'
        ], style={'text-align': 'center'}),
        html.Div([
            'Group: Anabell Gongora M20180349 | Hugo Silva M20190973 | Joana Ribeiro M20190459 | Liliana Nogueira M20190835'
        ], style={'text-align': 'center'}),
    ],className='box'),

])


@app.callback([
    Output('Gender_Percentage', 'figure'),
    Output('Gender_Year', 'figure'),
    Output('Gender_Participation', 'figure')
],
    [
        Input("year_slider", "value"),
        Input("country_drop", "value"),
    ]
)
# -------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------- Plots Creation -------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#

def update_graphs(year,country):
    # define dataset to Plot
    df_baseline = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    if  country == []:
        df_baseline = df_baseline.copy()
    elif country != []:
        df_baseline = df_baseline[df_baseline['Country_Name'].isin(country)].copy()

    #################################################################
    ######## Plot 1  - Gender Representation Olympic Games ##########
    #################################################################
    # Define the labels
    label_Gender = df_baseline["Gender"].value_counts().keys().tolist()
    # Define the values
    value_Gender = df_baseline["Gender"].value_counts().values.tolist()

    # Define the data to plot
    data_Gender = dict(type='pie', labels=label_Gender, values=value_Gender, marker_colors=['#87CEFA', '#FFC0CB'],
                       hole=0.60)

    layout_Gender = dict(title=dict(text='Gender Percentage in Olympic Games')
                         )

    # Show Figure
    fig_Gender_Percentage = go.Figure(data=[data_Gender], layout=layout_Gender)

    #################################################################
    ########## Plot 2  - Gender Representation per Year #############
    #################################################################
    # -- Step 1 -- Define the data
    df_GenderPerYear = pd.pivot_table(df_baseline, values="Athlete", index=["Year"], columns=["Gender"], aggfunc=len)

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
    fig_Gender_Year = go.Figure(data=data_bar, layout=layout_bar)

    #################################################################
    ###### Plot 3  - Gender Participantion per Sport per Year #######
    #################################################################

    # -- Step 1 -- Define the data
    # - Step 1.1 - Women data
    df_Plot_Woman = pd.pivot_table(df[df['Gender'] == "Women"], values='Medal', index=['Year'], columns=['Sport'],
                                   aggfunc=len, dropna=False)
    df_Plot_Woman[df_Plot_Woman > 0] = 2
    df_Plot_Woman[np.isnan(df_Plot_Woman)] = 1
    df_Plot_Men = pd.pivot_table(df[df['Gender'] == "Men"], values='Medal', index=['Year'], columns=['Sport'],
                                 aggfunc=len)

    # - Step 1.2 - Men data
    df_Plot_Men[df_Plot_Men > 0] = 3
    df_Plot_Men[np.isnan(df_Plot_Men)] = 1

    # - Step 1.3 - Multipli Men and Women data
    df_Sport_Year = df_Plot_Men * df_Plot_Woman

    # - Step 1.4 - Check Missing Values
    df_Sport_Year[np.isnan(df_Sport_Year)] = df_Plot_Men
    df_Sport_Year[np.isnan(df_Sport_Year)] = df_Plot_Woman
    df_Sport_Year[df_Sport_Year == 1] = 0

    # - Step 1.5 - Set the scale
    df_Sport_Year.replace(0, np.nan, inplace=True)
    df_Sport_Year.replace(6, 1, inplace=True)
    df_Sport_Year.replace(3, 0.5, inplace=True)
    df_Sport_Year.replace(2, 0.25, inplace=True)
    df_Plot = df_Sport_Year.T

    # - Step 1.6 - Change data for the hover
    df_Sport_Year_Name = df_Sport_Year.T
    df_Sport_Year_Name.replace(np.nan, "None", inplace=True)
    df_Sport_Year_Name.replace(1, "Both", inplace=True)
    df_Sport_Year_Name.replace(0.5, "Men", inplace=True)
    df_Sport_Year_Name.replace(0.25, "Women", inplace=True)

    # -- Step 2 -- Prepare Data to plot

    # Define the Values of the Heatmap
    y_corr = df_Plot.index
    x_corr = df_Plot.columns
    z_corr = df_Plot
    custom = df_Sport_Year_Name

    data_corr = dict(type='heatmap',
                     x=x_corr,
                     y=y_corr,
                     z=z_corr,
                     customdata=custom,
                     colorscale=[[0, '#FFC0CB'], [0.33, '#FFC0CB'], [0.33, '#87CEFA'], [0.66, '#87CEFA'],
                                 [0.66, '#c3e4a1'], [1, '#c3e4a1']],
                     hovertemplate="Column: <b>%{x}</b><br>" +
                                   "Line: <b>%{y}</b><br>" +
                                   "Played by: <b>%{customdata}</b><br>",
                     colorbar=dict(tickmode="array", tickvals=[0.25, 0.5, 0.75], ticktext=["Women", "Men", "Mixed"])
                     )

    layout_corr = dict(title="Sports played per Gender",
                       autosize=False,
                       height=800,
                       width=800,
                       yaxis=dict(tickfont=dict(size=9)),
                       xaxis=dict(tickfont=dict(size=9))
                       )
    # -- Step 3 -- Show Figure

    # Show the Figure
    fig_Gender_Participation = go.Figure(data=data_corr, layout=layout_corr)

    return fig_Gender_Percentage, fig_Gender_Year, fig_Gender_Participation


if __name__ == '__main__':
    app.run_server(debug=True)
