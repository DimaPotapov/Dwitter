import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
     
DATABASE = '/tmp/dwitter.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# создаём наше маленькое приложение :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'dwitter.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Если ещё нет соединения с базой данных, открыть новое - для
    текущего контекста приложения
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/', methods=['GET'])
def hello():
 db = get_db()
 cur = db.execute('select title, text from entries order by id desc')
 entries = cur.fetchall()
 return render_template('log_in.html', entries=entries)
	
@app.route('/sign_in', methods = ['POST','GET'])
def sign_in():
 db = get_db()
 if request.method == 'POST':
    if request.form['login'] == 'login' and request.form['password'] == 'password':
    	return 'Hello' + request.form['login']
    else:
    	return 'Wrong way Bro, Try again!'
@app.route('/sign_up')
def sign_up():
	return render_template('sign_up.html')

@app.route('/new_user_add', methods =['POST'])
def new_user_add():
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['new_user_login'], request.form['new_user_password']])
	db.commit()
	return "good"





if __name__ == '__main__':
    app.run()