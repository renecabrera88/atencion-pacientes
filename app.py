#from contextlib import ContextDecorator
#from crypt import methods
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask ( __name__ )
#MySQL coneccion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fonasa'
mysql = MySQL(app)

#setting
#Ni idea para lo que es, pero es como un token
app.secret_key = 'mysecretkey'

#@pp se llama decorador, si entra a la ruta raiz,
#ejecuta funcion Index que renderiza index.html, no es
# necesario indicar el la ruta por que sabe que esta en template 
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    #La siguiente linea retorna una variable contact que tiene valor de data
    #return render_template('index.html', contacts = data)
    print(data)
    return 'hello world'