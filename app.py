import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import plotly.graph_objects as go
from visualization import radar_capability, radar_capability_comparison, \
    off_def_plot, team_summary, scale_player, scale_team
import pickle
from data import fantasy_team_stats, Player_ODFAI, results
from data import C_list, PF_list, PG_list, SF_list, SG_list
from dash.exceptions import PreventUpdate


# player_name = ["name1", "name2", "name3", "name4", "name5",
#               "name6", "name7", "name8", "name9", "name10",
#               "name11", "name12", "name13", "name14", "name15"]
# player1 = {"Offensive": 20, "Defensive": 15, "Aggression": 3, "Control":20, "Form Stability": 5}
# player2 = {"Offensive": 16, "Defensive": 30, "Aggression": 4, "Control":28, "Form Stability": 3}
# player3 = {"Offensive": 26, "Defensive": 20, "Aggression": 6, "Control":18, "Form Stability": 2}
# player4 = {"Offensive": 10, "Defensive": 40, "Aggression": 2, "Control":18, "Form Stability": 6}
# player5 = {"Offensive": 14, "Defensive": 30, "Aggression": 3, "Control":13, "Form Stability": 7}
# player6 = {"Offensive": 20, "Defensive": 15, "Aggression": 3, "Control":20, "Form Stability": 5}
# player7 = {"Offensive": 16, "Defensive": 30, "Aggression": 4, "Control":28, "Form Stability": 3}
# player8 = {"Offensive": 26, "Defensive": 20, "Aggression": 6, "Control":18, "Form Stability": 2}
# player9 = {"Offensive": 10, "Defensive": 40, "Aggression": 2, "Control":18, "Form Stability": 6}
# player10 = {"Offensive": 14, "Defensive": 30, "Aggression": 3, "Control":13, "Form Stability": 7}
# player11 = {"Offensive": 20, "Defensive": 15, "Aggression": 3, "Control":20, "Form Stability": 5}
# player12 = {"Offensive": 16, "Defensive": 30, "Aggression": 4, "Control":28, "Form Stability": 3}
# player13 = {"Offensive": 26, "Defensive": 20, "Aggression": 6, "Control":18, "Form Stability": 2}
# player14 = {"Offensive": 10, "Defensive": 40, "Aggression": 2, "Control":18, "Form Stability": 6}
# player15 = {"Offensive": 14, "Defensive": 30, "Aggression": 3, "Control":13, "Form Stability": 7}
#
# test = pd.DataFrame([player1, player2, player3, player4, player5,
#                      player6, player7, player8, player9, player10,
#                      player11, player12, player13, player14, player15], index=player_name)
#


player_cap = pd.read_csv('data/player_cap_df.csv', index_col="Player")

player_name = list(player_cap.index)

# player_df_scaled = scale_visualization_data(player_cap)

# player1_od = {"Offensive": 20, "Defensive": 15}
# player2_od = {"Offensive": 16, "Defensive": 30}
# player3_od = {"Offensive": 26, "Defensive": 20}
# player4_od = {"Offensive": 10, "Defensive": 40}
# player5_od = {"Offensive": 14, "Defensive": 30}
# player6_od = {"Offensive": 20, "Defensive": 22}
# player7_od = {"Offensive": 16, "Defensive": 17}
# player8_od = {"Offensive": 26, "Defensive": 23}
# player9_od = {"Offensive": 10, "Defensive": 25}
# player10_od = {"Offensive": 22, "Defensive": 19}
# player11_od = {"Offensive": 17, "Defensive": 18}
# player12_od = {"Offensive": 23, "Defensive": 23}
# player13_od = {"Offensive": 19, "Defensive": 26}
# player14_od = {"Offensive": 11, "Defensive": 22}
# player15_od = {"Offensive": 26, "Defensive": 16}
#
# test_od = pd.DataFrame([player1_od,player2_od,player3_od,player4_od,player5_od,
#                      player6_od, player7_od,player8_od,player9_od,player10_od,
#                      player11_od, player12_od,player13_od,player14_od,player15_od], index = player_name)
#
# player_od_df = test_od.copy()
#
# team1 = {"Offensive": 20, "Defensive": 15, "Aggression": 3, "Control":20, "Form Stability": 5, "Cooperation": 10}

