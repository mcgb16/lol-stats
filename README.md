# Documentação do Projeto "Lol Stats"

Este projeto utiliza as APIs do Riot Games para coletar e analisar dados de partidas de League of Legends, fornecendo visualizações e insights sobre o desempenho de um jogador. O projeto utiliza um banco de dados MongoDB para armazenar dados das partidas e informações auxiliares, como nomes de itens, campeões, runas, etc.

## Estrutura do Projeto

O projeto é organizado em módulos para facilitar a manutenção e o desenvolvimento:

- **`basic_code.basic`**: Contém funções utilitárias para manipulação de dados, conversões de tempo e data, e outras funções auxiliares.
- **`lol_infos.lol_apis`**: Responsável pela comunicação com as APIs do Riot Games, fornecendo métodos para buscar informações de jogadores e partidas.
- **`lol_infos.lol_data_cleaning`**: Realiza a limpeza, organização e transformação dos dados brutos da API em um formato adequado para análise.
- **`lol_infos.lol_data_analysis`**: Contém a lógica para analisar os dados processados e gerar visualizações como gráficos e tabelas.
- **`mongo_code.db_connection`**: Gerencia a conexão e as operações com o banco de dados MongoDB.
- **`main.py`**: Arquivo principal que orquestra a execução do projeto.

## Descrição dos Módulos e suas Funcionalidades

### `basic_code.basic`

##### **`apis_basic_info(pl_name, pl_tag)`**
Obtém informações básicas da conta do jogador.
- **Parâmetros:**
  - `pl_name` (str): Nome de invocador do jogador.
  - `pl_tag` (str): Tag do jogador.
- **Retorno:** Dicionário contendo o objeto `LolVerifier`, PUUID e Summoner ID.

##### **`calculate_time_seconds(sec_time)`**
Converte segundos para o formato minutos:segundos.
- **Parâmetros:**
  - `sec_time` (int): Tempo em segundos.
- **Retorno:** String representando o tempo no formato `MM:SS`.

##### **`calculate_timestamps(timestamp_milliseconds)`**
Converte um timestamp em milissegundos para o formato de data e hora.
- **Parâmetros:**
  - `timestamp_milliseconds` (int): Timestamp em milissegundos.
- **Retorno:** String representando a data e hora no formato `DD-MM-YYYY HH:MM:SS`.

##### **`sum_data(initial_data, sum_time)`**
Soma um tempo a uma data inicial.
- **Parâmetros:**
  - `initial_data` (str): Data inicial no formato `DD-MM-YYYY HH:MM:SS`.
  - `sum_time` (str): Tempo a ser somado no formato `MM:SS`.
- **Retorno:** Data final formatada como string `DD-MM-YYYY HH:MM:SS`.

##### **`ask_name_tag()`**
**(Deprecated)** Solicita o nome e tag do jogador via input.

##### **`save_player_history(lol_acc, lol_acc_puuid)`**
Salva o histórico de partidas do jogador no banco de dados.
- **Parâmetros:**
  - `lol_acc` (LolVerifier): Objeto da classe LolVerifier.
  - `lol_acc_puuid` (str): PUUID do jogador.
- **Retorno:** Resultado da operação de salvamento no banco de dados.

##### **`check_invalid_game(game_duration)`**
Verifica se a duração da partida é válida (maior que 15 minutos).
- **Parâmetros:**
  - `game_duration` (str): Duração da partida no formato `MM:SS`.
- **Retorno:** String `"valid"` ou `"invalid"`.

---

### `lol_infos.lol_apis`

#### **`class LolVerifier(name, tag)`**
Classe para interagir com as APIs do Riot Games.
- **Parâmetros:**
  - `name` (str): Nome de invocador do jogador.
  - `tag` (str): Tag do jogador.

#### **`LolVerifier.get_puuid()`**
Retorna o PUUID do jogador.
- **Retorno:** PUUID do jogador (string).

#### **`LolVerifier.get_acc_info(puuid)`**
Retorna informações da conta do jogador.
- **Parâmetros:**
  - `puuid` (str): PUUID do jogador.
- **Retorno:** Dicionário com as informações da conta.

#### **`LolVerifier.get_acc_ranks(sum_id)`**
Retorna as informações de ranking do jogador.
- **Parâmetros:**
  - `sum_id` (str): Summoner ID do jogador.
- **Retorno:** Lista de dicionários com informações de ranking em diferentes filas.

#### **`LolVerifier.get_all_matchs(puuid)`**
Retorna uma lista de IDs de partidas do jogador.
- **Parâmetros:**
  - `puuid` (str): PUUID do jogador.
- **Retorno:** Lista de IDs de partidas.

#### **`LolVerifier.get_match_geral_info(match_id)`**
Retorna informações detalhadas de uma partida.
- **Parâmetros:**
  - `match_id` (str): ID da partida.
