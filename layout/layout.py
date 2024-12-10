from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-return-api', methods=['POST'])
def get_player_name_tag():
    player_name = request.form['player_name']
    player_tag = request.form['player_tag']

    return f"<h1>Você enviou: {player_name} e {player_tag}</h1>"

app.run()