player_od_df = player_cap[["Offense", "Defense"]]


################################################
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/coff.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization and Simulation of NBA Player Capability Using 2019-2020 NBA Stats')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('jack.jpeg'),
                         style={'height': '35px', 'paddingTop': '7%', 'paddingRight': '300px'}),
                html.Span('NBA Git Repo', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                        'paddingLeft': '1px', 'color': '#a3a7b0',
                                                        'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/data1050projectfall2019/data1050project'),
        html.B([html.Img(id='nba_logo', src=app.get_asset_url('nba-logo.jpg'),
                         style={'height': '100px', 'paddingTop': '1%'}),
                html.Span(' ', style={'fontSize': '2rem', 'height': '100px', 'bottom': 0,
                                      'paddingLeft': '4px', 'color': '#a3a7b0',
                                      'textDecoration': 'none'})],
               className="two columns row"),
        html.Div(children=[dcc.Markdown('''
            ---- CTRL-C, CTRL-V: 
            [About Page](https://docs.google.com/document/d/1cE0z6fRTA5pGp01ROxbX_DoFLjuWJOGx4U9gCLJSLKk/edit?usp=sharing), 
            [Additional Details](https://docs.google.com/document/d/1gKH3nA29nzM36KF6Bn30TmFd7xrYvLhz_bOSfw_A8tc/edit?usp=sharing)
            ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")
    ], className="row")


def description():
    """
    Returns overall project description
    """
    return html.Div(children=[
        dcc.Markdown('''
        ## NBA Player Capability Visualization
        
        Shiyu Liu | Peter Huang | Yi Wang
        
       All sports, regardless of the individual or team sports, create a large amount of data after even a single match. 
       Sports fans, media, bookmaker and team administrators investigate the data for multifarious needs. Since such 
       raw data merely are numbers that are hardly being comprehensible and interpretable, statistical analysis and 
       corresponding result visualization become the most crucial part when utilizing the data. In this project, we 
       aim to collect, store, analyze, and visualize NBA player match statistics. To provide users with more flexible 
       results, we expect our application to provide player capability visualization and comparisons based on users’ 
       queries. This application also enables the users to build their own team, and simulate a match between two teams.

        #### Data Source
        Data is obtained from https://www.basketball-reference.com/leagues/NBA_2020_per_game.html.

        ** The data is updated everyday after all match have been completed on that day**. 
        
        Our data include all registered players. You can select two of them to compare their performance below.
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")



def select_one_or_two_player():
    """Select one or two players from the player list"""
    return html.Div(children=[
        html.Div(id='above_drop_down', style={'marginTop': '2rem'}),
        html.Div(children=[
        html.Div(children=[
        dcc.Markdown('''Please select a player to visualize his performance:'''),
        dcc.Dropdown(
            options=[{"label": name, "value": name} for name in player_name],
            value=[],
            multi=False,
            id="player1_name",
            style={'height': '30px', 'width': '300px'}
        )], style={'width': '300px', 'marginLeft': '90px', 'display': 'inline-block'}),

        html.Div(children=[
        dcc.Markdown('''Please select a second player to compare their performance:'''),
        dcc.Dropdown(
            options=[{"label": name, "value": name} for name in player_name],
            value=[],
            multi=False,
            id="player2_name",
            style={'height': '30px', 'width': '300px'}
        )], style={'width': '300px', 'align': 'right', 'marginLeft': '400px', 'display': 'inline-block'})
        ]),

        html.Div(id='below_first_drop_down', style={'marginTop': '2rem'}),

        html.Div(children=[html.Div(children=[dcc.Graph(id='ranking1')], style={'width': '48%', 'align': 'right', 'display': 'inline-block'}),
                           html.Div(children=[dcc.Graph(id='ranking2')],
                           style={'width': '48%', 'align': 'right', 'display': 'inline-block'})], className='eleven columns'),

        html.Div(id='below_drop_down', style={'marginTop': '2rem'}),
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='eleven columns'),
        html.Div(id='below_visual', style={'marginTop': '2rem'})
    ], style={'marginLeft': '80px'})


def enhancement_description():
    """
    Returns enhancement part description
    """
    return html.Div(children=[dcc.Markdown('''
        ### Fantasy Team
        Finishing viewing the players?  Now select and build your team. You are able to build two teams, and our
        application will be able to visualize the overall team summary using the radar plot. This plot is an 
        comprehensive estimation on the players you selected. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


# c = ['name1', 'name2', 'name3']
# pf = ['name4', 'name5', 'name6']
# sf = ['name7', 'name8', 'name9']
# sg = ['name10', 'name11', 'name12']
# pg = ['name13', 'name14', 'name15']


c = C_list
pf = PF_list
sf = SF_list
sg = SG_list
pg = PG_list


def enhancement_team_what_if():
    return html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in c],
                        multi=False,
                        id="c",
                        placeholder="Select a Center",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in pf],
                        multi=False,
                        id="pf",
                        placeholder="Select a Power Forward",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in sf],
                        multi=False,
                        id="sf",
                        placeholder="Select a Small Forward",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in sg],
                        multi=False,
                        id="sg",
                        placeholder="Select a Shooting Guard",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in pg],
                        multi=False,
                        id="pg",
                        placeholder="Select a Point Guard",
                        style={'height': '0px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'})], style={'marginTop': '3.5rem', 'marginLeft': '80px', 'display': 'inline-block'}),

            html.Div(children=[
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in c],
                        multi=False,
                        id="c2",
                        placeholder="Select a Center",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in pf],
                        multi=False,
                        id="pf2",
                        placeholder="Select a Power Forward",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in sf],
                        multi=False,
                        id="sf2",
                        placeholder="Select a Small Forward",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in sg],
                        multi=False,
                        id="sg2",
                        placeholder="Select a Shooting Guard",
                        style={'height': '20px', 'width': '500px'}
                    )
                ], style={'width': '200px', 'marginTop': '3.5rem'}),
                html.Div(children=[
                    dcc.Dropdown(
                        options=[{"label": name, "value": name} for name in pg],
                        multi=False,
                        id="pg2",
                        placeholder="Select a Point Guard",
                        style={'height': '0px', 'width': '500px'}
                    )
                ], style={'marginTop': '3.5rem'})],
                style={'width': '300px', 'align': 'right', 'marginLeft': '450px', 'display': 'inline-block'}),
        ]),

        html.Div(id='below 2 team', style={'marginTop': '8rem'}),
        html.Div(children=[html.Div(children=[dcc.Graph(id='team_summary1')],
                                    style={'width': '42%', 'align': 'right', 'display': 'inline-block'}),
                           html.Div(children=[dcc.Graph(id='team_summary2')],
                                    style={'width': '42%', 'align': 'right', 'display': 'inline-block'})],
                 className='eleven columns')
        ], style={'marginLeft': '80px'})


def start_match():
    return html.Div(children=[
            html.Div(id='above the button', style={'marginTop': '8rem'}),
            html.Button('Simulate the Match!', id='button', style={'marginLeft': '450px', 'color': 'white', "backgroundColor":'blue'}),
            html.Div(id='output-container-button',
                     children='After selecting all players, start the match and view the result',
                     style={'marginLeft': '350px', 'color': 'white', 'fontSize': '2rem'})
            ], style={'marginLeft': '80px'})


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(
                src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''

        ''')
    ], className='row')


app.layout = html.Div([
    page_header(),
    html.Hr(),
    description(),
    select_one_or_two_player(),
    enhancement_description(),
    enhancement_team_what_if(),
    start_match(),
    architecture_summary()
    ])


@app.callback(
    dash.dependencies.Output('ranking1', 'figure'),
    [dash.dependencies.Input("player1_name", 'value')]
)
def display_ranking1(player1):
    if player1:
        o, d, cur = off_def_plot(player1, player_od_df)
        return cur
    else:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", width=500, height=280,
                          title="No Info", xaxis=dict(showticklabels=False),
                          yaxis=dict(showticklabels=False))
        return fig


@app.callback(
    dash.dependencies.Output('ranking2', 'figure'),
    [dash.dependencies.Input("player2_name", 'value')]
)
def display_ranking2(player2):
    if player2:
        o, d, cur = off_def_plot(player2, player_od_df)
        return cur
    else:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", width=500,
                          height=280, title="No Info", xaxis=dict(showticklabels=False),
                          yaxis=dict(showticklabels=False))
        return fig


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input("player1_name", 'value'),
     dash.dependencies.Input("player2_name", 'value')]
)
def what_if_handler(player1, player2):
    """Changes the display graph based on player input"""
    if player1 and player2:
        player1_result, feature_list = scale_player(player1, Player_ODFAI(player1))
        player2_result, feature_list = scale_player(player2, Player_ODFAI(player2))
        cur = radar_capability_comparison(feature_list, player1_result,
                                          player2_result, [player1, player2])
    elif player1:
        player1_result, feature_list = scale_player(player1, Player_ODFAI(player1))
        cur = radar_capability(feature_list,  player1_result, player1)
    elif player2:
        player2_result, feature_list = scale_player(player2, Player_ODFAI(player2))
        cur = radar_capability(feature_list, player2_result, player2)
    else:
        cur = radar_capability(['Control', 'Defensive', 'Impact', 'Offense', 'Scoring'], [-0.1, -0.1, -0.1, -0.1, -0.1], "No Player Info")
    return cur


