from flask import Flask, render_template, request
import lol_infos.lol_data_cleaning as ldc
import lol_infos.lol_apis as la
import basic_code.basic as basic
import lol_infos.lol_data_analysis as lda

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis-page', methods=['POST'])
def get_player_name_tag():
    pl_name = request.form['player_name']
    pl_tag = request.form['player_tag']

    api_basic = basic.apis_basic_info(pl_name, pl_tag)

    pl_elos = ldc.clean_elo_data(api_basic["lol_acc"], api_basic["sum_id"])

    pl_history_save = basic.save_player_history(api_basic["lol_acc"], api_basic["puuid"])

    player_analysis = lda.AnalysePlayer(api_basic["puuid"])
    dfs_dict, history_games = player_analysis.create_player_analysis()
    basic_info_list = [pl_name,pl_tag, pl_elos]

    pie_plot_json = player_analysis.create_acc_pie_plot(dfs_dict["no_filter_mean"])
    radar_plot_json = player_analysis.create_acc_radar_plot(dfs_dict["no_filter_mean"])
    champ_table_json = player_analysis.create_grouped_mean_table_plot(dfs_dict["champion_mean"])
    role_table_json = player_analysis.create_grouped_mean_table_plot(dfs_dict["role_mean"])

    return render_template('analysis.html',
                           pie_plot_json=pie_plot_json,
                           radar_plot_json=radar_plot_json,
                           champ_table_json=champ_table_json,
                           role_table_json=role_table_json,
                           history_games=history_games
                           )

app.run(debug=True)