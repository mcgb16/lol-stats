import lol_infos.lol_apis as la
import basic_code.basic as basic
import lol_infos.lol_data_analysis as lda

if __name__ == "__main__":    
    pl_name, pl_tag = basic.ask_name_tag()
    
    lol_acc = la.LolVerifier(pl_name, pl_tag)
    lol_acc_puuid = lol_acc.get_puuid()
    lol_acc_infos = lol_acc.get_acc_info(lol_acc_puuid)
    lol_acc_sum_id = lol_acc_infos["id"]
    pl_elos = lol_acc.get_acc_ranks(lol_acc_sum_id)

    pl_elos_cleaned = []
    pl_elo_index = {
        "Queue" : "",
        "Tier" : "",
        "Rank" : "",
        "Lp" : "",
        "Wins" : "",
        "Losses" : ""
    }

    for i in pl_elos:
        pl_elo_index["Queue"] = i["queueType"]
        pl_elo_index["Tier"] = i["tier"]
        pl_elo_index["Rank"] = i["rank"]
        pl_elo_index["Lp"] = i["leaguePoints"]
        pl_elo_index["Wins"] = i["wins"]
        pl_elo_index["Losses"] = i["losses"]
        pl_elos_cleaned.append(pl_elo_index.copy())

    pl_history_save = basic.save_player_history(lol_acc, lol_acc_puuid)

    player_analysis = lda.AnalysePlayer(lol_acc_puuid)
    dfs_dict, history_games = player_analysis.create_player_analysis()
    basic_info_list = [pl_name,pl_tag, pl_elos_cleaned]

    player_analysis.create_acc_pie_plot(dfs_dict["no_filter_mean"])
    player_analysis.create_acc_radar_plot(dfs_dict["no_filter_mean"])
    player_analysis.create_grouped_mean_table_plot(dfs_dict["champion_mean"])
    player_analysis.create_grouped_mean_table_plot(dfs_dict["role_mean"])