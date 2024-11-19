import lol_infos.lol_apis as la
import basic_code.basic as basic
import lol_infos.lol_data_analysis as lda
import tk_layout.app_layout as app

if __name__ == "__main__":
    pl_name, pl_tag = basic.ask_name_tag()

    lol_acc = la.LolVerifier(pl_name, pl_tag)
    lol_acc_puuid = lol_acc.get_puuid()

    pl_history_save = basic.save_player_history(lol_acc, lol_acc_puuid)

    player_analysis = lda.AnalysePlayer(lol_acc_puuid)

    dfs_dict = player_analysis.create_player_analysis()

    player_analysis.create_acc_pie_plot(dfs_dict["no_filter_mean"])
    player_analysis.create_acc_radar_plot(dfs_dict["no_filter_mean"])
    player_analysis.create_grouped_mean_table_plot(dfs_dict["champion_mean"])
    player_analysis.create_grouped_mean_table_plot(dfs_dict["role_mean"])