import extras.ex_info as ex
import requests

# ACCOUNT-V1
# - /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine} -> Para pegar o puuid.

# SUMMONER-V4
# - /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID} -> Para pegar todas as informações da conta do usuário.

# MATCH-V5
# - /lol/match/v5/matches/by-puuid/{puuid}/ids -> Para pegar as informações de todas as partidas do usuário.

# - /lol/match/v5/matches/{matchId} -> Para pegar as informações gerais de uma partida em específico.

# - /lol/match/v5/matches/{matchId}/timeline -> Para pegar todas as informações baseadas na timeline de uma partida em específico.

# SPECTATOR-V5
# - /lol/spectator/v5/active-games/by-summoner/{encryptedPUUID} -> Para pegar as informações da partida atual do usuário.

class LolVerifier:
    def __init__(self, name, tag):
        self.n = name
        self.t = tag
        self.api = ex.my_api
        self.base_url_platform = "https://br1.api.riotgames.com"
        self.base_url_region = "https://americas.api.riotgames.com"
        self.api_params = {'api_key': self.api}

    def __check_response(self,response):
        if response.status_code == 200:
            account_info = response.json()
            return account_info
        else:
            return response.status_code
    
    def get_puuid(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self.n}/{self.t}"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    def get_acc_info(self,puuid):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"
        url = self.base_url_platform + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    def get_all_matchs(self):
        pass

    def get_match_geral_info(self):
        pass

    def get_match_timeline_info(self):
        pass

    def get_current_match(self):
        pass