@app.callback(
    dash.dependencies.Output('team_summary1', 'figure'),
    [dash.dependencies.Input("pg", 'value'),
     dash.dependencies.Input("sg", 'value'),
     dash.dependencies.Input("sf", 'value'),
     dash.dependencies.Input("pf", 'value'),
     dash.dependencies.Input("c", 'value')]
)
def display_team1(name1, name2, name3, name4, name5):
    t0 = {"Offense": -5, "Defense": -5, "Scoring": -5, "Control": -5, "Impact": -5, "Tacit": -5, "Shooting": -5}
    if name1 or name2 or name3 or name4 or name5:
        summary0 = fantasy_team_stats(name1, name2, name3, name4, name5)
        summary1 = scale_team("TEAM 1", summary0)
        cur = team_summary(summary1, "TEAM 1")
    else:
        cur = team_summary(t0, "TEAM 1")
    return cur


@app.callback(
    dash.dependencies.Output('team_summary2', 'figure'),
    [dash.dependencies.Input("pg2", 'value'),
     dash.dependencies.Input("sg2", 'value'),
     dash.dependencies.Input("sf2", 'value'),
     dash.dependencies.Input("pf2", 'value'),
     dash.dependencies.Input("c2", 'value')]
)
def display_team2(name1, name2, name3, name4, name5):
    t0 = {"Offense": -5, "Defense": -5, "Scoring": -5, "Control": -5, "Impact": -5, "Tacit": -5, "Shooting": -5}
    if name1 or name2 or name3 or name4 or name5:
        summary0 = fantasy_team_stats(name1, name2, name3, name4, name5)
        summary2 = scale_team("TEAM 1", summary0)
        cur = team_summary(summary2, "TEAM 2")
    else:
        cur = team_summary(t0, "TEAM 2")
    return cur


@app.callback(
    Output(component_id='output-container-button', component_property='children'),
    [dash.dependencies.Input(component_id='button', component_property='n_clicks')],
    [
     dash.dependencies.State("pg", 'value'),
     dash.dependencies.State("sg", 'value'),
     dash.dependencies.State("sf", 'value'),
     dash.dependencies.State("pf", 'value'),
     dash.dependencies.State("c", 'value'),
     dash.dependencies.State("pg2", 'value'),
     dash.dependencies.State("sg2", 'value'),
     dash.dependencies.State("sf2", 'value'),
     dash.dependencies.State("pf2", 'value'),
     dash.dependencies.State("c2", 'value')
     ]
)
def update_output(n_clicks, player1, player2, player3, player4, player5, player6, player7, player8, player9, player10):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if player1 and player2 and player3 and player4 and player5 and player6 and player7 and player8 and player9 and player10:
            ability1, ability2, score1, score2, result = results(player1, player2, player3, player4,
                                                                 player5, player6, player7, player8, player9, player10)
            return u'''
                {}, the score is {} to {}
            '''.format(result, score1, score2)
        else:
            return "You have to select all 10 players"


if __name__ == '__main__':
    app.run_server(debug=True)