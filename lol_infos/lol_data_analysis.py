import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, Normalize
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import mongo_code.db_connection as db_conn
import basic_code.basic as basic

class AnalysePlayer:
    def __init__(self, puuid):
        self.puuid = puuid

    def __create_dfs_classic(self):
        match_history = db_conn.find_player_history(self.puuid)

        if match_history == []:
            return None
        
        player_info_df = pd.DataFrame()
        game_info_df = pd.DataFrame()
        bans_info_df = pd.DataFrame()
        teams_info_df = pd.DataFrame()

        for m in match_history:
            game_check = basic.check_invalid_game(m['game_data']['game_duration'])

            if m['game_data']['game_mode'] == "CLASSIC" and game_check == 'valid':
                match_id = m["match_id"]

                player_df = pd.DataFrame(m["players_data"])
                game_df = pd.DataFrame(m["game_data"], index=[0])

                team_rows = []

                for team_name, team_data in m["teams_data"].items():
                    row = {
                        'teamId': team_data['teamId'],
                        'teamName': team_name,
                        'win': team_data['win']
                    }

                    for objective, details in team_data['objectives'].items():
                        row[f"{objective}_first"] = details['first']
                        row[f"{objective}_kills"] = details['kills']
                    
                    team_rows.append(row)

                teams_df = pd.DataFrame(team_rows)

                ban_rows = []

                for team_name, team_data in m["teams_data"].items():
                    
                    for ban in team_data['bans']:
                        ban_row = {
                            'teamId': team_data['teamId'],
                            'teamName': team_name,
                            'championId': ban['championId'],
                            'pickTurn': ban['pickTurn']
                        }
                        ban_rows.append(ban_row)

                bans_df = pd.DataFrame(ban_rows)

                player_df["matchId"] = match_id
                game_df["matchId"] = match_id
                teams_df["matchId"] = match_id
                bans_df["matchId"] = match_id

                player_info_df = pd.concat([player_info_df, player_df], ignore_index=True)
                game_info_df = pd.concat([game_info_df, game_df], ignore_index=True)
                teams_info_df = pd.concat([teams_info_df, teams_df], ignore_index=True)
                bans_info_df = pd.concat([bans_info_df, bans_df], ignore_index=True)
            else:
                continue
        
        return player_info_df, game_info_df, bans_info_df, teams_info_df
    
    def __numerical_analysis(self, p_df):
        # Médias
        kp_mean = round(np.mean(p_df['kp']), 1)
        fb_kill_mean = round(np.mean(p_df['firstBloodKill']) * 100, 1)
        fb_assist_mean = round(np.mean(p_df['firstBloodAssist']) * 100, 1)
        fb_participation_mean = round(fb_kill_mean + fb_assist_mean, 1)
        ft_kill_mean = round(np.mean(p_df['firstTowerKill']) * 100, 1)
        ft_assist_mean = round(np.mean(p_df['firstTowerAssist']) * 100, 1)
        ft_participation_mean = round(ft_kill_mean + ft_assist_mean, 1)
        winrate_mean = round(np.mean(p_df["win"]) * 100, 1)
        wins = np.sum(p_df["win"])
        losses = np.sum(p_df["win"] == False)

        # Extremos
        max_kda = round(np.max(p_df['kda']), 1)
        min_kda = round(np.min(p_df['kda']), 1)
        max_kp = round(np.max(p_df['kp']), 1)
        min_kp = round(np.min(p_df['kp']), 1)
        max_fpm = round(np.max(p_df['fpm']), 1)
        min_fpm = round(np.min(p_df['fpm']), 1)
        max_dpm_champions = round(np.max(p_df['dpmChampions']), 1)
        max_dpm_turrets = round(np.max(p_df['dpmTurrets']), 1)
        min_dpm_champions = round(np.min(p_df['dpmChampions']), 1)
        min_dpm_turrets = round(np.min(p_df['dpmTurrets']), 1)
        max_vspm = round(np.max(p_df['vspm']), 1)
        min_vspm = round(np.min(p_df['vspm']), 1)
        max_percentage_gold = round(np.max(p_df['percentageTeamGold']), 1)
        min_percentage_gold = round(np.min(p_df['percentageTeamGold']), 1)
        max_percentage_dpm_champions = round(np.max(p_df['percentageTeamDpmChampions']), 1)
        min_percentage_dpm_champions = round(np.min(p_df['percentageTeamDpmChampions']), 1)
        max_gold_efficiency = round(np.max(p_df['goldEfficiency']), 1)
        min_gold_efficiency = round(np.min(p_df['goldEfficiency']), 1)

        max_min_dict = {
            "max_kda": max_kda,
            "min_kda": min_kda,
            "max_kp": max_kp,
            "min_kp": min_kp,
            "max_fpm": max_fpm,
            "min_fpm": min_fpm,
            "max_dpm_champions": max_dpm_champions,
            "min_dpm_champions": min_dpm_champions,
            "max_dpm_turrets": max_dpm_turrets,
            "min_dpm_turrets": min_dpm_turrets,
            "max_vspm": max_vspm,
            "min_vspm": min_vspm,
            "max_percentage_gold": max_percentage_gold,
            "min_percentage_gold": min_percentage_gold,
            "max_percentage_dpm_champions": max_percentage_dpm_champions,
            "min_percentage_dpm_champions": min_percentage_dpm_champions,
            "max_gold_efficiency": max_gold_efficiency,
            "min_gold_efficiency": min_gold_efficiency,
            "wins": wins,
            "losses": losses
        }

        mean_dict = {
            "kp": kp_mean,
            "fb_participation": fb_participation_mean,
            "ft_participation": ft_participation_mean,
            "winrate": winrate_mean,
            "wins": wins,
            "losses": losses
        }

        max_min_df = pd.DataFrame([max_min_dict])
        mean_df = pd.DataFrame([mean_dict])

        return mean_df, max_min_df
    
    def __grouped_numerical_analysis(self, p_df):
        # Médias
        kp_mean = round(p_df['kp'].mean(), 1)
        dpm_champion_mean = round(p_df['dpmChampions'].mean(), 1)
        dpm_turret_mean = round(p_df['dpmTurrets'].mean(), 1)
        fpm_mean = round(p_df['fpm'].mean(), 1)
        kda_mean = round(p_df['kda'].mean(), 1)
        gpm_mean = round(p_df['gpm'].mean(), 1)
        gold_efficiency_mean = round(p_df['goldEfficiency'].mean(), 1)
        vspm_mean = round(p_df['vspm'].mean(), 1)
        fb_kill_mean = round(p_df['firstBloodKill'].mean() * 100, 1)
        fb_assist_mean = round(p_df['firstBloodAssist'].mean() * 100, 1)
        fb_participation_mean = round(fb_kill_mean + fb_assist_mean, 1)
        ft_kill_mean = round(p_df['firstTowerKill'].mean() * 100, 1)
        ft_assist_mean = round(p_df['firstTowerAssist'].mean() * 100, 1)
        ft_participation_mean = round(ft_kill_mean + ft_assist_mean, 1)
        team_gold_percentage_mean = round(p_df['percentageTeamGold'].mean(), 1)
        team_dpm_percentage_mean = round(p_df['percentageTeamDpmChampions'].mean(), 1)
        winrate_mean = round(p_df['win'].mean() * 100, 1)
        wins = p_df['win'].apply(lambda x: x[x == True].count())
        losses = p_df['win'].apply(lambda x: x[x == False].count())
        pickrate = round(p_df.size(), 1)

        # Extremos
        max_kda = round(p_df['kda'].max(), 1)
        min_kda = round(p_df['kda'].min(), 1)
        max_kp = round(p_df['kp'].max(), 1)
        min_kp = round(p_df['kp'].min(), 1)
        max_fpm = round(p_df['fpm'].max(), 1)
        min_fpm = round(p_df['fpm'].min(), 1)
        max_dpm_champions = round(p_df['dpmChampions'].max(), 1)
        max_dpm_turrets = round(p_df['dpmTurrets'].min(), 1)
        min_dpm_champions = round(p_df['dpmChampions'].min(), 1)
        min_dpm_turrets = round(p_df['dpmTurrets'].min(), 1)
        max_vspm = round(p_df['vspm'].max(), 1)
        min_vspm = round(p_df['vspm'].min(), 1)
        max_percentage_gold = round(p_df['percentageTeamGold'].max(), 1)
        min_percentage_gold = round(p_df['percentageTeamGold'].min(), 1)
        max_percentage_dpm_champions = round(p_df['percentageTeamDpmChampions'].max(), 1)
        min_percentage_dpm_champions = round(p_df['percentageTeamDpmChampions'].min(), 1)
        max_gold_efficiency = round(p_df['goldEfficiency'].max(), 1)
        min_gold_efficiency = round(p_df['goldEfficiency'].min(), 1)

        max_min_dict = {
            "max_kda": max_kda,
            "min_kda": min_kda,
            "max_kp": max_kp,
            "min_kp": min_kp,
            "max_fpm": max_fpm,
            "min_fpm": min_fpm,
            "max_dpm_champions": max_dpm_champions,
            "min_dpm_champions": min_dpm_champions,
            "max_dpm_turrets": max_dpm_turrets,
            "min_dpm_turrets": min_dpm_turrets,
            "max_vspm": max_vspm,
            "min_vspm": min_vspm,
            "max_percentage_gold": max_percentage_gold,
            "min_percentage_gold": min_percentage_gold,
            "max_percentage_dpm_champions": max_percentage_dpm_champions,
            "min_percentage_dpm_champions": min_percentage_dpm_champions,
            "max_gold_efficiency": max_gold_efficiency,
            "min_gold_efficiency": min_gold_efficiency,
            "pickrate": pickrate,
            "wins": wins,
            "losses": losses
        }

        mean_dict = {
            "kp": kp_mean,
            "dpm_champion": dpm_champion_mean,
            "dpm_turret": dpm_turret_mean,
            "fpm": fpm_mean,
            "kda": kda_mean,
            "gpm": gpm_mean,
            "gold_efficiency": gold_efficiency_mean,
            "vspm": vspm_mean,
            "fb_participation": fb_participation_mean,
            "ft_participation": ft_participation_mean,
            "team_gold_percentage": team_gold_percentage_mean,
            "team_dpm_percentage": team_dpm_percentage_mean,
            "winrate": winrate_mean,
            "pickrate": pickrate,
            "wins": wins,
            "losses": losses
        }

        max_min_df = pd.DataFrame(max_min_dict)
        mean_df = pd.DataFrame(mean_dict)

        return mean_df, max_min_df

    def create_acc_radar_plot(self, acc_df):
        radar_df = acc_df[["kp","fb_participation","ft_participation"]]

        values = radar_df.iloc[0].values.tolist()
        values += values[:1]

        labels = self.__adjust_col_labels(radar_df.columns)

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            name='Porcentagem Média de Participação',
            line=dict(color='blue', width=2),
            fillcolor='rgba(0, 0, 255, 0.25)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    ticktext=['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'],
                    tickfont=dict(color='gray', size=10)
                )
            ),
            title=dict(text='Participação em Abates', x=0.5, font=dict(size=16)),
            showlegend=False
        )

        # fig.show()
        radar_json = fig.to_json()

        return radar_json
    
    def create_acc_pie_plot(self, df):
        data = df.loc[0]
        wins = data["wins"]
        losses = data["losses"]
        winrate = data["winrate"]

        labels = ['Wins', 'Losses']
        sizes = [wins, losses]
        colors = ['#4CAF50', '#F44336']

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels=labels,
            values=sizes,
            marker=dict(colors=colors),
            textinfo='percent+label',
            hole=0,
            pull=[0.1, 0]
        ))

        fig.update_layout(
            annotations=[
                dict(
                    text=f"{winrate:.1f}%",
                    x=0.5, y=0.5, font_size=20, showarrow=False, font=dict(weight='bold')
                )
            ],
            title=dict(text="Winrate", x=0.5, font=dict(size=16)),
            showlegend=False
        )

        # fig.show()
        pie_json = fig.to_json()

        return pie_json

    def __adjust_col_labels(self, table_columns):
        table_name_switch = {
            "kp": "KP",
            "dpm_champion": "DPMC",
            "dpm_turret": "DPMT",
            "fpm": "FPM",
            "kda": "KDA",
            "gpm": "GPM",
            "gold_efficiency": "GEFF",
            "vspm": "VSPM",
            "fb_participation": "FB%",
            "ft_participation": "FT%",
            "team_gold_percentage": "GOLD%",
            "team_dpm_percentage": "DMG%",
            "winrate": "Winrate%",
            "pickrate": "Pickrate",
            "wins": "Wins",
            "losses": "Losses",
            "championName": "Champion",
            "teamPosition": "Role"
        }
        
        new_table_columns = []

        for i in table_columns:
            col_name = table_name_switch.get(i,"N/D")
            new_table_columns.append(col_name)
        
        return new_table_columns

    def create_grouped_mean_table_plot(self, mean_df):
        mean_df_sorted = mean_df.sort_values(by='pickrate', ascending=False)
        mean_df_top_10 = mean_df_sorted.head(10)

        table_data = mean_df_top_10.reset_index()
        table_data.columns = self.__adjust_col_labels(table_data.columns)

        colors_gradient = ["#FF6F61", "#ffff8c", "#77DD77"]
        cmap = LinearSegmentedColormap.from_list("custom_cmap", colors_gradient)
        header_color = '#b39bd7'

        fill_colors = []
        for j, col_name in enumerate(table_data.columns):
            column_colors = []
            if j == 0:
                column_colors = [header_color] * len(table_data.index)
            elif col_name == "Wins" or col_name == "Losses":
                winrate_index = table_data.columns.get_loc('Winrate%')
                norm = Normalize(vmin=table_data['Winrate%'].min(), vmax=table_data['Winrate%'].max())
                for i in range(len(table_data.index)):
                    value = table_data.iloc[i, winrate_index]
                    color = mcolors.to_hex(cmap(norm(value)))
                    column_colors.append(color)
            else:
                norm = Normalize(vmin=table_data[col_name].min(), vmax=table_data[col_name].max())
                for i in range(len(table_data.index)):
                    value = table_data.iloc[i, j]
                    color = mcolors.to_hex(cmap(norm(value)))
                    column_colors.append(color)
            fill_colors.append(column_colors)


        header = dict(
            values=list(table_data.columns),
            fill_color=header_color,
            align='center',
            font=dict(color='white', size=12)
        )

        cells = dict(
            values=[table_data[col].tolist() for col in table_data.columns],
            fill_color=fill_colors,
            align='center',
            font=dict(color='black', size=10)
        )

        fig = go.Figure(data=[go.Table(header=header, cells=cells)])

        fig.update_layout(
            title="Grouped Mean Table",
            title_x=0.5,
            width=1200,
            height=400,
        )
        
        column_widths = [
        max(max(len(str(val)) for val in table_data[col]), len(col))
        for col in table_data.columns
        ]

        fig.data[0].columnwidth = column_widths

        # fig.show()
        table_json = fig.to_json()

        return table_json

    def create_player_analysis(self):
        all_pl_df, all_games_df, all_bans_df, all_teams_df = self.__create_dfs_classic()

        all_pl_df["totalTeamDpmChampions"] = all_pl_df.groupby(['matchId','teamId'])['dpmChampions'].transform('sum')
        all_pl_df['percentageTeamDpmChampions'] = np.round((all_pl_df['dpmChampions'] / all_pl_df["totalTeamDpmChampions"])*100, 2)

        all_pl_df["totalTeamGold"] = all_pl_df.groupby(['matchId','teamId'])['goldEarned'].transform('sum')
        all_pl_df['percentageTeamGold'] = np.round((all_pl_df['goldEarned'] / all_pl_df["totalTeamGold"])*100, 2)
        
        current_player_df = all_pl_df[all_pl_df['puuid'] == self.puuid]
        champions_current_player_df = current_player_df.groupby('championName')
        role_current_player_df = current_player_df.groupby('teamPosition')

        no_filter_mean_df, no_filter_max_min_df = self.__numerical_analysis(current_player_df)
        champion_mean_df, champion_max_min_df = self.__grouped_numerical_analysis(champions_current_player_df)
        role_mean_df, role_max_min_df = self.__grouped_numerical_analysis(role_current_player_df)

        history_dfs = {
            "players": all_pl_df,
            "games": all_games_df,
            "bans": all_bans_df,
            "teams": all_teams_df,
        }

        history_games = self.__create_player_history(history_dfs)

        dfs_dict = {
            "no_filter_mean" : no_filter_mean_df,
            "no_filter_max_min" : no_filter_max_min_df,
            "champion_mean" : champion_mean_df,
            "champion_max_min" : champion_max_min_df,
            "role_mean" : role_mean_df,
            "role_max_min" : role_max_min_df
        }

        return dfs_dict, history_games

    def __create_player_history(self, dfs):
        player_info_to_maintain_history = [
            "riotIdGameName",
            "riotIdTagline",
            "championName",
            "kills",
            "deaths",
            "assists"            
        ]

        ban_info_to_maintain_history = [
            "championId"           
        ]

        dfs["games"]["game_creation_time"] = pd.to_datetime(dfs["games"]['game_creation_time'], format='%d-%m-%Y %H:%M:%S')
        dfs["games"] = dfs["games"].sort_values(by='game_creation_time', ascending=False)

        history_games = []
        unique_game = {}

        for i in range(9):
            current_game_players = dfs["players"][dfs["players"]['matchId'] == dfs["games"].iloc[i]['matchId']]
            current_game_bans = dfs["bans"][dfs["bans"]['matchId'] == dfs["games"].iloc[i]['matchId']]
            current_game_teams = dfs["teams"][dfs["teams"]['matchId'] == dfs["games"].iloc[i]['matchId']]
            
            for j in range(len(current_game_teams)):
                team_info = []

                current_team_players_df = current_game_players[current_game_players['teamId'] == current_game_teams.iloc[j]['teamId']]
                current_team_bans_df = current_game_bans[current_game_bans['teamId'] == current_game_teams.iloc[j]['teamId']]

                player_being_analysed_df = current_team_players_df[current_team_players_df['puuid'] == self.puuid]

                if player_being_analysed_df.empty == False:
                    player_being_analysed_champion = player_being_analysed_df.iloc[0]["championName"]
                    player_being_analysed_kda = f"{player_being_analysed_df.iloc[0]['kills']} / {player_being_analysed_df.iloc[0]['deaths']} / {player_being_analysed_df.iloc[0]['assists']}"
                    player_being_analysed_win = player_being_analysed_df.iloc[0]["win"]

                current_team_players_cleaned = current_team_players_df[player_info_to_maintain_history].to_dict('records')
                current_team_bans_cleaned = current_team_bans_df[ban_info_to_maintain_history].to_dict('records')

                team_info.append(current_team_players_cleaned)
                team_info.append(current_team_bans_cleaned)

                unique_game[current_game_teams.iloc[j]['teamName']] = team_info
            
            unique_game["champion"] = player_being_analysed_champion
            unique_game["kda"] = player_being_analysed_kda
            if player_being_analysed_win:
                unique_game["match_result"] = "Win"
            else:
                unique_game["match_result"] = "Loss"
            
            history_games.append(unique_game.copy())

        return history_games