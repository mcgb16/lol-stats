# **basic.py**

Este módulo fornece funções utilitárias para lidar com dados do League of Legends, desde o consumo de APIs até o processamento e validação de informações de partidas.

## **Funções Disponíveis**

### **`apis_basic_info(pl_name, pl_tag)`**
Obtém informações básicas de um jogador usando a classe `LolVerifier`.
- **Parâmetros:**
  - `pl_name` (str): Nome do jogador.
  - `pl_tag` (str): Tag do jogador.
- **Retorno:** Dicionário contendo:
  - `lol_acc` (LolVerifier): Instância da classe `LolVerifier`.
  - `puuid` (str): Identificador único do jogador.
  - `sum_id` (str): ID do invocador.

---

### **`calculate_time_seconds(sec_time)`**
Converte um tempo em segundos para o formato `MM:SS`.
- **Parâmetros:**
  - `sec_time` (int): Tempo em segundos.
- **Retorno:** Tempo formatado como string `MM:SS`.

---

### **`calculate_timestamps(timestamp_milliseconds)`**
Converte um timestamp em milissegundos para a data e hora formatadas.
- **Parâmetros:**
  - `timestamp_milliseconds` (int): Timestamp em milissegundos.
- **Retorno:** Data e hora formatadas como string `DD-MM-YYYY HH:MM:SS`.

---

### **`sum_data(initial_data, sum_time)`**
Soma um tempo a uma data inicial.
- **Parâmetros:**
  - `initial_data` (str): Data inicial no formato `DD-MM-YYYY HH:MM:SS`.
  - `sum_time` (str): Tempo a ser somado no formato `MM:SS`.
- **Retorno:** Data final formatada como string `DD-MM-YYYY HH:MM:SS`.

---

### **`ask_name_tag()`**
**Depreciada.** Solicita ao usuário o nome e tag do jogador.
- **Retorno:** Tuple contendo o nome e a tag do jogador.

---

### **`save_player_history(lol_acc, lol_acc_puuid)`**
Salva o histórico de partidas de um jogador no banco de dados.
- **Parâmetros:**
  - `lol_acc` (LolVerifier): Instância da classe `LolVerifier`.
  - `lol_acc_puuid` (str): Identificador único do jogador.
- **Retorno:** Resultado do processo de salvamento no banco de dados.

---

### **`check_invalid_game(game_duration)`**
Verifica se a duração de uma partida é inválida (menor que 15 minutos).
- **Parâmetros:**
  - `game_duration` (str): Duração da partida no formato `MM:SS`.
- **Retorno:** String indicando se a partida é `"invalid"` ou `"valid"`.

---

## **Dependências**
- `datetime`: Para manipulação de datas e horas.
- `lol_infos.lol_data_cleaning`: Biblioteca customizada para limpeza de dados.
- `mongo_code.db_connection`: Biblioteca customizada para conexão com banco de dados.
- `lol_infos.lol_apis`: Classe `LolVerifier` para acesso às APIs da Riot Games.

---

## **Observações**
- A função `ask_name_tag` está marcada como **depreciada** e não é recomendada para uso.
- Certifique-se de configurar corretamente as dependências, como conexões de banco de dados e estrutura de APIs.


# **lol_apis.py**

Este módulo fornece uma classe `LolVerifier` para interagir com a API da Riot Games, permitindo acessar informações sobre contas, partidas e classificações no jogo League of Legends.

## **Estrutura do Arquivo**
- Importações: Dependências do módulo (`extras.ex_info` e `requests`).
- Classe: `LolVerifier`.

---

## **Classe LolVerifier**

### **Descrição**
A classe `LolVerifier` fornece métodos para acessar várias informações sobre jogadores e partidas do League of Legends usando a API da Riot Games.

### **Inicialização**
```python
LolVerifier(name, tag)
```

- **Parâmetros:**
  - `name` (str): Nome de invocador do jogador.
  - `tag` (str): Tag do jogador.
- **Atributos:**
  - `api` (str): Chave da API, importada do módulo `extras.ex_info`.
  - `base_url_platform` (str): URL da plataforma regional da Riot Games.
  - `base_url_region` (str): URL da região global da Riot Games.
  - `api_params` (dict): Parâmetros para autenticação da API.

---

### **Métodos**

#### **`__check_response(response)`**
Valida o código de status da resposta e retorna os dados JSON se bem-sucedido.
- **Parâmetros:**
  - `response` (Response): Objeto da resposta da API.
- **Retorno:** Dados JSON da resposta.
- **Erro:** Lança uma exceção para status de erro.

---

#### **`get_puuid()`**
Obtém o `puuid` de um jogador pelo seu nome e tag.
- **Retorno:** `puuid` (str).

---

#### **`get_acc_info(puuid)`**
Obtém informações detalhadas da conta de um jogador.
- **Parâmetros:** 
  - `puuid` (str): Identificador único do jogador.
- **Retorno:** Informações da conta (JSON).

---

#### **`get_acc_ranks(sum_id)`**
Obtém os elos do jogador em diferentes filas ranqueadas.
- **Parâmetros:**
  - `sum_id` (str): ID do invocador.
