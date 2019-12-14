import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import plotly.graph_objects as go
from scipy import stats


# Input is a dataframe containing all of the players, output scaled df
def scale_visualization_data(player_df):
    player_df = player_df.astype("float")
    feature_list = player_df.columns
    scaler = MinMaxScaler(copy=True)
    player_df_scaled = player_df.copy()
    player_df_scaled[player_df.columns] = scaler.fit_transform(player_df)
    return player_df_scaled


def radar_capability(feature_list, player_value, playername):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=player_value,
        theta=feature_list,
        fill='toself',
        name=playername
    ))

    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(range=[-0.1, 1.1], showticklabels=False, ticks='')
        ),
        title=playername,
        font_size=20
    )
    return fig


# Input two player info to compare the two player capability
def radar_capability_comparison(feature_list, player1_value, player2_value, playername_list):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=player1_value,
        theta=feature_list,
        fill='toself',
        name=playername_list[0]
    ))
    fig.add_trace(go.Scatterpolar(
        r=player2_value,
        theta=feature_list,
        fill='toself',
        name=playername_list[1]
    ))

    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(range=[-0.1, 1.1], showticklabels=False, ticks='')
        ),
        font_size=20
    )

    return fig


# Calculate the Percentile of a value in a list
def calculate_pecentile(arr, x):
    percentile = np.around(stats.percentileofscore(arr, x), decimals = 0)
    return percentile


# mean = {"Defensive Mean:": np.mean(test_od["Defensive"]), "Offensive mean": np.mean(test_od["Offensive"])}

def off_def_plot(player_name, off_def_df):
    off_def_df = off_def_df.astype("float")

    DEF = list(off_def_df["Defensive"])
    OFF = list(off_def_df["Offensive"])
    player_od = off_def_df.loc[player_name]
    player_def = player_od["Defensive"]
    player_off = player_od["Offensive"]

    off_perc = calculate_pecentile(OFF, player_off)
    def_perc = calculate_pecentile(DEF, player_def)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Offensive Ranking', 'Defensive Ranking'],

        x=[off_perc, def_perc],
        name='name5',
        orientation='h',
        marker=dict(
            color='rgba(122, 120, 168, 0.8)',
            line=dict(color='rgb(248, 248, 249)', width=0.1)
        )
    ))

    fig.add_trace(go.Bar(
        y=['Offensive Ranking', 'Defensive Ranking'],
        x=[100 - off_perc, 100 - def_perc],
        name='All NBA Players',
        orientation='h',
        marker=dict(
            color='rgba(190, 192, 213, 1)',
            line=dict(color='rgb(248, 248, 249)', width=0.1)
        )
    ))
    fig.update_layout(barmode='stack', template="plotly_dark",
                      width=500,
                      height=280,
                      xaxis=dict(
                          showgrid=True,
                          showline=False,
                          showticklabels=True,
                          zeroline=False,
                          domain=[0.15, 1]
                      ),
                      title=player_name,
                      showlegend=False,
                      bargap=0.5
                      )
    return player_off, player_def, fig


# For visualizing the
def team_summary(team_dict, team_name):
    feature = list(team_dict.keys())
    value = list(team_dict.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=value,
        theta=feature,
        fill='toself',
        name=team_name
    ))

    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(range=[0, 50], showticklabels=False)
        ),
        title=team_name,
        font_size=20
    )

    return fig
