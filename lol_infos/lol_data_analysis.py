import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
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

        fig, ax = plt.subplots(figsize=(10,6), subplot_kw=dict(polar=True))
        num_vars = len(radar_df.columns)

        values = radar_df.iloc[0].values.tolist()
        values += values[:1]

        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        ax.fill(angles, values, color='blue', alpha=0.25)
        ax.plot(angles, values, color='blue', linewidth=2)

        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], color='gray', fontsize=10)

        labels = self.__adjust_col_labels(radar_df.columns)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=12)

        ax.set_title("Participação em Abates", fontsize=16, pad=20)
        
        plt.show()

        return
    
    def create_acc_pie_plot(self, df):
        wins = df.loc[0,"wins"]
        losses = df.loc[0,"losses"]
        winrate = df.loc[0,"winrate"]

        labels = ['Wins', 'Losses']
        sizes = [wins, losses]
        colors = ['#4CAF50', '#F44336']
        explode = (0.1, 0)            

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(sizes, labels=labels, autopct=lambda p: f"{np.round(p/100.*np.sum(sizes), 0):.0f}", startangle=90, colors=colors, explode=explode)

        ax.text(0, 0, f"{winrate:.1f}%", ha='center', va='center', fontsize=20, fontweight='bold')
        ax.set_title("Winrate", fontsize=16, pad=20)

        plt.show()

        return

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
        fig, ax = plt.subplots(figsize=(10,6))

        ax.axis("off")

        mean_df_sorted = mean_df.sort_values(by='pickrate', ascending=False)
        mean_df_top_10 = mean_df_sorted.head(10)

        table_data = mean_df_top_10.reset_index()

        table_data.columns = self.__adjust_col_labels(table_data.columns)

        table = ax.table(
            cellText=table_data.values,
            colLabels=table_data.columns,
            cellLoc='center',
            loc='center',
        )
        table.auto_set_column_width(col=list(range(len(mean_df_top_10.columns))))
        table.set_fontsize(10)
        
        colors_gradient = ["#FF6F61", "#ffff8c", "#77DD77"]
        cmap = LinearSegmentedColormap.from_list("custom_cmap", colors_gradient)

        for j, col_name in enumerate(table_data.columns):
            if j == 0:
                continue
            
            if col_name == "Wins" or col_name == "Losses":
                winrate_index = table_data.columns.get_loc('Winrate%')
                norm = mcolors.Normalize(vmin=table_data['Winrate%'].min(), vmax=table_data['Winrate%'].max())
                for i in range(1, len(table_data.index) + 1):
                    value = table_data.iloc[i - 1, winrate_index]
                    color = cmap(norm(value))
                    table[i, j].set_facecolor(color)
            else:
                norm = mcolors.Normalize(vmin=table_data[col_name].min(), vmax=table_data[col_name].max())
                for i in range(1, len(table_data.index) + 1):
                    value = table_data.iloc[i - 1, j]
                    color = cmap(norm(value))
                    table[i, j].set_facecolor(color)

        header_color = '#b39bd7'
        for j in range(len(table_data.columns)):
            table[0, j].set_facecolor(header_color)
        for i in range(1, len(table_data.index) + 1):
            table[i, 0].set_facecolor(header_color)

        plt.show()

        return

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

        dfs_dict = {
            "no_filter_mean" : no_filter_mean_df,
            "no_filter_max_min" : no_filter_max_min_df,
            "champion_mean" : champion_mean_df,
            "champion_max_min" : champion_max_min_df,
            "role_mean" : role_mean_df,
            "role_max_min" : role_max_min_df
        }

        return dfs_dict