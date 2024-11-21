import tkinter as tk
import lol_infos.lol_apis as la
import basic_code.basic as basic
import lol_infos.lol_data_analysis as lda

class LolStatsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lol Stats")
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

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

    def analysis_page(self, dict):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        return

    def __execute_basic_analysis(self):
        pl_name = self.name_input.get()
        pl_tag = self.tag_input.get()
        
        lol_acc = la.LolVerifier(pl_name, pl_tag)
        lol_acc_puuid = lol_acc.get_puuid()

        pl_history_save = basic.save_player_history(lol_acc, lol_acc_puuid)

        player_analysis = lda.AnalysePlayer(lol_acc_puuid)

        dfs_dict = player_analysis.create_player_analysis()

        self.analysis_page(dfs_dict)
        
        return