import matplotlib.pyplot as plt
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
        kp_mean = np.mean(p_df['kp'])
        dpm_champion_mean = np.mean(p_df['dpmChampions'])
        dpm_turret_mean = np.mean(p_df['dpmTurrets'])
        fpm_mean = np.mean(p_df['fpm'])
        kda_mean = np.mean(p_df['kda'])
        gpm_mean = np.mean(p_df['gpm'])
        gold_efficiency_mean = np.mean(p_df['goldEfficiency'])
        vspm_mean = np.mean(p_df['vspm'])
        fb_kill_mean = np.mean(p_df['firstBloodKill'])
        fb_assist_mean = np.mean(p_df['firstBloodAssist'])
        fb_participation_mean = fb_kill_mean + fb_assist_mean
        ft_kill_mean = np.mean(p_df['firstTowerKill'])
        ft_assist_mean = np.mean(p_df['firstTowerAssist'])
        ft_participation_mean = ft_kill_mean + ft_assist_mean
        team_gold_percentage_mean = np.mean(p_df['percentageTeamGold'])
        team_dpm_percentage_mean = np.mean(p_df['percentageTeamDpmChampions'])
        winrate_mean = np.mean(p_df["win"])
        wins = np.sum(p_df["win"])
        loses = np.sum(p_df["win"] == False)

        # Extremos
        max_kda = np.max(p_df['kda'])
        min_kda = np.min(p_df['kda'])
        max_kp = np.max(p_df['kp'])
        min_kp = np.min(p_df['kp'])
        max_fpm = np.max(p_df['fpm'])
        min_fpm = np.min(p_df['fpm'])
        max_dpm_champions = np.max(p_df['dpmChampions'])
        max_dpm_turrets = np.max(p_df['dpmTurrets'])
        min_dpm_champions = np.min(p_df['dpmChampions'])
        min_dpm_turrets = np.min(p_df['dpmTurrets'])
        max_vspm = np.max(p_df['vspm'])
        min_vspm = np.min(p_df['vspm'])
        max_percentage_gold = np.max(p_df['percentageTeamGold'])
        min_percentage_gold = np.min(p_df['percentageTeamGold'])
        max_percentage_dpm_champions = np.max(p_df['percentageTeamDpmChampions'])
        min_percentage_dpm_champions = np.min(p_df['percentageTeamDpmChampions'])
        max_gold_efficiency = np.max(p_df['goldEfficiency'])
        min_gold_efficiency = np.min(p_df['goldEfficiency'])

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
            "loses": loses
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
            "fb_kill": fb_kill_mean,
            "fb_assist": fb_assist_mean,
            "fb_participation": fb_participation_mean,
            "ft_kill": ft_kill_mean,
            "ft_assist": ft_assist_mean,
            "ft_participation": ft_participation_mean,
            "team_gold_percentage": team_gold_percentage_mean,
            "team_dpm_percentage": team_dpm_percentage_mean,
            "winrate": winrate_mean,
            "wins": wins,
            "loses": loses
        }

        max_min_df = pd.DataFrame([max_min_dict])
        mean_df = pd.DataFrame([mean_dict])

        return mean_df, max_min_df
    
    def __grouped_numerical_analysis(self, p_df):
        # Médias
        kp_mean = p_df['kp'].mean()
        dpm_champion_mean = p_df['dpmChampions'].mean()
        dpm_turret_mean = p_df['dpmTurrets'].mean()
        fpm_mean = p_df['fpm'].mean()
        kda_mean = p_df['kda'].mean()
        gpm_mean = p_df['gpm'].mean()
        gold_efficiency_mean = p_df['goldEfficiency'].mean()
        vspm_mean = p_df['vspm'].mean()
        fb_kill_mean = p_df['firstBloodKill'].mean()
        fb_assist_mean = p_df['firstBloodAssist'].mean()
        fb_participation_mean = fb_kill_mean + fb_assist_mean
        ft_kill_mean = p_df['firstTowerKill'].mean()
        ft_assist_mean = p_df['firstTowerAssist'].mean()
        ft_participation_mean = ft_kill_mean + ft_assist_mean
        team_gold_percentage_mean = p_df['percentageTeamGold'].mean()
        team_dpm_percentage_mean = p_df['percentageTeamDpmChampions'].mean()
        winrate_mean = p_df['win'].mean()
        wins = p_df['win'].apply(lambda x: x[x == True].count())
        loses = p_df['win'].apply(lambda x: x[x == False].count())
        pickrate = p_df.size()

        # Extremos
        max_kda = p_df['kda'].max()
        min_kda = p_df['kda'].min()
        max_kp = p_df['kp'].max()
        min_kp = p_df['kp'].min()
        max_fpm = p_df['fpm'].max()
        min_fpm = p_df['fpm'].min()
        max_dpm_champions = p_df['dpmChampions'].max()
        max_dpm_turrets = p_df['dpmTurrets'].min()
        min_dpm_champions = p_df['dpmChampions'].max()
        min_dpm_turrets = p_df['dpmTurrets'].min()
        max_vspm = p_df['vspm'].max()
        min_vspm = p_df['vspm'].min()
        max_percentage_gold = p_df['percentageTeamGold'].max()
        min_percentage_gold = p_df['percentageTeamGold'].min()
        max_percentage_dpm_champions = p_df['percentageTeamDpmChampions'].max()
        min_percentage_dpm_champions = p_df['percentageTeamDpmChampions'].min()
        max_gold_efficiency = p_df['goldEfficiency'].max()
        min_gold_efficiency = p_df['goldEfficiency'].min()

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
            "loses": loses
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
            "fb_kill": fb_kill_mean,
            "fb_assist": fb_assist_mean,
            "fb_participation": fb_participation_mean,
            "ft_kill": ft_kill_mean,
            "ft_assist": ft_assist_mean,
            "ft_participation": ft_participation_mean,
            "team_gold_percentage": team_gold_percentage_mean,
            "team_dpm_percentage": team_dpm_percentage_mean,
            "winrate": winrate_mean,
            "pickrate": pickrate,
            "wins": wins,
            "loses": loses
        }

        max_min_df = pd.DataFrame(max_min_dict)
        mean_df = pd.DataFrame(mean_dict)

        return mean_df, max_min_df

    def __first_blood_tower_plot(self, plot, df, indices, bar_width):
        for i, champion in enumerate(df.index):
            plot.barh(indices[i] - bar_width / 2, df.loc[champion, "fb_kill"], height=bar_width, label='First Blood Kill' if i == 0 else "", color='skyblue')

            plot.barh(indices[i] - bar_width / 2, df.loc[champion, "fb_assist"], height=bar_width, left=df.loc[champion, "fb_kill"], label='First Blood Assist' if i == 0 else "", color='dodgerblue')

            plot.barh(indices[i] + bar_width / 2, df.loc[champion, "ft_kill"], height=bar_width, label='First Tower Kill' if i == 0 else "", color='lightgreen')

            plot.barh(indices[i] + bar_width / 2, df.loc[champion, "ft_assist"], height=bar_width, left=df.loc[champion, "ft_kill"], label='First Tower Assist' if i == 0 else "", color='green')

        plot.set_yticks(indices)
        plot.set_yticklabels(df.index)
        plot.set_ylabel('Campeões')
        plot.set_xlabel('Quantidade')
        plot.set_title('Participação em First Blood e First Tower por Campeão')
        plot.legend(loc='upper right')

        return plot
    
    def __percentage_dpm_gold_plot(self, plot, df, indices, bar_width):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] - bar_width / 2, df.loc[champion, "dpm_champion"], width=bar_width, label='DPM Champion' if i == 0 else "", color='skyblue')
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "dpm_turret"], width=bar_width, label='DPM Turret' if i == 0 else "", color='dodgerblue')
        plot.plot(indices, df["gpm"], color='green', marker='o', linestyle='-', label='Gold Earned', linewidth=2)

        ax2 = plot.twinx()
        ax2.plot(indices, df["gold_efficiency"], color='red', marker='*', linestyle='', label='Gold Efficiency', linewidth=2)
        ax2.set_ylabel('Gold Efficiency')
        
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Quantidade')
        plot.set_title('Relação de Dano e Gold por Campeão')

        lines, labels = plot.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        
        lines.extend(lines2)
        labels.extend(labels2)

        ax2.legend(lines, labels, loc='upper right')

    def __winrate_plot(self, plot, df, indices, bar_width):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] - bar_width / 2, df.loc[champion, "wins"], width=bar_width, label='Wins' if i == 0 else "", color='green')
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "loses"], width=bar_width, label='Loses' if i == 0 else "", color='red')
        plot3 = plot.twinx()
        plot3.plot(indices,df["winrate"], color='blue', marker='o', linestyle='-', label='Winrate', linewidth=2)
        plot3.set_ylabel('% Winrate')

        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Quantidade Jogos')
        plot.set_title('Winrate')

    def __basic_plot(self, plot, df, indices, bar_width):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "kda"], width=bar_width, label='KDA' if i == 0 else "", color='dodgerblue')

        plot3 = plot.twinx()
        plot3.plot(indices,df["fpm"], color='red', marker='o', linestyle='-', label='Farm per Minute', linewidth=2)
        plot3.plot(indices,df["vspm"], color='purple', marker='^', linestyle='--', label='Vision Score per Minute', linewidth=2)
        plot3.set_ylabel('Farm/Vision Score per Minute')

        

        lines, labels = plot.get_legend_handles_labels()
        lines2, labels2 = plot3.get_legend_handles_labels()
        
        lines.extend(lines2)
        labels.extend(labels2)

        plot3.legend(lines, labels, loc='upper right')

        

        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Quantidade')
        plot.set_title('Relação de Dano e Gold por Campeão')

    def __team_comparison_plot(self, plot, df, indices, bar_width):
        plot.plot(indices, df["team_gold_percentage"], color='green', marker='o', linestyle='-', label='% De Gold', linewidth=2)
        plot.plot(indices, df["team_dpm_percentage"], color='orange', marker='o', linestyle='--', label='% De DPM', linewidth=2)
        plot.plot(indices, df["kp"], color='red', marker='o', linestyle='-.', label='KP', linewidth=2)
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90) 
        plot.set_ylabel('Gold | DPM | KP')
        plot.legend(loc='upper right')

    def __pickrate_plot(self, plot, df, indices, bar_width):
        # Ordenando por winrate para o Pareto
        sorted_pickrate = df['pickrate'].sort_values(ascending=False)

        # Plotando as barras de winrate
        sorted_pickrate.plot(kind='bar', color='skyblue', ax=plot)
        plot.set_ylabel('Winrate (%)')
        plot.set_xlabel('Campeões')
        plot.set_title('Pareto de Winrate por Campeão')

        # Calculando a linha de porcentagem acumulada
        cumulative_sum = sorted_pickrate.cumsum()
        cumulative_percentage = cumulative_sum / cumulative_sum.iloc[-1] * 100

        # Plotando a linha cumulativa no eixo secundário
        plot2 = plot.twinx()
        plot2.plot(cumulative_percentage, color='red', marker='D', linestyle='-', label='Cumulativo (%)')

        # Ajustando os rótulos do eixo X
        plot2.set_ylabel('Porcentagem Cumulativa (%)')

        # Garantir que o número de ticks e rótulos seja o mesmo e na ordem correta
        plot2.set_xticks(range(len(df)))  # Alinha os ticks com o número de campeões
        plot2.set_xticklabels(sorted_pickrate.index, rotation=45)  # Define os rótulos dos campeões

        plot2.legend(loc='upper right')

    def create_mean_plots(self, mean_df):
        fig, axes = plt.subplots(2, 3, figsize=(10, 6))

        bar_width = 0.35
        indices = range(len(mean_df))

        fb_plot = self.__first_blood_tower_plot(axes[0,0], mean_df, indices, bar_width)
        
        team_comparison_plot = self.__team_comparison_plot(axes[0,1], mean_df, indices, bar_width)
        
        winrate_plot = self.__winrate_plot(axes[0,2], mean_df, indices, bar_width)
        
        percentage_dpm_gold_plot = self.__percentage_dpm_gold_plot(axes[1,0], mean_df, indices, bar_width)
        
        basic_plot = self.__basic_plot(axes[1,1], mean_df, indices, bar_width)
        
        pickrate_plot = self.__pickrate_plot(axes[1,2], mean_df, indices, bar_width)

        plt.tight_layout()
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