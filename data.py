import pandas as pd
import numpy as np
# from database import *


df = pd.read_csv('data/df.csv')
# df = to_df()

def _cleaning(df):
    df.loc[df['FGA'] == 0, ['FG%', 'eFG%']] = 0
    df.loc[df['3PA'] == 0, '3P%'] = 0
    df.loc[df['2PA'] == 0, '2P%'] = 0
    df.loc[df['FTA'] == 0, 'FT%'] = 0
    return df


def _Player_ODFI_wopp(Player, Opponent, df):
    ind = np.where(df['Player'] == Player)[0][0]
    Team = df['Tm'][ind]
    Team_df = df[df['Tm'] == Team]
    Opponent_df = df[df['Tm'] == Opponent].reset_index(drop=True)
    Team_MP = sum(Team_df['MP'])
    Team_FGM = sum(Team_df['FG'])
    Team_FGA = sum(Team_df['FGA'])
    Team_3PM = sum(Team_df['3P'])
    Team_FTM = sum(Team_df['FT'])
    Team_FTA = sum(Team_df['FTA'])
    Team_ORB = sum(Team_df['ORB'])
    Team_DRB = sum(Team_df['DRB'])
    Team_AST = sum(Team_df['AST'])
    Team_STL = sum(Team_df['STL'])
    Team_BLK = sum(Team_df['BLK'])
    Team_TOV = sum(Team_df['TOV'])
    Team_PF = sum(Team_df['PF'])
    Team_PTS = sum(Team_df['PTS'])

    Opponent_MP = sum(Opponent_df['MP'])
    Opponent_FGM = sum(Opponent_df['FG'])
    Opponent_FGA = sum(Opponent_df['FGA'])
    Opponent_FTM = sum(Opponent_df['FT'])
    Opponent_FTA = sum(Opponent_df['FTA'])
    Opponent_ORB = sum(Opponent_df['ORB'])
    Opponent_TRB = sum(Opponent_df['TRB'])
    Opponent_TOV = sum(Opponent_df['TOV'])
    Opponent_PTS = sum(Opponent_df['PTS'])

    GmPTS = Team_PTS + Opponent_PTS
    GmFGM = Team_FGM + Opponent_FGM
    GmFTM = Team_FTM + Opponent_FTM
    GmFGA = Team_FGA + Opponent_FGA
    GmFTA = Team_FTA + Opponent_FTA
    GmDREB = Team_DRB + sum(Opponent_df['DRB'])
    GmOREB = Team_ORB + Opponent_ORB
    GmAST = Team_AST + sum(Opponent_df['AST'])
    GmSTL = Team_STL + sum(Opponent_df['STL'])
    GmBLK = Team_BLK + sum(Opponent_df['BLK'])
    GmPF = Team_PF + sum(Opponent_df['PF'])
    GmTO = Team_TOV + Opponent_TOV

    qAST = ((Team_df.MP / (Team_MP / 5)) * (1.14 * ((Team_AST - Team_df.AST) / Team_FGM))) + ((((
                                                                                                            Team_AST / Team_MP) * Team_df.MP * 5 - Team_df.AST) / (
                                                                                                           (
                                                                                                                       Team_FGM / Team_MP) * Team_df.MP * 5 - Team_df.FG)) * (
                                                                                                          1 - (
                                                                                                              Team_df.MP / (
                                                                                                                  Team_MP / 5))))
    FG_Part = Team_df.FG * (1 - 0.5 * ((Team_df.PTS - Team_df.FT) / (2 * Team_df.FGA)) * qAST)
    FG_Part = FG_Part.replace(np.nan, 0)
    AST_Part = 0.5 * (
                ((Team_PTS - Team_FTM) - (Team_df.PTS - Team_df.FT)) / (2 * (Team_FGA - Team_df.FGA))) * Team_df.AST
    FT_Part = (1 - (1 - Team_df['FT%']) ** 2) * 0.4 * Team_df.FTA
    Team_Scoring_Poss = Team_FGM + (1 - (1 - (Team_FTM / Team_FTA)) ** 2) * Team_FTA * 0.4
    Team_ORBP = Team_ORB / (Team_ORB + (Opponent_TRB - Opponent_ORB))
    Team_PlayP = Team_Scoring_Poss / (Team_FGA + Team_FTA * 0.4 + Team_TOV)
    Team_ORB_Weight = ((1 - Team_ORBP) * Team_PlayP) / ((1 - Team_ORBP) * Team_PlayP + Team_ORBP * (1 - Team_PlayP))
    ORB_Part = Team_df.ORB * Team_ORB_Weight * Team_PlayP
    ScPoss = (FG_Part + AST_Part + FT_Part) * (
                1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_PlayP) + ORB_Part

    FGxPoss = (Team_df.FGA - Team_df.FG) * (1 - 1.07 * Team_ORBP)
    FTxPoss = ((1 - Team_df['FT%']) ** 2) * 0.4 * Team_df.FTA

    TotPoss = ScPoss + FGxPoss + FTxPoss + Team_df.TOV

    PProd_FG_Part = 2 * (Team_df.FG + 0.5 * Team_df['3P']) * (
                1 - 0.5 * ((Team_df.PTS - Team_df.FT) / (2 * Team_df.FGA)) * qAST)
    PProd_FG_Part = PProd_FG_Part.replace(np.nan, 0)
    PProd_AST_Part = 2 * (
                (Team_FGM - Team_df.FG + 0.5 * (Team_3PM - Team_df['3P'])) / (Team_FGM - Team_df.FG)) * 0.5 * (
                                 ((Team_PTS - Team_FTM) - (Team_df.PTS - Team_df.FT)) / (
                                     2 * (Team_FGA - Team_df.FGA))) * Team_df.AST
    PProd_ORB_Part = Team_df.ORB * Team_ORB_Weight * Team_PlayP * (
                Team_PTS / (Team_FGM + (1 - (1 - (Team_FTM / Team_FTA)) ** 2) * 0.4 * Team_FTA))
    PProd = (PProd_FG_Part + PProd_AST_Part + Team_df.FT) * (
                1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_PlayP) + PProd_ORB_Part

    ORtg = 100 * (PProd / TotPoss)
    ORtg = ORtg.replace(np.nan, 0)

    DORP = Opponent_ORB / (Opponent_ORB + Team_DRB)
    DFGP = Opponent_FGM / Opponent_FGA
    FMwt = (DFGP * (1 - DORP)) / (DFGP * (1 - DORP) + (1 - DFGP) * DORP)
    Stops1 = Team_df.STL + Team_df.BLK * FMwt * (1 - 1.07 * DORP) + Team_df.DRB * (1 - FMwt)
    Stops2 = (((Opponent_FGA - Opponent_FGM - Team_BLK) / Team_MP) * FMwt * (1 - 1.07 * DORP) + (
                (Opponent_TOV - Team_STL) / Team_MP)) * Team_df.MP + (Team_df.PF / Team_PF) * 0.4 * Opponent_FTA * (
                         1 - (Opponent_FTM / Opponent_FTA)) ** 2
    Stops = Stops1 + Stops2
    Team_Possessions = sum(TotPoss)
    StopP = (Stops * Opponent_MP) / (Team_Possessions * Team_df.MP)
    StopP = StopP.replace(np.nan, 0)
    Team_Defensive_Rating = 100 * (Opponent_PTS / Team_Possessions)
    D_Pts_per_ScPoss = Opponent_PTS / (
                Opponent_FGM + (1 - (1 - (Opponent_FTM / Opponent_FTA)) ** 2) * Opponent_FTA * 0.4)
    DRtg = Team_Defensive_Rating + 0.2 * (100 * D_Pts_per_ScPoss * (1 - StopP) - Team_Defensive_Rating)

    FloorP = ScPoss / TotPoss
    FloorP = FloorP.replace(np.nan, 0)

    PIE = (df['PTS'][ind] + df['FG'][ind] + df['FT'][ind] - df['FGA'][ind] - df['FTA'][ind] + df['DRB'][ind] + (
                .5 * df['ORB'][ind]) + df['AST'][ind] + df['STL'][ind] + (.5 * df['BLK'][ind]) - df['PF'][ind] -
           df['TOV'][ind]) / (GmPTS + GmFGM + GmFTM - GmFGA - GmFTA + GmDREB + (.5 * GmOREB) + GmAST + GmSTL + (
                .5 * GmBLK) - GmPF - GmTO)

    return ORtg[ind], DRtg[ind], FloorP[ind], PIE


