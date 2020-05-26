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
html.Div([ # DIV A - LEFT COLUMN
        html.Div([ # Div A1 - Logo and Text
            html.Div([ # Div A1.1 - Logo
                html.Img(
                    src="assets/Olympic_Rings.png",
                    alt="Olympic Games logo",
                    id="logo",
                    width="100%",
                    height="100%",
                ),
            ],style={'vertical-align': 'middle','horizontal-align': 'middle'}),# End Div A1.1
            html.Div([ # Div A1.2 - Text
                html.Div(['More than 35,000 medals have been awarded at the Olympics since 1896.'
                        ], style={'text-align': 'center','font-size':'0.8em', 'color':'gray'}),
                html.Div(['The information in this visualisation contains every Olympic athlete that has won a medal since the first games.'
                        ], style={'text-align': 'center', 'font-size': '0.8em', 'color': 'gray'}),
            ],),# End Div A1.2
        ],),

        html.Br(),

        html.Div([  # Div A2 - Indicator Cards
            html.Div([ # Div A2.1 - Number of Countries
                html.Div('Number of Countries', style={"font-size": 15, "font-weight": "bold"}),
                html.Br(),
                html.Div('Total', style={"font-size": 14}),
                dcc.Loading(html.Div([html.H4("...")], id="N_Country_Total_Filter",
                                     style={"font-size": 16, "font-weight": "bold", 'color': 'grey'})),
                html.Div([
                    html.Div([
                        html.Div('Men', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Country_Gender_Men_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#87CEFA'})),
                    ], style={'width': '50%'}),
                    html.Div([
                        html.Div('Women', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Country_Gender_Women_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#FFC0CB'})),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex'}),
                    html.Br(),
                    html.Div([
                        'Number of countries with Olympic medalists split by Gender. '
                    
                    ], style={'text-align': 'left', 'font-size': '0.5em', 'color': 'gray'}),
            ], className='box',
                style={'text-align': 'center', 'vertical-align': 'middle', 'horizontal-align': 'middle'}), # End Div A2.1


            html.Div([ # Div A2.2 - Number of Athletes
                html.Div('Number of Athletes', style={"font-size": 15, "font-weight": "bold"}),
                html.Br(),
                html.Div('Total', style={"font-size": 14}),
                dcc.Loading(html.Div([html.H4("...")], id="N_Athletes_Total_Filter",
                                     style={"font-size": 16, "font-weight": "bold", 'color': 'grey'})),
                html.Div([
                    html.Div([
                        html.Div('Men', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Athletes_Gender_Men_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#87CEFA'})),
                    ], style={'width': '50%'}),
                    html.Div([
                        html.Div('Women', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Athletes_Gender_Women_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#FFC0CB'})),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex'}),
                html.Br(),
                html.Div([
                    'Number of Olympic medalists & Olympic medalists split by Gender. '                  
                ], style={'text-align': 'left', 'font-size': '0.5em', 'color': 'gray'}),
            ], className='box',
                style={'text-align': 'center', 'vertical-align': 'middle', 'horizontal-align': 'middle'}), # End Div A2.2


            html.Div([ # Div A2.3 - Number of Sports
                html.Div('Number of Sports', style={"font-size": 15, "font-weight": "bold"}),
                html.Br(),
                html.Div('Total', style={"font-size": 14}),
                dcc.Loading(html.Div([html.H4("...")], id="N_Sports_Total_Filter",
                                     style={"font-size": 16, "font-weight": "bold", 'color': 'grey'})),
                html.Div([
                    html.Div([
                        html.Div('Men', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Sports_Gender_Men_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#87CEFA'})),
                    ], style={'width': '50%'}),
                    html.Div([
                        html.Div('Women', style={"font-size": 14}),
                        dcc.Loading(html.Div([html.H6("...")], id="N_Sports_Gender_Women_Filter",
                                             style={"font-size": 16, "font-weight": "bold", 'color': '#FFC0CB'})),
                    ], style={'width': '50%'}),
                ], style={'display': 'flex'}),
                html.Br(),
                html.Div([
                    'Olympic medalists by Sport & split by Gender.'
                ], style={'text-align': 'left', 'font-size': '0.5em', 'color': 'gray'}),
            ], className='box',
                style={'text-align': 'center', 'vertical-align': 'middle', 'horizontal-align': 'middle'}), # End Div A2.3
        ],style={'display':'flex', 'flex-direction': 'column'}), # End Div A2
    ],className='column_1'), # End DIV A


    html.Div([ # DIV B - RIGHT COLUMN
        html.Div([  # Div B1 - Title and SubTitle
            html.Div([ # Div B1.1 - Title
                html.H1('Do the Olympic Games have a gender gap?'),
            ], style={'text-align': 'center', 'color':'#4c8bf5'}), # End Div B1.1
            html.Div([ # Div B1.2 - SubTitle
                html.H3('Olympic Medals as a medium to understand the underrepresentation of female athletes in the Olympics (1896 to 2014)'),
            ], style={'text-align': 'center', 'color':'#4c8bf5'}), # End Div B1.2
        ],), # End Div B1

        html.Div([ # Div B2 - Filters Menu
            html.Div([ # Div B2.1 - Title
                html.H4('Filters Menu'),
            ], style={'width': '80%', 'display': 'inline-block', 'vertical-align': 'middle'}), # End Div B2.1

            html.Br(),

            html.Div([ # Div B2.2 - Country Dropdown
                html.Label('Country Choice'),
                dropdown_country,
            ],style={'width':'50%','display': 'inline-block'}),# End Div B2.2

            html.Br(),
            html.Br(),

            html.Div([ # Div B2.3 - Year Slider
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
                                '1992' : '',
                                '1994' : '1994',
                                '1996' : '',
                                '1998' : '1998',
                                '2000' : '',
                                '2002' : '2002',
                                '2004' : '',
                                '2006' : '2006',
                                '2008' : '',
                                '2010' : '2010',
                                '2012' : '',
                                '2014' : '2014',},
                        step=None
                    )
                ], id='slider'),
                html.Br(),
            ],style={'width':'100%','display': 'inline-block'}), # End Div B2.3
        ], className='box'), # End Div B2


        html.Div([ # Div B3 - Gender Percentage
            html.Div([ # Div B3.1 - Title
                html.H3('The gap'),
                html.H5('More than 100 years later, gender equality is still not a reality in the Olympic Games.'),
                        'Use the Filter Menu and hover over the graphs to find the gap between men and women Olympic medalists',
            ]),# End Div B3.1

            html.Div([  # Div B3.2 - Graphs
                html.Div([  # Div B3.2.1 - Pie Chart
                    dcc.Loading(dcc.Graph(id='Gender_Percentage'))
                ], style={'width': '30%'}),  # End Div B3.2.1
                html.Br(),

                html.Div([  # Div B3.2.2 - Bar Chart
                    dcc.Loading(dcc.Graph(id='Gender_Year'))
                ], style={'width': '70%'}),  # End Div B3.2.2
                html.Br(),
            ], style={'display': 'flex'})  # End Div B3.2
        ], className='box'),  # End Div B3


        html.Div([ # Div B4 - Gender Participation
            html.Div([ # Div B4.1 - Title
                html.H3('The changing path'),
                html.H5('Women have not always been allowed to participate in the Olympic Games. '),
                 'No women participated in Athens in 1896;  Women competed in 1900. Until 2010 not all sports had female or mixed categories',
            ]),# End Div B4.1

            html.Div([ # Div B4.2 -Stacked 100%
                dcc.Graph(id='Gender_Swap'),
            ],style={'text-align': 'center', 'vertical-align': 'middle', 'horizontal-align': 'middle'}),# End Div B4.2

            html.Div([  # Div B4.3 - Heatmap
                dcc.Graph(id='Gender_Participation'),
            ],style={'text-align': 'center', 'vertical-align': 'middle', 'horizontal-align': 'middle'}),  # End Div B4.3
        ],className='box'), # End Div B4
        html.Br(),

        html.Div([ # Div B5 - Footer
            html.Div([ # Div B5.1 - School
                'NOVA IMS | Data Visualisation | Spring Semester 2019-2020'
                ], style={'text-align': 'center','font-size':'0.8em', 'color':'gray'}), # End Div B5.1
            html.Div([ # Div B5.2 - Professors
                'Professors: Pedro Cabral | Nuno Alpalhão'
            ], style={'text-align': 'center','font-size':'0.8em', 'color':'gray'}), # End Div B5.2
            html.Div([ # Div B5.3 - Group
                'Group: Anabell Gongora M20180349 | Hugo Silva M20190973 | Joana Ribeiro M20190459 | Liliana Nogueira M20190835'
            ], style={'text-align': 'center','font-size':'0.8em', 'color':'gray'}), # End Div B5.3
        ],className='box'), # End Div B5
    ],className='column_2'), # end DIV B

], style={'display':'flex'})



# -------------------------------------------------------------------------------------------------------------------#
# -------------------------------------------- Plots Creation -------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------------------#

@app.callback([
    Output('N_Country_Total_Filter','children'),
    Output('N_Country_Gender_Men_Filter','children'),
    Output('N_Country_Gender_Women_Filter','children'),
    Output('N_Athletes_Total_Filter', 'children'),
    Output('N_Athletes_Gender_Men_Filter', 'children'),
    Output('N_Athletes_Gender_Women_Filter', 'children'),
    Output('N_Sports_Total_Filter', 'children'),
    Output('N_Sports_Gender_Men_Filter', 'children'),
    Output('N_Sports_Gender_Women_Filter', 'children'),
    Output('Gender_Percentage', 'figure'),
    Output('Gender_Year', 'figure'),
    Output('Gender_Participation', 'figure'),
    Output('Gender_Swap', 'figure')
],
    [
        Input("year_slider", "value"),
        Input("country_drop", "value"),
    ]
)

def update_graphs(year,country):

# ___________________________________________________________________________________________________________________#
#                                     Filter Data acording to the user inputs
# ___________________________________________________________________________________________________________________#

    # -- Step 1 - Filter Dataframe
    df_baseline = df[(df['Year'] >= year[0]) & (df['Year'] <= year[1])]

    if  country == []:
        df_baseline = df_baseline.copy()
    elif country != []:
        df_baseline = df_baseline[df_baseline['Country_Name'].isin(country)].copy()

# ___________________________________________________________________________________________________________________#
#                                               Define the Graphs
# ___________________________________________________________________________________________________________________#

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                   Indicators 1  - Number of Countries
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot
    N_Country_Total_Filter = df_baseline['Country_Name'].nunique()
    N_Country_Gender_Filter = pd.pivot_table(df_baseline, values='Medal', index=['Country_Name'], columns=['Gender'],
                                              aggfunc=len,
                                              dropna=False)
    N_Country_Gender_Split_Filter = N_Country_Gender_Filter.count()
    if len(N_Country_Gender_Split_Filter) == 2:
        N_Country_Gender_Men_Filter = N_Country_Gender_Split_Filter['Men']
        N_Country_Gender_Women_Filter = N_Country_Gender_Split_Filter['Women']
    elif N_Country_Gender_Split_Filter.index == 'Men':
        N_Country_Gender_Men_Filter = N_Country_Gender_Split_Filter['Men']
        N_Country_Gender_Women_Filter = 0
    elif N_Country_Gender_Split_Filter.index == 'Women':
        N_Country_Gender_Women_Filter = N_Country_Gender_Split_Filter['Women']
        N_Country_Gender_Men_Filter = 0
    else:
        N_Country_Gender_Men_Filter = 0
        N_Country_Gender_Women_Filter = 0



#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                   Indicators 2  - Number of Countries
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot
    N_Athletes_Total_Filter = df_baseline['Athlete'].nunique()
    N_Athletes_Gender_Filter = pd.pivot_table(df_baseline, values='Medal', index=['Athlete'], columns=['Gender'],
                                              aggfunc=len,
                                              dropna=False)
    N_Athletes_Gender_Split_Filter = N_Athletes_Gender_Filter.count()
    if len(N_Athletes_Gender_Split_Filter) == 2:
        N_Athletes_Gender_Men_Filter = N_Athletes_Gender_Split_Filter['Men']
        N_Athletes_Gender_Women_Filter = N_Athletes_Gender_Split_Filter['Women']
    elif N_Athletes_Gender_Split_Filter.index == 'Men':
        N_Athletes_Gender_Men_Filter = N_Athletes_Gender_Split_Filter['Men']
        N_Athletes_Gender_Women_Filter = 0
    elif N_Athletes_Gender_Split_Filter.index == 'Women':
        N_Athletes_Gender_Women_Filter = N_Athletes_Gender_Split_Filter['Women']
        N_Athletes_Gender_Men_Filter = 0
    else:
        N_Athletes_Gender_Men_Filter = 0
        N_Athletes_Gender_Women_Filter = 0



# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                   Indicators 3  - Number of Sports
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot
    N_Sports_Total_Filter = df_baseline['Sport'].nunique()
    N_Sports_Gender_Filter = pd.pivot_table(df_baseline, values='Medal', index=['Sport'], columns=['Gender'],
                                              aggfunc=len,
                                              dropna=False)
    N_Sports_Gender_Split_Filter = N_Sports_Gender_Filter.count()
    if len(N_Sports_Gender_Split_Filter) == 2:
        N_Sports_Gender_Men_Filter = N_Sports_Gender_Split_Filter['Men']
        N_Sports_Gender_Women_Filter = N_Sports_Gender_Split_Filter['Women']
    elif N_Sports_Gender_Split_Filter.index == 'Men':
        N_Sports_Gender_Men_Filter = N_Sports_Gender_Split_Filter['Men']
        N_Sports_Gender_Women_Filter = 0
    elif N_Sports_Gender_Split_Filter.index == 'Women':
        N_Sports_Gender_Women_Filter = N_Sports_Gender_Split_Filter['Women']
        N_Sports_Gender_Men_Filter = 0
    else:
        N_Sports_Gender_Men_Filter = 0
        N_Sports_Gender_Women_Filter = 0


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                        Plot 1  - Gender Representation Olympic Games
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot

    # Define the labels
    label_Gender = df_baseline["Gender"].value_counts().keys().tolist()
    # Define the values
    value_Gender = df_baseline["Gender"].value_counts().values.tolist()

    Error_Message = 0
    data_Gender = dict(type='pie', labels=label_Gender, values=value_Gender, marker_colors=['#87CEFA', '#FFC0CB'],
                       hole=0.60)

    if value_Gender == []:
        Error_Message = 1

    if Error_Message != 1:
        layout_Gender = dict(title=dict(text='Gender Percentage')
                             )
    else:
        layout_Gender = dict(title=dict(text='Gender Percentage'),
                             yaxis=dict(visible=False),
                             xaxis=dict(visible=False),
                             annotations=[dict(text='No matching data found',
                                               xref="paper",
                                               yref="paper",
                                               showarrow=False,
                                               font=dict(size=12))
                                          ]
                             )

    # -- Step 3 - Plot the Figure
    fig_Gender_Percentage = go.Figure(data=[data_Gender], layout=layout_Gender)


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                        Plot 2  - Gender Representation per Year
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot

    df_GenderPerYear = pd.pivot_table(df_baseline, values="Athlete", index=["Year"], columns=["Gender"], aggfunc=len)

    Error_Message = 0
    if len(df_GenderPerYear.columns) == 2:
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

    elif df_GenderPerYear.columns == 'Men':
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
        data_bar = data_Men

    elif df_GenderPerYear.columns == 'Women':
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
        data_bar = data_Women

    else:
        data_bar = []
        Error_Message = 1

    # Define the Layout
    if Error_Message != 1:
        layout_bar = dict(title=dict(text='Number of Medals per Gender'),
                          yaxis=dict(title='Number of Medals', tickfont=dict(size=9)),
                          xaxis=dict(title="Year", tickfont=dict(size=9)),
                          )
    else:
        layout_bar = dict(title=dict(text='Number of Medals per Gender'),
                          yaxis=dict(visible=False),
                          xaxis=dict(visible=False),
                          annotations=[dict(text='No matching data found',
                                            xref="paper",
                                            yref="paper",
                                            showarrow=False,
                                            font=dict(size=12))
                                       ]
                          )

    # -- Step 3 - Plot the Figure

    fig_Gender_Year = go.Figure(data=data_bar, layout=layout_bar)


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                       Plot 3  - Gender Participation per Sport per Year
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot

    # - Step 2.1 - Women data
    df_Plot_Woman = pd.pivot_table(df[df['Gender'] == "Women"], values='Medal', index=['Year'], columns=['Sport'],
                                   aggfunc=len, dropna=False)
    df_Plot_Woman[df_Plot_Woman > 0] = 2
    df_Plot_Woman[np.isnan(df_Plot_Woman)] = 1
    df_Plot_Men = pd.pivot_table(df[df['Gender'] == "Men"], values='Medal', index=['Year'], columns=['Sport'],
                                 aggfunc=len)

    # - Step 2.2 - Men data
    df_Plot_Men[df_Plot_Men > 0] = 3
    df_Plot_Men[np.isnan(df_Plot_Men)] = 1

    # - Step 2.3 - Multipli Men and Women data
    df_Sport_Year = df_Plot_Men * df_Plot_Woman

    # - Step 2.4 - Check Missing Values
    df_Sport_Year[np.isnan(df_Sport_Year)] = df_Plot_Men
    df_Sport_Year[np.isnan(df_Sport_Year)] = df_Plot_Woman
    df_Sport_Year[df_Sport_Year == 1] = 0

    # - Step 2.5 - Set the scale
    df_Sport_Year.replace(0, np.nan, inplace=True)
    df_Sport_Year.replace(6, 1, inplace=True)
    df_Sport_Year.replace(3, 0.5, inplace=True)
    df_Sport_Year.replace(2, 0.25, inplace=True)
    df_Plot = df_Sport_Year.T

    # - Step 2.6 - Change data for the hover
    df_Sport_Year_Name = df_Sport_Year.T
    df_Sport_Year_Name.replace(np.nan, "None", inplace=True)
    df_Sport_Year_Name.replace(1, "Both", inplace=True)
    df_Sport_Year_Name.replace(0.5, "Men", inplace=True)
    df_Sport_Year_Name.replace(0.25, "Women", inplace=True)


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
                     name='Gender Representation',
                     colorscale=[[0, '#FFC0CB'], [0.33, '#FFC0CB'], [0.33, '#87CEFA'], [0.66, '#87CEFA'],
                                 [0.66, '#c3e4a1'], [1, '#c3e4a1']],
                     hovertemplate="Year: <b>%{x}</b><br>" +
                                   "Sport: <b>%{y}</b><br>" +
                                   "Played by: <b>%{customdata}</b><br>",
                     colorbar=dict(tickmode="array", tickvals=[0.25, 0.5, 0.75], ticktext=["Women", "Men", "Both"])
                     )

    layout_corr = dict(title="Sports played per Gender",
                       autosize=False,
                       height=800,
                       width=800,
                       yaxis=dict(tickfont=dict(size=9)),
                       xaxis=dict(tickfont=dict(size=9)),
                       annotations= [dict(text='Softball was the only Sport played exclusively by Women since 1996 until 2014',
                            x = '1996',
                            y = 'Softball',
                            bordercolor="#FFC0CB",
                            borderwidth=1,
                            borderpad=4,
                            bgcolor="#f9f9f9",
                            opacity=0.8,
                            font=dict(size=6))
                         ]
                       )


    # -- Step 3 - Plot the Figure
    fig_Gender_Participation = go.Figure(data=data_corr, layout=layout_corr)


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#                                                Plot 4  - Gender Swap
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||#

    # -- Step 2 - Prepare Data to Plot
    df_GenderParticipationColumns = df_Sport_Year_Name.stack().reset_index().rename(columns={'level_0':'Sport','level_1':'Year', 0:'PlayedBy'})
    df_GenderParticipationColumns.drop(columns=['Sport'])
    df_GenderPlayedBy = pd.pivot_table(df_GenderParticipationColumns, index=['Year'], columns=['PlayedBy'], aggfunc=len)
    df_GenderPlayedBy.columns = [col[1] for col in df_GenderPlayedBy.columns]
    df_GenderPlayedBy=df_GenderPlayedBy.drop(columns=['None'], axis=1)
    df_GenderPlayedBy.replace(np.nan,0, inplace=True)

    df_GenderPlayedBy['Total'] = df_GenderPlayedBy.sum(axis=1)
    df_GenderPlayedBy['Men_Percentage'] = round(100*df_GenderPlayedBy['Men']/df_GenderPlayedBy['Total'],2)
    df_GenderPlayedBy['Women_Percentage'] = round(100*df_GenderPlayedBy['Women']/df_GenderPlayedBy['Total'],2)
    df_GenderPlayedBy['Both_Percentage'] = round(100*df_GenderPlayedBy['Both']/df_GenderPlayedBy['Total'],2)

    data_Men = (dict(type='bar',
                         x=df_GenderPlayedBy.index,
                         y=df_GenderPlayedBy['Men_Percentage'],
                         text=df_GenderPlayedBy['Men_Percentage'],
                         textposition='auto',
                         name="Men",
                         marker_color="#87CEFA",
                         hovertemplate="Year: <b>%{x}</b><br>" +
                                      "Gender: <b>Men</b><br>" +
                                      "Percentage of Participation: <b>%{y}%</b><br>",
                         )
                    )

    data_Women = (dict(type='bar',
                       x=df_GenderPlayedBy.index,
                       y=df_GenderPlayedBy['Women_Percentage'],
                       text=df_GenderPlayedBy['Women_Percentage'],
                       textposition='auto',
                       name="Women",
                       marker_color="#FFC0CB",
                       hovertemplate="Year: <b>%{x}</b><br>" +
                                     "Gender: <b>Women</b><br>" +
                                     "Percentage of Participation: <b>%{y}%</b><br>",
                       )
                  )

    data_Both = (dict(type='bar',
                       x=df_GenderPlayedBy.index,
                       y=df_GenderPlayedBy['Both_Percentage'],
                       text=df_GenderPlayedBy['Both_Percentage'],
                       textposition='auto',
                       name="Both",
                       marker_color="#c3e4a1",
                       hovertemplate="Year: <b>%{x}</b><br>" +
                                     "Gender: <b>Both</b><br>" +
                                     "Percentage of Participation: <b>%{y}%</b><br>",
                       )
                  )


    data_bar = [data_Men, data_Women, data_Both]

    layout_bar = dict(barmode = 'stack',
                     title=dict(text='Percentage of Participation per Gender'),
                     yaxis=dict(title='Percentage of Participation [%]'),
                     xaxis=dict(title="Year"),
                     )

    # -- Step 3 - Plot the Figure
    fig_Gender_Swap = go.Figure(data=data_bar, layout=layout_bar)


    return N_Country_Total_Filter, N_Country_Gender_Men_Filter, N_Country_Gender_Women_Filter, \
           N_Athletes_Total_Filter, N_Athletes_Gender_Men_Filter, N_Athletes_Gender_Women_Filter, \
           N_Sports_Total_Filter, N_Sports_Gender_Men_Filter, N_Sports_Gender_Women_Filter, \
           fig_Gender_Percentage, fig_Gender_Year, fig_Gender_Participation, fig_Gender_Swap


if __name__ == '__main__':
    app.run_server(debug=True)
