import tkinter as tk
from tkinter import ttk
import lol_infos.lol_apis as la
import basic_code.basic as basic
import lol_infos.lol_data_analysis as lda
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LolStatsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lol Stats")
        self.root.geometry(f"1280x720")

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.container = tk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.create_window((0, 0), window=self.container, anchor="nw")

        self.container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def main_page(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        tk.Label(self.container, text="Name").grid(row=0, column=0, padx=10, pady=10)
        self.name_input = tk.Entry(self.container)
        self.name_input.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.container, text="Tag").grid(row=1, column=0, padx=10, pady=10)
        self.tag_input = tk.Entry(self.container)
        self.tag_input.grid(row=1, column=1, padx=10, pady=10)

        self.search_lol_acc_bttn = tk.Button(self.container, text="Enviar", command=self.__execute_basic_analysis)
        self.search_lol_acc_bttn.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.container.mainloop()

    def analysis_page(self, dfs_dict, basic_info_list, history_games):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.top_frame = tk.Frame(self.container, height=300)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.middle_frame = tk.Frame(self.container, height=300)
        self.middle_frame.grid(row=1, column=0, sticky="ew")

        self.bottom_frame = tk.Frame(self.container, height=100)
        self.bottom_frame.grid(row=2, column=0, sticky="ew")

        self.__create_basic_info(basic_info_list)
        self.__create_carousel(dfs_dict)
        self.__create_history(history_games)

    def __create_basic_info(self, basic_info_list):
        pl_name, pl_tag, pl_elos = basic_info_list

        pl_name_output = tk.Label(self.top_frame,text=pl_name).grid(row=0, column=0, padx=10, pady=10)
        pl_tag_output = tk.Label(self.top_frame,text=pl_tag).grid(row=0, column=1, padx=10, pady=10)

        if len(pl_elos) > 0:
            for i in range(len(pl_elos)):
                pl_queue = tk.Label(self.top_frame,text=pl_elos[i]["Queue"]).grid(row=i + 1, column=0, padx=10, pady=10)
                pl_tier = tk.Label(self.top_frame,text=pl_elos[i]["Tier"]).grid(row=i + 1, column=1, padx=10, pady=10)
                pl_rank = tk.Label(self.top_frame,text=pl_elos[i]["Rank"]).grid(row=i + 1, column=2, padx=10, pady=10)
                pl_lp = tk.Label(self.top_frame,text=pl_elos[i]["Lp"]).grid(row=i + 1, column=3, padx=10, pady=10)
                pl_wins = tk.Label(self.top_frame,text=pl_elos[i]["Wins"]).grid(row=i + 1, column=4, padx=10, pady=10)
                pl_losses = tk.Label(self.top_frame,text=pl_elos[i]["Losses"]).grid(row=i + 1, column=5, padx=10, pady=10)
        else:
            pass
         
    def __create_carousel(self, dfs_dict):
        self.tables = []
        self.current_table_index = 0

        self.__create_tables(dfs_dict)
        
        btn_prev = tk.Button(self.middle_frame, text="Anterior", command=self.__show_previous_table)
        btn_prev.pack(side="left", padx=10)

        self.table_container = tk.Frame(self.middle_frame)
        self.table_container.pack(fill="both", expand=True)

        btn_next = tk.Button(self.middle_frame, text="Próximo", command=self.__show_next_table)
        btn_next.pack(side="right", padx=10)

        self.__show_table(0)
    
    def __create_tables(self, dfs_dict):
        pl_analysis = lda.AnalysePlayer(self.lol_acc_puuid)
        fig = pl_analysis.create_grouped_mean_table_plot(dfs_dict["champion_mean"])
        fig2 = pl_analysis.create_grouped_mean_table_plot(dfs_dict["role_mean"])
        self.tables.append(fig)
        self.tables.append(fig2)

    def __show_table(self, index):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        fig = self.tables[index]
        canvas = FigureCanvasTkAgg(fig, master=self.table_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def __show_next_table(self):
        self.current_table_index = (self.current_table_index + 1) % len(self.tables)
        self.__show_table(self.current_table_index)

    def __show_previous_table(self):
        self.current_table_index = (self.current_table_index - 1) % len(self.tables)
        self.__show_table(self.current_table_index)

    def __execute_basic_analysis(self):
        pl_name = self.name_input.get()
        pl_tag = self.tag_input.get()
        
        lol_acc = la.LolVerifier(pl_name, pl_tag)
        self.lol_acc_puuid = lol_acc.get_puuid()
        lol_acc_infos = lol_acc.get_acc_info(self.lol_acc_puuid)
        self.lol_acc_sum_id = lol_acc_infos["id"]
        pl_elos = lol_acc.get_acc_ranks(self.lol_acc_sum_id)

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

        pl_history_save = basic.save_player_history(lol_acc, self.lol_acc_puuid)

        player_analysis = lda.AnalysePlayer(self.lol_acc_puuid)
        dfs_dict, history_games = player_analysis.create_player_analysis()
        basic_info_list = [pl_name,pl_tag, pl_elos_cleaned]

        self.analysis_page(dfs_dict, basic_info_list, history_games)
        
        return
