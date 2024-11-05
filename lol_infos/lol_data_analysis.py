import matplotlib as mpl
import pandas as pd
import numpy as np
import mongo_code.db_connection as db_conn

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
            if m['game_data']['game_mode'] == "CLASSIC":
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
    
    def numerical_analysis(self):
        pass

    def create_player_analysis(self):
        all_pl_df, all_games_df, all_bans_df, all_teams_df = self.__create_dfs_classic()

        all_pl_df["totalTeamDpmChampions"] = all_pl_df.groupby(['matchId','teamId'])['dpmChampions'].transform('sum')
        all_pl_df['percentageTeamDpmChampions'] = np.round((all_pl_df['dpmChampions'] / all_pl_df["totalTeamDpmChampions"])*100, 2)

        all_pl_df["totalTeamGold"] = all_pl_df.groupby(['matchId','teamId'])['goldEarned'].transform('sum')
        all_pl_df['percentageTeamGold'] = np.round((all_pl_df['goldEarned'] / all_pl_df["totalTeamGold"])*100, 2)
        
        current_player_df = all_pl_df[all_pl_df['puuid'] == self.puuid]

        # Média de KP
        kp_mean = np.mean(current_player_df['kp'])
        print(f"KP: {kp_mean}")

        # Média de DPM em Champions
        dpm_champion_mean = np.mean(current_player_df['dpmChampions'])
        print(f"DPM Champions: {dpm_champion_mean}")

        # Média de DPM em Turrets
        dpm_turret_mean = np.mean(current_player_df['dpmTurrets'])
        print(f"DPM Turrets: {dpm_turret_mean}")

        # Média de DPM Total
        dpm_total_mean = np.mean(current_player_df['dpmTotal'])
        print(f"DPM Total: {dpm_total_mean}")

        # Média de FPM
        fpm_mean = np.mean(current_player_df['fpm'])
        print(f"FPM: {fpm_mean}")

        # Média de KDA
        kda_mean = np.mean(current_player_df['kda'])
        print(f"KDA: {kda_mean}")

        # Média de Gold Earned
        gold_earned_mean = np.mean(current_player_df['goldEarned'])
        print(f"Gold Earned: {gold_earned_mean}")

        # Média de Gold Spent
        gold_spent_mean = np.mean(current_player_df['goldSpent'])
        print(f"Gold Spent: {gold_spent_mean}")

        # Média de Gold Efficiency
        gold_efficiency_mean = np.mean(current_player_df['goldEfficiency'])
        print(f"Gold Efficiency: {gold_efficiency_mean}")

        # Média de Vision Score
        vision_score_mean = np.mean(current_player_df['visionScore'])
        print(f"Vision Score: {vision_score_mean}")

        # Média de Participação em FB
        fb_kill_mean = np.mean(current_player_df['firstBloodKill'])
        fb_assist_mean = np.mean(current_player_df['firstBloodAssist'])
        fb_participation_mean = fb_kill_mean + fb_assist_mean
        print(f"First Blood Participation: {fb_participation_mean}")

        # Média de Participação em First Tower
        ft_kill_mean = np.mean(current_player_df['firstTowerKill'])
        ft_assist_mean = np.mean(current_player_df['firstTowerAssist'])
        ft_participation_mean = ft_kill_mean + ft_assist_mean
        print(f"First Tower Participation: {ft_participation_mean}")

        # % Média de Gold da Equipe
        team_gold_percentage_mean = np.mean(current_player_df['percentageTeamGold'])
        print(f"Percentage Team Gold: {team_gold_percentage_mean}")

        # % Média de DPM da Equipe
        team_dpm_percentage_mean = np.mean(current_player_df['percentageTeamDpmChampions'])
        print(f"Percentage Team DPM Champions: {team_dpm_percentage_mean}")


        # Melhor KDA
        # Pior KDA
        # Maior KP
        # Menor KP
        # Maior FPM
        # Menor FPM
        # Maior dpm
        # Menor dpm
        # Maior vision score
        # Menor vision score
        # Maior % gold/equipe
        # Menor % gold/equipe
        # Maior % de dano/equipe
        # Menor % de dano/equipe
        # Maior gold efficiency (dano/gold)
        # Menor gold efficiency (dano/gold)



        return