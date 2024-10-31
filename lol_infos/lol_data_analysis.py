import matplotlib as mpl
import pandas as pd
import numpy as np
import mongo_code.db_connection as db_conn

class AnalysePlayer:
    def __init__(self, puuid):
        self.puuid = puuid

    def __create_dfs(self):
        match_history = db_conn.find_player_history(self.puuid)

        if match_history == []:
            return None
        
        player_info_df = pd.DataFrame()
        game_info_df = pd.DataFrame()
        bans_info_df = pd.DataFrame()
        teams_info_df = pd.DataFrame()

        for m in match_history:
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
        
        return player_info_df, game_info_df, bans_info_df, teams_info_df
    
    def numerical_analysis(self):
        pass

    def create_player_analysis(self):
        all_pl_df, all_games_df, all_bans_df, all_teams_df = self.__create_dfs()

        return