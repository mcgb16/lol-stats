import extras.ex_info as ex
import requests

class LolVerifier:
    def __init__(self, name, tag):
        self.n = name
        self.t = tag
        self.api = ex.my_api
        self.base_url_platform = "https://br1.api.riotgames.com"
        self.base_url_region = "https://americas.api.riotgames.com"
        self.api_params = {'api_key': self.api}

    # Checa se o resultado da API foi o esperado.
    def __check_response(self,response):
        if response.status_code == 200:
            api_info = response.json()
            return api_info
        else:
            raise Exception(f"Erro {response.status_code} na API.")
    
    # Para pegar o puuid.
    def get_puuid(self):
        endpoint = f"/riot/account/v1/accounts/by-riot-id/{self.n}/{self.t}"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        puuid = response_checked['puuid']

        return puuid

    # Para pegar todas as informações da conta do usuário.
    # Ainda não usada.
    def get_acc_info(self,puuid):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{puuid}"
        url = self.base_url_platform + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    # Para pegar as informações de todas as partidas do usuário (padrão vem as últimas 20).
    def get_all_matchs(self, puuid):
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    # Para pegar as informações gerais de uma partida em específico.
    def get_match_geral_info(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    # Para pegar todas as informações baseadas na timeline de uma partida em específico.
    # Ainda não usada.
    def get_match_timeline_info(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}/timeline"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked

    # Para pegar as informações da partida atual do usuário.
    # Ainda não usada.
    def get_current_match(self, puuid):
        endpoint = f"/lol/spectator/v5/active-games/by-summoner/{puuid}"
        url = self.base_url_region + endpoint
        response = requests.get(url, params=self.api_params)

        response_checked = self.__check_response(response)

        return response_checked