- **Retorno:** Dicionário com as informações da partida.

#### **`LolVerifier.get_match_timeline_info(match_id)`**
**(Não utilizada)** Destinada a retornar informações da timeline da partida.

#### **`LolVerifier.get_current_match(puuid)`**
**(Não utilizada)** Destinada a retornar informações da partida em andamento.

---

### `lol_infos.lol_data_cleaning`

#### **`organize_match_geral_data(match_dict)`**
Organiza os dados brutos da partida em um dicionário estruturado.
- **Parâmetros:**
  - `match_dict` (dict): Dicionário contendo os dados brutos da partida.
- **Retorno:** Dicionário com os dados organizados.

#### **`clean_teams_data(teams_data)`**
Limpa e processa os dados dos times.
- **Parâmetros:**
  - `teams_data` (dict): Dicionário contendo os dados dos times.
- **Retorno:** Dicionário com os dados dos times limpos e processados.

#### **`clean_players_data(players_data)`**
Limpa e processa os dados dos jogadores.
- **Parâmetros:**
  - `players_data` (list): Lista contendo os dados dos jogadores.
- **Retorno:** Lista com os dados dos jogadores limpos e processados.

#### **`clean_game_data(game_data)`**
Limpa e formata os dados gerais da partida.
- **Parâmetros:**
  - `game_data` (dict): Dicionário contendo os dados gerais da partida.
- **Retorno:** Dicionário com os dados limpos e formatados.

#### **`clean_elo_data(lol_acc, acc_sum_id)`**
Processa os dados de elo do jogador.
- **Parâmetros:**
  - `lol_acc` (LolVerifier): Objeto da classe LolVerifier.
  - `acc_sum_id` (str): Summoner ID do jogador.
- **Retorno:** Lista de dicionários contendo informações de elo.

#### **`organize_match_timeline_data(match_dict)`**
**(Não implementada)**  Função prevista para processar os dados da timeline da partida.

---

### `lol_infos.lol_data_analysis`

#### **`class AnalysePlayer(puuid)`**
Classe responsável por analisar os dados de um jogador específico.

- **Parâmetros:**
  - `puuid` (str): O PUUID do jogador a ser analisado.

#### **`AnalysePlayer.__create_dfs_classic()`**
Cria DataFrames a partir do histórico de partidas do jogador no modo clássico.  Filtra partidas válidas (com duração superior a 15 minutos) e as organiza em DataFrames separados para informações do jogador, informações da partida, bans e times.

- **Retorno:**
    - `player_info_df` (DataFrame): DataFrame contendo informações dos jogadores em cada partida.
    - `game_info_df` (DataFrame): DataFrame com informações gerais de cada partida.
    - `bans_info_df` (DataFrame): DataFrame com informações sobre os bans de cada partida.
    - `teams_info_df` (DataFrame): DataFrame com informações sobre os times em cada partida.
    - `None`: Se o jogador não tiver histórico de partidas.

#### **`AnalysePlayer.__numerical_analysis(p_df)`**
Calcula estatísticas numéricas descritivas, como médias e valores extremos (mínimo e máximo), a partir de um DataFrame contendo dados do jogador (`p_df`).  As estatísticas calculadas incluem KP, participação em First Blood, participação em First Tower, Winrate, KDA, FPM, DPM, VSPM, participação no ouro do time, entre outras.

- **Parâmetros:**
  - `p_df` (DataFrame): DataFrame contendo os dados do jogador a serem analisados.

- **Retorno:**
    - `mean_df` (DataFrame): DataFrame contendo as médias das estatísticas calculadas.
    - `max_min_df` (DataFrame): DataFrame contendo os valores mínimos e máximos das estatísticas calculadas.

#### **`AnalysePlayer.__grouped_numerical_analysis(p_df)`**
Calcula estatísticas numéricas descritivas, semelhante a `__numerical_analysis`, mas agrupadas por uma determinada característica, como campeão ou função (role).  Isso permite comparar o desempenho do jogador com diferentes campeões ou em diferentes funções.

- **Parâmetros:**
  - `p_df` (DataFrame): DataFrame contendo os dados do jogador agrupados (ex: por campeão).

- **Retorno:**
    - `mean_df` (DataFrame): DataFrame contendo as médias das estatísticas calculadas, agrupadas pela característica especificada.
    - `max_min_df` (DataFrame): DataFrame contendo os valores mínimos e máximos das estatísticas calculadas, agrupadas pela característica especificada.

#### **`AnalysePlayer.create_acc_radar_plot(acc_df)`**
Gera um gráfico de radar mostrando a participação do jogador em abates (KP), First Blood (FB) e First Tower (FT).  O gráfico permite visualizar o desempenho do jogador nessas três métricas importantes.

