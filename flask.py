from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():

    conn = sqlite3.connect('subway.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, latitude, longitude, address, time FROM store")
    rows = cursor.fetchall()

    conn.close()
    
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)