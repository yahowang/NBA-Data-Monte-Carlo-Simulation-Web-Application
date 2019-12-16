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
    scaler = MinMaxScaler(copy=True)
    player_df_scaled = player_df.copy()
    player_df_scaled[player_df.columns] = scaler.fit_transform(player_df)
    return player_df_scaled


def scale_player(player_name, player_cap_dict):
    player_max = {"Control": 5, "Defense": 115, "Impact": 0.15, "Offense": 140, "Scoring": 0.65}

    player_min = {"Control": 0, "Defense": 90, "Impact": 0, "Offense": 45, "Scoring": 0}

    index1 = [player_name, 'player_max', 'player_min']

    player_df = pd.DataFrame([player_cap_dict, player_max, player_min], index=index1)
    player_df = player_df.astype("float")

    feature_list = list(player_df.columns)
    scaler = MinMaxScaler(copy=True)
    player_df_scaled = player_df.copy()
    player_df_scaled[player_df.columns] = scaler.fit_transform(player_df)

    player_result = player_df_scaled.loc[player_name, :]

    for i in range(len(player_result)):
        if player_result[i] > 1:
            player_result[i] = 0.7
        if player_result[i] < 0:
            player_result[i] = 0
    return player_result, feature_list


def scale_team(team_name, team_cap_dict):
    team_max = {"Offense": 58, "Defense": 48, "Scoring": 55, "Control": 25, "Impact": 47, "Tacit": 66, "Shooting": 66}

    team_min = {"Offense": 35, "Defense": 20, "Scoring": 30, "Control": 7, "Impact": 6, "Tacit": 15, "Shooting": 40}

    index1 = [team_name, 'team_max', 'team_min']

    team_df = pd.DataFrame([team_cap_dict, team_max, team_min], index=index1)

    team_df = team_df.astype("float")

    feature_list = list(team_df.columns)
    scaler = MinMaxScaler(feature_range=(0, 100), copy=True)
    team_df_scaled = team_df.copy()
    team_df_scaled[team_df.columns] = scaler.fit_transform(team_df)

    team_result = team_df_scaled.loc[team_name, :]

    for i in range(len(team_result)):
        if team_result[i] > 100:
            team_result[i] = 100
        if team_result[i] < 0:
            team_result[i] = 0
    return dict(team_result)


def radar_capability(feature_list, player_value, playername):
    fig = go.Figure()
    player_value = list(player_value)
    player_value.append(player_value[0])
    feature_list.append(feature_list[0])
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
    player1_value = list(player1_value)
    player1_value.append(player1_value[0])
    player2_value = list(player2_value)
    player2_value.append(player2_value[0])
    feature_list.append(feature_list[0])
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

    DEF = list(off_def_df["Defense"])
    OFF = list(off_def_df["Offense"])
    player_od = off_def_df.loc[player_name]
    player_def = player_od["Defense"]
    player_off = player_od["Offense"]

    off_perc = calculate_pecentile(OFF, player_off)
    def_perc = calculate_pecentile(DEF, player_def)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Offensive Stats Ranking', 'Defensive Stats Ranking'],

        x=[off_perc, def_perc],
        name='name5',
        orientation='h',
        marker=dict(
            color='rgba(122, 120, 168, 0.8)',
            line=dict(color='rgb(248, 248, 249)', width=0.1)
        )
    ))

    fig.add_trace(go.Bar(
        y=['Offensive Stats Ranking', 'Defensive Stats Ranking'],
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

    value = list(value)
    value.append(value[0])
    feature.append(feature[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=value,
        theta=feature,
        fill='toself',
        name=team_name,
        line_color='deepskyblue'
    ))

    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(range=[-5, 105], showticklabels=False)
        ),
        title=team_name,
        font_size=20
    )

    return fig
