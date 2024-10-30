import lol_infos.lol_apis as la
import basic_code.basic as basic

if __name__ == "__main__":
    pl_name, pl_tag = basic.ask_name_tag()

    lol_acc = la.LolVerifier(pl_name, pl_tag)
    lol_acc_puuid = lol_acc.get_puuid()

    pl_history_save = basic.save_player_history(lol_acc, lol_acc_puuid)

    print(pl_history_save)