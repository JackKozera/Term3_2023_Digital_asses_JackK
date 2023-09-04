from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
import bcrypt
import requests

app = Flask(__name__)
app.secret_key = 'theSecret'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if password == password_check:
            try:
                with sqlite3.connect('northside.db') as db:
                    cursor = db.cursor()
                    cursor.execute('''INSERT INTO normal_user (username, hashed_password) VALUES (?, ?)''', (username, hashed_password))
                    db.commit()
                    db.close()
                    print("registered successfully")
                    return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                print("username already exists")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with sqlite3.connect('northside.db') as db:
                cursor = db.cursor()
                sqlite_select_query = """SELECT * from normal_user where username == 'username'"""
                cursor.execute(sqlite_select_query, (username))
                saved_password = cursor.fetchone(hashed_password)
                print('saved password: ', saved_password)
                if hashed_password == saved_password:
                    print("logged in successfully")
                    return redirect(url_for('index'))
                else:
                    print("incorrect password")
        except sqlite3.IntegrityError:
            print("username does not exist")
            db.commit()
            db.close()

    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if request.method == 'POST':
            artist_name = request.form['artist']
            albums = search_albums(artist_name)
            print(type(albums))
            save_albums_to_db(artist_name, albums)
            return render_template('results.html', artist=artist_name, albums=albums)
    return render_template('search.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        albums = search_albums(artist_name)
        print(type(albums))
    return render_template('results.html', albums=albums, artist=artist_name)

def search_albums(artist_name):
    API_KEY = '523532'
    URL = f'https://theaudiodb.com/api/v1/json/{API_KEY}/searchalbum.php?s={artist_name}'
    response = requests.get(URL)
    data = response.json()
    albums = data['album']
    return albums

def save_albums_to_db(artist_name, albums):
    conn = sqlite3.connect('albums.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums
                 (artist TEXT, album TEXT, year INTEGER)''')

    for album in albums:
        c.execute("INSERT INTO albums VALUES (?,?,?)",(artist_name, album['strAlbum'], album['intYearReleased']))
    conn.commit()
    conn.close()



if __name__ == '__main__':
    app.run(debug=True)