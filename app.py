import psycopg2
import configparser
from flask import Flask, jsonify

# Dane do połączenia z bazą danych
def connect_to_db(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    params = config['POST']
    conn = psycopg2.connect(**params)
    return conn

app = Flask(__name__)

@app.route('/data')
def get_data():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dzienne_porownanie")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run()
