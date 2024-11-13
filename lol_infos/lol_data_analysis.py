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
        kp_mean = round(np.mean(p_df['kp']), 1)
        dpm_champion_mean = round(np.mean(p_df['dpmChampions']), 1)
        dpm_turret_mean = round(np.mean(p_df['dpmTurrets']), 1)
        fpm_mean = round(np.mean(p_df['fpm']), 1)
        kda_mean = round(np.mean(p_df['kda']), 1)
        gpm_mean = round(np.mean(p_df['gpm']), 1)
        gold_efficiency_mean = round(np.mean(p_df['goldEfficiency']), 1)
        vspm_mean = round(np.mean(p_df['vspm']), 1)
        fb_kill_mean = round(np.mean(p_df['firstBloodKill']) * 100, 1)
        fb_assist_mean = round(np.mean(p_df['firstBloodAssist']) * 100, 1)
        fb_participation_mean = round(fb_kill_mean + fb_assist_mean, 1)
        ft_kill_mean = round(np.mean(p_df['firstTowerKill']) * 100, 1)
        ft_assist_mean = round(np.mean(p_df['firstTowerAssist']) * 100, 1)
        ft_participation_mean = round(ft_kill_mean + ft_assist_mean, 1)
        team_gold_percentage_mean = round(np.mean(p_df['percentageTeamGold']), 1)
        team_dpm_percentage_mean = round(np.mean(p_df['percentageTeamDpmChampions']), 1)
        winrate_mean = round(np.mean(p_df["win"]) * 100, 1)
        wins = np.sum(p_df["win"])
        loses = np.sum(p_df["win"] == False)

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
            "fb_participation": fb_participation_mean,
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
        loses = p_df['win'].apply(lambda x: x[x == False].count())
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
            "fb_participation": fb_participation_mean,
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

    def __first_blood_tower_plot(self, plot, df, indices, bar_width, ticks_info):
        for i, champion in enumerate(df.index):
            plot.barh(indices[i] - bar_width / 2, df.loc[champion, "fb_kill"], height=bar_width, label='First Blood Kill' if i == 0 else "", color='skyblue')

            plot.barh(indices[i] - bar_width / 2, df.loc[champion, "fb_assist"], height=bar_width, left=df.loc[champion, "fb_kill"], label='First Blood Assist' if i == 0 else "", color='dodgerblue')

            plot.barh(indices[i] + bar_width / 2, df.loc[champion, "ft_kill"], height=bar_width, label='First Tower Kill' if i == 0 else "", color='lightgreen')

            plot.barh(indices[i] + bar_width / 2, df.loc[champion, "ft_assist"], height=bar_width, left=df.loc[champion, "ft_kill"], label='First Tower Assist' if i == 0 else "", color='green')
        
        max_value = df[["fb_kill", "fb_assist", "ft_kill", "ft_assist"]].max().max()

        x_ticks = np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"])

        plot.set_xlim(ticks_info["min_value"], max_value*1.05)
        plot.set_xticks(x_ticks)
        plot.set_xticklabels([f"{tick:.0f}" for tick in x_ticks])
        plot.set_yticks(indices)
        plot.set_yticklabels(df.index)
        plot.set_ylabel('Campeões')
        plot.set_xlabel('% de Participações')
        plot.set_title('Participação em First Blood e First Tower por Campeão')
        plot.legend(loc='upper right', framealpha=0.2, fontsize=7)

        return plot
    
    def __percentage_dpm_gold_plot(self, plot, df, indices, bar_width, ticks_info):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] - bar_width / 2, df.loc[champion, "dpm_champion"], width=bar_width, label='DPM em Campeões' if i == 0 else "", color='skyblue')
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "dpm_turret"], width=bar_width, label='DPM em Torres' if i == 0 else "", color='dodgerblue')
        
        plot.plot(indices, df["gpm"], color='green', marker='o', linestyle='-', label='Gold Adquirido por Minuto', linewidth=2)

        max_value = np.ceil(df[["dpm_champion", "gpm", "dpm_turret"]].max().max())

        y_ticks = np.ceil(np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"]))

        plot.set_ylim(ticks_info["min_value"], max_value*1.05)
        plot.set_yticks(y_ticks)
        plot.set_yticklabels([f"{tick:.0f}" for tick in y_ticks])
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Valor por Minuto')
        plot.set_title('Relação de DPM e GPM por Campeão')

        plot2 = plot.twinx()
        plot2.plot(indices, df["gold_efficiency"], color='red', marker='*', linestyle='', label='Eficiência de Gold', linewidth=2)

        max_value2 = df[["gold_efficiency"]].max().max()

        y_ticks2 = np.linspace(ticks_info["min_value"], max_value2, ticks_info["num_ticks"])

        plot2.set_ylim(ticks_info["min_value"], max_value2*1.05)
        plot2.set_yticks(y_ticks2)
        plot2.set_yticklabels([f"{tick:.1f}" for tick in y_ticks2])
        plot2.set_ylabel('Eficiência de Gold (DPM/GPM)')

        lines, labels = plot.get_legend_handles_labels()
        lines2, labels2 = plot2.get_legend_handles_labels()
        
        lines.extend(lines2)
        labels.extend(labels2)

        plot2.legend(lines, labels, loc='upper right', framealpha=0.2, fontsize=7)

        return plot2

    def __winrate_plot(self, plot, df, indices, bar_width, ticks_info):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] - bar_width / 2, df.loc[champion, "wins"], width=bar_width, label='Vitórias' if i == 0 else "", color='green')
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "loses"], width=bar_width, label='Derrotas' if i == 0 else "", color='red')
        
        max_value = np.ceil(df[["wins", "loses"]].max().max())

        y_ticks = np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"])

        plot.set_ylim(ticks_info["min_value"], max_value*1.05)
        plot.set_yticks(y_ticks)
        plot.set_yticklabels([f"{tick:.0f}" for tick in y_ticks])
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Quantidade de Jogos')
        plot.set_title('Vitórias/Derrotas e Winrate por Campeão')

        plot2 = plot.twinx()
        plot2.plot(indices,df["winrate"], color='blue', marker='o', linestyle='-', label='Winrate', linewidth=2)

        max_value2 = df[["winrate"]].max().max()

        y_ticks2 = np.linspace(ticks_info["min_value"], max_value2, ticks_info["num_ticks"])

        plot2.set_ylim(ticks_info["min_value"], max_value2*1.05)
        plot2.set_yticks(y_ticks2)
        plot2.set_yticklabels([f"{tick:.0f}" for tick in y_ticks2])
        plot2.set_ylabel('% Winrate')

        lines, labels = plot.get_legend_handles_labels()
        lines2, labels2 = plot2.get_legend_handles_labels()
        
        lines.extend(lines2)
        labels.extend(labels2)

        plot2.legend(lines, labels, loc='upper right', framealpha=0.2, fontsize=7)

        return plot2

    def __basic_plot(self, plot, df, indices, bar_width, ticks_info):
        for i, champion in enumerate(df.index):
            plot.bar(indices[i] + bar_width / 2, df.loc[champion, "kda"], width=bar_width, label='KDA' if i == 0 else "", color='dodgerblue')
        plot.plot(indices,df["fpm"], color='red', marker='o', linestyle='-', label='Farm por Minuto', linewidth=2)
        plot.plot(indices,df["vspm"], color='purple', marker='^', linestyle='--', label='Placar de Visão por Minuto', linewidth=2)

        max_value = np.ceil(df[["kda", "fpm", "vspm"]].max().max())

        y_ticks = np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"])

        plot.set_ylim(ticks_info["min_value"], max_value*1.05)
        plot.set_yticks(y_ticks)
        plot.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90)
        plot.set_xlabel('Campeões')
        plot.set_ylabel('Valor')
        plot.set_title('Farm/Placar de Visão por Minuto e KDA por Campeão')

        plot.legend(loc='upper right', framealpha=0.2, fontsize=7)

        return plot

    def __team_comparison_plot(self, plot, df, indices, bar_width, ticks_info):
        plot.plot(indices, df["team_gold_percentage"], color='green', marker='o', linestyle='-', label='% De Gold', linewidth=2)
        plot.plot(indices, df["team_dpm_percentage"], color='orange', marker='o', linestyle='--', label='% De DPM', linewidth=2)
        plot.plot(indices, df["kp"], color='red', marker='o', linestyle='-.', label='KP', linewidth=2)

        max_value = df[["team_gold_percentage","team_dpm_percentage","kp"]].max().max()

        y_ticks = np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"])
        
        plot.set_ylim(ticks_info["min_value"], max_value*1.05)
        plot.set_yticks(y_ticks)
        plot.set_yticklabels([f"{tick:.0f}" for tick in y_ticks])
        plot.set_xticks(indices)
        plot.set_xticklabels(df.index, rotation=90) 
        plot.set_ylabel('Valor em %')
        plot.set_xlabel('Campeões')
        plot.set_title('Gold, Dano (em Campeões) e Participação de Kills em Relação ao Time.')
        plot.legend(loc='upper right', framealpha=0.2, fontsize=7)

        return plot

    def __pickrate_plot(self, plot, df, indices, bar_width, ticks_info):
        sorted_pickrate = df['pickrate'].sort_values(ascending=False)

        sorted_pickrate.plot(kind='bar', color='skyblue', ax=plot, label="Quantide de Jogos")

        cumulative_sum = sorted_pickrate.cumsum()
        cumulative_percentage = cumulative_sum / cumulative_sum.iloc[-1] * 100

        max_value = np.ceil(df[["pickrate"]].max().max())

        y_ticks = np.linspace(ticks_info["min_value"], max_value, ticks_info["num_ticks"])

        plot.set_ylim(ticks_info["min_value"], max_value*1.05)
        plot.set_yticks(y_ticks)
        plot.set_yticklabels([f"{tick:.0f}" for tick in y_ticks])
        plot.set_xticks(indices)
        plot.set_xticklabels(sorted_pickrate.index, rotation=90)
        plot.set_ylabel('Quantidade de Jogos')
        plot.set_xlabel('Campeões')
        plot.set_title('Pickrate por Campeão')

        plot2 = plot.twinx()
        plot2.plot(cumulative_percentage, color='red', marker='D', linestyle='-', label='Porcentagem Cumulativa (%)')
        
        max_value2 = cumulative_percentage.max().max()

        y_ticks2 = np.linspace(ticks_info["min_value"], max_value2, ticks_info["num_ticks"])

        plot2.set_ylim(ticks_info["min_value"], max_value2*1.05)
        plot2.set_yticks(y_ticks2)
        plot2.set_yticklabels([f"{tick:.0f}" for tick in y_ticks2])
        plot2.set_ylabel('Porcentagem Cumulativa (%)')
        
        lines,labels = plot.get_legend_handles_labels()
        lines2,labels2 = plot2.get_legend_handles_labels()

        lines.extend(lines2)
        labels.extend(labels2)

        plot2.legend(lines, labels, loc='upper right', framealpha=0.2, fontsize=7)

        return plot2

    def create_mean_grouped_plots(self, mean_df):
        fig, axes = plt.subplots(2, 3, figsize=(10, 6))

        mean_df_sorted = mean_df.sort_values(by='pickrate', ascending=False)
        mean_df_top_10 = mean_df_sorted.head(10)

        bar_width = 0.35
        indices = range(len(mean_df_top_10))

        ticks_info = {
            "min_value": 0,
            "num_ticks": 10
        }

        fb_plot = self.__first_blood_tower_plot(axes[0,0], mean_df_top_10, indices, bar_width, ticks_info)
        
        team_comparison_plot = self.__team_comparison_plot(axes[0,1], mean_df_top_10, indices, bar_width, ticks_info)
        
        winrate_plot = self.__winrate_plot(axes[0,2], mean_df_top_10, indices, bar_width, ticks_info)
        
        percentage_dpm_gold_plot = self.__percentage_dpm_gold_plot(axes[1,0], mean_df_top_10, indices, bar_width, ticks_info)
        
        basic_plot = self.__basic_plot(axes[1,1], mean_df_top_10, indices, bar_width, ticks_info)
        
        pickrate_plot = self.__pickrate_plot(axes[1,2], mean_df_top_10, indices, bar_width, ticks_info)

        for ax in axes.flat:
            ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.tight_layout()
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
            "fb_participation": "FB",
            "ft_participation": "FT",
            "team_gold_percentage": "GOLD%",
            "team_dpm_percentage": "DMG%",
            "winrate": "Winrate",
            "pickrate": "Pickrate",
            "wins": "Wins",
            "loses": "Loses",
            "championName": "Champion"
        }
        
        new_table_columns = []

        for i in table_columns:
            col_name = table_name_switch.get(i,"N/D")
            new_table_columns.append(col_name)
        
        return new_table_columns

    def create_champion_mean_table_plot(self, mean_df):
        fig, ax = plt.subplots(figsize=(10,6))

        ax.axis("off")

        mean_df_sorted = mean_df.sort_values(by='pickrate', ascending=False)
        mean_df_top_10 = mean_df_sorted.head(10)

        table_data = mean_df_top_10.reset_index()
        col_widths = [0.05] * len(table_data.columns)

        table_data.columns = self.__adjust_col_labels(table_data.columns)

        table = ax.table(
            cellText=table_data.values,
            colLabels=table_data.columns,
            cellLoc='center',
            loc='center',
        )
        table.auto_set_column_width(col=list(range(len(mean_df_top_10.columns))))
        table.set_fontsize(10)
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