def Player_ODFAI(Player):
    ind = np.where(df['Player'] == Player)[0][0]
    Team = df['Tm'][ind]
    ORtg = 0
    DRtg = 0
    FloorP = 0
    PIE = 0
    for team in set(df['Tm']):
        if team != Team:
            ortg, drtg, floorp, pie = _Player_ODFI_wopp(Player, team, df)
            ORtg += ortg
            DRtg += drtg
            FloorP += floorp
            PIE += pie
    num_team = len(set(df['Tm'])) - 1
    avg_ORtg = ORtg / num_team
    avg_DRtg = DRtg / num_team
    avg_FloorP = FloorP / num_team
    avg_PIE = PIE / num_team
    if df['TOV'][ind] != 0:
        AST_TO = df['AST'][ind] / df['TOV'][ind]
    else:
        AST_TO = df['AST'][ind] * 2

    ret = {"Offense": avg_ORtg, "Defense": avg_DRtg, "Scoring": avg_FloorP, "Control": AST_TO, "Impact": avg_PIE}
    return ret


def advance_df():
    # df = _cleaning(to_df())
    df1 = _cleaning(df)
    performance = []
    for player in df1['Player']:
        performance.append(Player_ODFAI(player, df1))

    advance_df = pd.DataFrame(performance, index = df1['Player'])
    return advance_df


