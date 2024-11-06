import matplotlib as mpl
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
    
    def __numerical_analysis(self, player_df):
        # Médias
        kp_mean = np.mean(player_df['kp'])
        dpm_champion_mean = np.mean(player_df['dpmChampions'])
        dpm_turret_mean = np.mean(player_df['dpmTurrets'])
        dpm_total_mean = np.mean(player_df['dpmTotal'])
        fpm_mean = np.mean(player_df['fpm'])
        kda_mean = np.mean(player_df['kda'])
        gold_earned_mean = np.mean(player_df['goldEarned'])
        gold_spent_mean = np.mean(player_df['goldSpent'])
        gold_efficiency_mean = np.mean(player_df['goldEfficiency'])
        vision_score_mean = np.mean(player_df['visionScore'])
        fb_kill_mean = np.mean(player_df['firstBloodKill'])
        fb_assist_mean = np.mean(player_df['firstBloodAssist'])
        fb_participation_mean = fb_kill_mean + fb_assist_mean
        ft_kill_mean = np.mean(player_df['firstTowerKill'])
        ft_assist_mean = np.mean(player_df['firstTowerAssist'])
        ft_participation_mean = ft_kill_mean + ft_assist_mean
        team_gold_percentage_mean = np.mean(player_df['percentageTeamGold'])
        team_dpm_percentage_mean = np.mean(player_df['percentageTeamDpmChampions'])

        # Extremos
        max_kda = np.max(player_df['kda'])
        min_kda = np.min(player_df['kda'])
        max_kp = np.max(player_df['kp'])
        min_kp = np.min(player_df['kp'])
        max_fpm = np.max(player_df['fpm'])
        min_fpm = np.min(player_df['fpm'])
        max_dpm_champions = np.max(player_df['dpmChampions'])
        max_dpm_turrets = np.max(player_df['dpmTurrets'])
        min_dpm_champions = np.min(player_df['dpmChampions'])
        min_dpm_turrets = np.min(player_df['dpmTurrets'])
        max_vision_score = np.max(player_df['visionScore'])
        min_vision_score = np.min(player_df['visionScore'])
        max_percentage_gold = np.max(player_df['percentageTeamGold'])
        min_percentage_gold = np.min(player_df['percentageTeamGold'])
        max_percentage_dpm_champions = np.max(player_df['percentageTeamDpmChampions'])
        min_percentage_dpm_champions = np.min(player_df['percentageTeamDpmChampions'])
        max_gold_efficiency = np.max(player_df['goldEfficiency'])
        min_gold_efficiency = np.min(player_df['goldEfficiency'])

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
            "max_vision_score": max_vision_score,
            "min_vision_score": min_vision_score,
            "max_percentage_gold": max_percentage_gold,
            "min_percentage_gold": min_percentage_gold,
            "max_percentage_dpm_champions": max_percentage_dpm_champions,
            "min_percentage_dpm_champions": min_percentage_dpm_champions,
            "max_gold_efficiency": max_gold_efficiency,
            "min_gold_efficiency": min_gold_efficiency
        }

        mean_dict = {
            "kp": kp_mean,
            "dpm_champion": dpm_champion_mean,
            "dpm_turret": dpm_turret_mean,
            "dpm_total": dpm_total_mean,
            "fpm": fpm_mean,
            "kda": kda_mean,
            "gold_earned": gold_earned_mean,
            "gold_spent": gold_spent_mean,
            "gold_efficiency": gold_efficiency_mean,
            "vision_score": vision_score_mean,
            "fb_kill": fb_kill_mean,
            "fb_assist": fb_assist_mean,
            "fb_participation": fb_participation_mean,
            "ft_kill": ft_kill_mean,
            "ft_assist": ft_assist_mean,
            "ft_participation": ft_participation_mean,
            "team_gold_percentage": team_gold_percentage_mean,
            "team_dpm_percentage": team_dpm_percentage_mean
        }

        max_min_df = pd.DataFrame([max_min_dict])
        mean_df = pd.DataFrame([mean_dict])

        return mean_df, max_min_df
    
    def __grouped_numerical_analysis(self, player_df):
        # Médias
        kp_mean = player_df['kp'].mean()
        dpm_champion_mean = player_df['dpmChampions'].mean()
        dpm_turret_mean = player_df['dpmTurrets'].mean()
        dpm_total_mean = player_df['dpmTotal'].mean()
        fpm_mean = player_df['fpm'].mean()
        kda_mean = player_df['kda'].mean()
        gold_earned_mean = player_df['goldEarned'].mean()
        gold_spent_mean = player_df['goldSpent'].mean()
        gold_efficiency_mean = player_df['goldEfficiency'].mean()
        vision_score_mean = player_df['visionScore'].mean()
        fb_kill_mean = player_df['firstBloodKill'].mean()
        fb_assist_mean = player_df['firstBloodAssist'].mean()
        fb_participation_mean = fb_kill_mean + fb_assist_mean
        ft_kill_mean = player_df['firstTowerKill'].mean()
        ft_assist_mean = player_df['firstTowerAssist'].mean()
        ft_participation_mean = ft_kill_mean + ft_assist_mean
        team_gold_percentage_mean = player_df['percentageTeamGold'].mean()
        team_dpm_percentage_mean = player_df['percentageTeamDpmChampions'].mean()

        # Extremos
        max_kda = player_df['kda'].max()
        min_kda = player_df['kda'].min()
        max_kp = player_df['kp'].max()
        min_kp = player_df['kp'].min()
        max_fpm = player_df['fpm'].max()
        min_fpm = player_df['fpm'].min()
        max_dpm_champions = player_df['dpmChampions'].max()
        max_dpm_turrets = player_df['dpmTurrets'].min()
        min_dpm_champions = player_df['dpmChampions'].max()
        min_dpm_turrets = player_df['dpmTurrets'].min()
        max_vision_score = player_df['visionScore'].max()
        min_vision_score = player_df['visionScore'].min()
        max_percentage_gold = player_df['percentageTeamGold'].max()
        min_percentage_gold = player_df['percentageTeamGold'].min()
        max_percentage_dpm_champions = player_df['percentageTeamDpmChampions'].max()
        min_percentage_dpm_champions = player_df['percentageTeamDpmChampions'].min()
        max_gold_efficiency = player_df['goldEfficiency'].max()
        min_gold_efficiency = player_df['goldEfficiency'].min()

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
            "max_vision_score": max_vision_score,
            "min_vision_score": min_vision_score,
            "max_percentage_gold": max_percentage_gold,
            "min_percentage_gold": min_percentage_gold,
            "max_percentage_dpm_champions": max_percentage_dpm_champions,
            "min_percentage_dpm_champions": min_percentage_dpm_champions,
            "max_gold_efficiency": max_gold_efficiency,
            "min_gold_efficiency": min_gold_efficiency
        }

        mean_dict = {
            "kp": kp_mean,
            "dpm_champion": dpm_champion_mean,
            "dpm_turret": dpm_turret_mean,
            "dpm_total": dpm_total_mean,
            "fpm": fpm_mean,
            "kda": kda_mean,
            "gold_earned": gold_earned_mean,
            "gold_spent": gold_spent_mean,
            "gold_efficiency": gold_efficiency_mean,
            "vision_score": vision_score_mean,
            "fb_kill": fb_kill_mean,
            "fb_assist": fb_assist_mean,
            "fb_participation": fb_participation_mean,
            "ft_kill": ft_kill_mean,
            "ft_assist": ft_assist_mean,
            "ft_participation": ft_participation_mean,
            "team_gold_percentage": team_gold_percentage_mean,
            "team_dpm_percentage": team_dpm_percentage_mean
        }

        max_min_df = pd.DataFrame(max_min_dict)
        mean_df = pd.DataFrame(mean_dict)

        return mean_df, max_min_df

    def create_player_analysis(self):
        all_pl_df, all_games_df, all_bans_df, all_teams_df = self.__create_dfs_classic()

        all_pl_df["totalTeamDpmChampions"] = all_pl_df.groupby(['matchId','teamId'])['dpmChampions'].transform('sum')
        all_pl_df['percentageTeamDpmChampions'] = np.round((all_pl_df['dpmChampions'] / all_pl_df["totalTeamDpmChampions"])*100, 2)

        all_pl_df["totalTeamGold"] = all_pl_df.groupby(['matchId','teamId'])['goldEarned'].transform('sum')
        all_pl_df['percentageTeamGold'] = np.round((all_pl_df['goldEarned'] / all_pl_df["totalTeamGold"])*100, 2)
        
        current_player_df = all_pl_df[all_pl_df['puuid'] == self.puuid]

        champions_current_player_df = current_player_df.groupby('championName')

        no_filter_mean_df, no_filter_max_min_df = self.__numerical_analysis(current_player_df)
        champion_mean_df, champion_max_min_df = self.__grouped_numerical_analysis(champions_current_player_df)

        return 