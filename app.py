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
    return render_template('index.html', contacts = data)

@app.route('/add_persona')
def add_persona():
    return render_template('add-persona.html')

@app.route('/add_hospital')
def add_hospital():
    return render_template('add-hospital.html')


@app.route('/add_persona_db', methods=['POST'])
def add_persona_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        rut = request.form['rut']
        fechaNacimiento = request.form['fechaNacimiento']
        print(fechaNacimiento)
        #crea una coneccion y la envia a una variable cur (cursos)
        cur = mysql.connection.cursor()
        #escribe lña consulta sql
        cur.execute('INSERT INTO personas (rut, nombre, direccion, fechaNacimiento) VALUES (%s, %s, %s, %s)',(rut, nombre, direccion, fechaNacimiento))
        #ejecuta la coinsulta sql
        mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        flash('Constact added successfully')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))
        

@app.route('/add_hospital_db', methods=['POST'])
def add_hospital_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        #crea una coneccion y la envia a una variable cur (cursos)
        cur = mysql.connection.cursor()
        #escribe lña consulta sql
        cur.execute('INSERT INTO hospital (nombre, direccion) VALUES (%s, %s)',(nombre, direccion))
        #ejecuta la coinsulta sql
        mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        flash('Constact added successfully')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))

#si el archjivo que arranca es app.py, arranca el server
if __name__ == '__main__':
    app.run(port = 3000, debug = True )