def _Player_PTS_prop(Player, df):
    ind = np.where(df['Player'] == Player)[0][0]
    Team = df['Tm'][ind]
    Team_PTS = sum(df['PTS'][df['Tm'] == Team])
    PTS_prop = df['PTS'][ind] / Team_PTS
    return PTS_prop


def fantasy_team_stats(PG=None, SG=None, SF=None, PF=None, C=None):
    # df = to_df()
    players = []
    if PG:
        players.append(PG)
    if SG:
        players.append(SG)
    if SF:
        players.append(SF)
    if PF:
        players.append(PF)
    if C:
        players.append(C)

    Tm = []
    MP = []
    Offense = []
    Defense = []
    Scoring = []
    Impact = []
    FGA = 0
    FTA = 0
    AST = 0
    TOV = 0
    PTS = 0
    PTS_prop = 0
    for player in players:
        ind = np.where(df['Player'] == player)[0][0]
        Tm.append(df['Tm'][ind])
        MP.append(df['MP'][ind])
        ODFAI = Player_ODFAI(player)
        Offense.append(ODFAI['Offense'])
        Defense.append(ODFAI['Defense'])
        Scoring.append(ODFAI['Scoring'])
        Impact.append(ODFAI['Impact'])
        FGA += df['FGA'][ind]
        FTA += df['FTA'][ind]
        AST += df['AST'][ind]
        TOV += df['TOV'][ind]
        PTS += df['PTS'][ind]
        PTS_prop += _Player_PTS_prop(player, df)
    MP = np.array(MP)
    MP_Weight = MP / sum(MP)

    ORtg = sum(MP_Weight * np.array(Offense)) / 2.15 * len(players) / 5
    DRtg = (sum(MP_Weight * np.array(Defense)) - 90) * 2 * len(players) / 5
    FloorP = sum(MP_Weight * np.array(Scoring)) * 100 * len(players) / 5
    PIE = sum(Impact) / 0.0075
    if PIE < 0:
        PIE = 0
    if TOV != 0:
        AST_TO = AST / TOV * 10
    else:
        AST_TO = AST * 2 * 10
    Tacit = 1.5 - PTS_prop
    for i in range(len(Tm) - 1):
        for j in range(i + 1, len(Tm)):
            if Tm[i] == Tm[j]:
                Tacit += 0.1
    Tacit *= 40
    if FGA == 0 and FTA == 0:
        Shoot = 0
    else:
        Shoot = PTS / (2 * (FGA + 0.44 * FTA)) * 100

    ret = {"Offense": ORtg, "Defense": DRtg, "Scoring": FloorP, "Control": AST_TO, "Impact": PIE, "Tacit": Tacit,
           "Shooting": Shoot}
    return ret


def results(PG1, SG1, SF1, PF1, C1, PG2, SG2, SF2, PF2, C2):
    stats1 = fantasy_team_stats(PG1, SG1, SF1, PF1, C1)
    stats2 = fantasy_team_stats(PG2, SG2, SF2, PF2, C2)
    ability1 = 0.2 * (stats1['Offense'] + stats1['Defense'] + stats1['Scoring'] + stats1['Control'] + stats1['Tacit'] + stats1['Shooting']) + 0.8 * stats1['Impact']
    ability2 = 0.2 * (stats2['Offense'] + stats2['Defense'] + stats2['Scoring'] + stats2['Control'] + stats2['Tacit'] + stats2['Shooting']) + 0.8 * stats2['Impact']
    if ability1 > 100:
        point1 = 100
    if ability2 > 100:
        point2 = 100
    score1 = int(1.25 * ability1 + np.random.normal(0, 10))
    score2 = int(1.25 * ability2 + np.random.normal(0, 10))
    while score1 == score2:
        score1 += int(abs(np.random.normal(10, 5)))
        score2 += int(abs(np.random.normal(10, 5)))
    if score1 > score2:
        result = "Team 1 wins!"
    else:
        result = "Team 2 wins!"
    return ability1, ability2, score1, score2, result


# player_cap = advance_df()
C_list = list(df['Player'][df['Pos'] == 'C'])
PF_list = list(df['Player'][df['Pos'] == 'PF'])
SF_list = list(df['Player'][df['Pos'] == 'SF'])
SG_list = list(df['Player'][df['Pos'] == 'SG'])
PG_list = list(df['Player'][df['Pos'] == 'PG'])