- **Parâmetros:**
  - `acc_df` (DataFrame): DataFrame contendo os dados do jogador.

- **Retorno:** None. Exibe o gráfico gerado.

#### **`AnalysePlayer.create_acc_pie_plot(df)`**
Gera um gráfico de pizza exibindo a winrate (taxa de vitórias) do jogador.  O gráfico mostra a proporção de vitórias e derrotas do jogador.

- **Parâmetros:**
  - `df` (DataFrame): DataFrame contendo os dados do jogador, incluindo o número de vitórias e derrotas.

- **Retorno:**  None. Exibe o gráfico gerado.

#### **`AnalysePlayer.__adjust_col_labels(table_columns)`**
Função auxiliar que ajusta os rótulos das colunas de um DataFrame para serem exibidos em gráficos e tabelas.  Converte nomes de colunas em formato de código (ex: "kp") para um formato mais legível (ex: "KP").

- **Parâmetros:**
  - `table_columns` (Index):  Índice de colunas do DataFrame.

- **Retorno:** Lista com os novos rótulos das colunas.

#### **`AnalysePlayer.create_grouped_mean_table_plot(mean_df)`**
Cria uma tabela com as médias das estatísticas do jogador, agrupadas por campeão ou função. A tabela permite comparar o desempenho do jogador com diferentes campeões ou em diferentes funções de forma mais detalhada.

- **Parâmetros:**
  - `mean_df` (DataFrame): DataFrame contendo as médias das estatísticas, agrupadas por campeão ou função.

- **Retorno:**  `fig` (Figure): Objeto da figura gerada pelo matplotlib.

#### **`AnalysePlayer.create_player_analysis()`**
Realiza a análise completa dos dados do jogador.  Essa função orquestra a execução das outras funções do módulo, criando os DataFrames, calculando as estatísticas e preparando os dados para a geração dos gráficos.

- **Retorno:**
    - `dfs_dict` (dict): Dicionário contendo os DataFrames gerados durante a análise (média, mínimo/máximo, agrupados por campeão e por função).
    - `history_games` (list): Lista contendo o histórico de partidas do jogador, com informações resumidas de cada partida.

#### **`AnalysePlayer.__create_player_history(dfs)`**
Cria um histórico resumido das partidas do jogador, incluindo informações como nome de invocador, campeão jogado, KDA, bans e informações dos jogadores de cada time.

- **Parâmetros:**
  - `dfs` (dict): Dicionário contendo os DataFrames com os dados das partidas (`players`, `games`, `bans`, `teams`).

- **Retorno:** `history_games` (list): Lista de dicionários, onde cada dicionário representa uma partida e contém informações resumidas sobre ela.

---

### `mongo_code.db_connection`

#### **`find_items(id_item)`**
Busca um item pelo ID.
- **Parâmetros:**
  - `id_item` (int/str): ID do item.
- **Retorno:** Nome do item.

#### **`find_runes(id_rune)`**
Busca uma runa pelo ID.
- **Parâmetros:**
  - `id_rune` (int/str): ID da runa.
- **Retorno:** Nome da runa.

#### **`find_summoner_spells(id_spell)`**
Busca um feitiço de invocador pelo ID.
- **Parâmetros:**
  - `id_spell` (int/str): ID do feitiço.
- **Retorno:** Nome do feitiço.

#### **`find_champion_by_id(id_champion)`**
Busca um campeão pelo ID.
- **Parâmetros:**
  - `id_champion` (int/str): ID do campeão.
- **Retorno:** Nome do campeão.

#### **`find_champion_by_name(name_champion)`**
Busca um campeão pelo nome.
- **Parâmetros:**
  - `name_champion` (str): Nome do campeão.
- **Retorno:** Informações do campeão.

#### **`find_match(id_match)`**
Busca uma partida pelo ID.
- **Parâmetros:**
  - `id_match` (str): ID da partida.
- **Retorno:** Dados da partida.

#### **`find_player_history(puuid)`**
Busca o histórico de partidas de um jogador.
- **Parâmetros:**
  - `puuid` (str): PUUID do jogador.
- **Retorno:** Lista de partidas.

#### **`create_match_db(matchs_data)`**
Salva os dados de uma ou várias partidas no banco de dados.
- **Parâmetros:**
  - `matchs_data` (list): Lista de dicionários, onde cada dicionário representa os dados de uma partida.
- **Retorno:** Resultado da operação de inserção no banco de dados.

#### **`find_queue_type(queue_id)`**
Busca o tipo de fila pelo ID.
- **Parâmetros:**
  - `queue_id` (int): ID da fila.
- **Retorno:** Descrição do tipo de fila.

---

### `main.py`

Arquivo principal que inicia a execução do projeto. Responsável por obter o nome e a tag do jogador, coletar os dados, processá-los, analisá-los e gerar as visualizações.