- **Retorno:** Dados dos elos (JSON).

---

#### **`get_all_matchs(puuid)`**
Obtém as IDs das últimas partidas do jogador (até 85 por padrão).
- **Parâmetros:**
  - `puuid` (str): Identificador único do jogador.
- **Retorno:** Lista de IDs das partidas.

---

#### **`get_match_geral_info(match_id)`**
Obtém informações gerais de uma partida específica.
- **Parâmetros:**
  - `match_id` (str): ID da partida.
- **Retorno:** Informações da partida (JSON).

---

#### **`get_match_timeline_info(match_id)`**
Obtém informações detalhadas baseadas na timeline de uma partida.
- **Parâmetros:**
  - `match_id` (str): ID da partida.
- **Retorno:** Informações detalhadas da timeline (JSON).

---

#### **`get_current_match(puuid)`**
Obtém informações da partida atual do jogador.
- **Parâmetros:**
  - `puuid` (str): Identificador único do jogador.
- **Retorno:** Informações da partida atual (JSON).

---

## **Dependências**
- `extras.ex_info`: Módulo customizado que contém a chave da API (`my_api`).
- `requests`: Biblioteca para realizar chamadas HTTP.

---

## **Observações**
- Métodos `get_match_timeline_info` e `get_current_match` não estão atualmente em uso no projeto.
- Ajuste o número de partidas no método `get_all_matchs` alterando o parâmetro `count`.


# **lol_data_analysis.py**

Este módulo fornece a classe `AnalysePlayer` para realizar análises avançadas de dados de partidas de League of Legends. A classe permite criar DataFrames, realizar análises numéricas e gerar visualizações úteis, como gráficos de radar e de pizza.

## **Classe AnalysePlayer**

### **Descrição**
A classe `AnalysePlayer` utiliza dados armazenados em um banco de dados MongoDB para criar relatórios e análises sobre o desempenho de um jogador.

### **Inicialização**
```python
AnalysePlayer(puuid)
```
- **Parâmetros:**
  - `puuid` (str): Identificador único do jogador.

---

### **Métodos Principais**

#### **`create_acc_radar_plot(acc_df)`**
Cria um gráfico de radar para exibir participação em abates, first blood e first tower.
- **Parâmetros:**
  - `acc_df` (DataFrame): Dados do jogador para análise.
- **Retorno:** None (mostra o gráfico).

---

#### **`create_acc_pie_plot(df)`**
Cria um gráfico de pizza para exibir a taxa de vitórias do jogador.
- **Parâmetros:**
  - `df` (DataFrame): Dados contendo as informações de vitórias e derrotas.
- **Retorno:** None (mostra o gráfico).

---

#### **`create_grouped_mean_table_plot(mean_df)`**
Gera uma tabela com as médias agrupadas de métricas do jogador.
- **Parâmetros:**
  - `mean_df` (DataFrame): Dados agrupados para a análise.
- **Retorno:** Figura do matplotlib.

---

#### **`create_player_analysis()`**
Executa uma análise completa do jogador, incluindo cálculos de métricas, agrupamentos e histórico.
- **Retorno:** 
  - `dfs_dict` (dict): Dicionário contendo DataFrames com métricas calculadas.
  - `history_games` (list): Histórico de partidas formatado.

---

### **Métodos Auxiliares**

#### **`__create_dfs_classic()`**
Cria DataFrames com informações de jogadores, partidas, bans e equipes.
- **Retorno:** Tuple com os DataFrames criados.

---

#### **`__numerical_analysis(p_df)`**
Calcula métricas médias e extremos de desempenho do jogador.
- **Parâmetros:**
  - `p_df` (DataFrame): Dados de desempenho do jogador.
- **Retorno:** Dois DataFrames com as métricas médias e os valores máximos/mínimos.

---

#### **`__grouped_numerical_analysis(p_df)`**
Calcula métricas agrupadas por campeão ou posição.
- **Parâmetros:**
  - `p_df` (GroupBy): Dados agrupados do jogador.
- **Retorno:** Dois DataFrames com as métricas médias e os valores máximos/mínimos.

---

#### **`__adjust_col_labels(table_columns)`**
Ajusta os nomes das colunas para exibição em tabelas e gráficos.
- **Parâmetros:**
  - `table_columns` (list): Lista de colunas originais.
- **Retorno:** Lista de colunas ajustadas.

---

#### **`__create_player_history(dfs)`**
Cria um histórico formatado das partidas do jogador.
- **Parâmetros:**
  - `dfs` (dict): Dicionário contendo DataFrames de jogadores, partidas, bans e equipes.
- **Retorno:** Lista com o histórico das partidas.

---

## **Dependências**
- `matplotlib`: Para geração de gráficos.
- `pandas`: Para manipulação de dados.
- `numpy`: Para cálculos numéricos.
- `mongo_code.db_connection`: Biblioteca customizada para conexão ao banco de dados.
- `basic_code.basic`: Utilitários básicos para processamento de dados.

---

## **Observações**
- Certifique-se de que o banco de dados MongoDB contém os dados necessários para execução.
- Os gráficos são interativos e exibidos automaticamente.

