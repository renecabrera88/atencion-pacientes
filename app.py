#from contextlib import ContextDecorator
#from crypt import methods
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from calculos.calculo import suma
from middleware.consulta import consultaPaciente, salaEspera
from middleware.consultaIndex import get_pacientes, get_data_filtrada, get_sala_atencion, get_sala, update_estado_consulta

app = Flask ( __name__ )
#MySQL coneccion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fonasa'
mysql = MySQL(app)

#setting
# es como un token
app.secret_key = 'mysecretkey'

#@pp se llama decorador, si entra a la ruta raiz,
#ejecuta funcion Index que renderiza index.html, no es
# necesario indicar el la ruta por que sabe que esta en template 
@app.route('/')
def Index():
    data = get_pacientes(mysql)
    print('esta es la data de index :', data)
    return render_template('index.html', pacientes = data)

@app.route('/add_persona')
def add_persona():
    return render_template('add-persona.html')

@app.route('/add_hospital')
def add_hospital():
    return render_template('add-hospital.html')

@app.route('/add_doctor')
def add_doctor():
    return render_template('add-doctor.html')

@app.route('/add_consulta')
def add_consulta():
    return render_template('add-consulta.html')

@app.route('/add_paciente')
def add_paciente():
    return render_template('add-paciente.html')

@app.route('/add_atencion')
def add_atencion():
    return render_template('add-atencion.html')

@app.route('/req_uno')
def req_uno():
    data = get_pacientes(mysql)
    print('esta es la data de index :', data)
    return render_template('req-uno.html', pacientes = data)

@app.route('/req_uno_seleccionar/<prioridad>')
def req_uno_filtro(prioridad):
    data = get_data_filtrada(mysql, prioridad)
    return render_template('index.html', pacientes = data)

@app.route('/req_dos')
def req_dos():
    data = get_sala(mysql)
    print('esta es la data de index :', data)
    return render_template('req-dos.html', pacientes = data)

@app.route('/req_dos_atencion/<id_sala>')
def req_dos_atencion(id_sala):
    data = get_sala_atencion(mysql, id_sala)
    print('Data requerimiento 2 :', data[0])
    return render_template('req-dos-atencion.html', pacientes = data[0])





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


@app.route('/add_doctor_db', methods=['POST'])
def add_doctor_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        rut = request.form['rut']
        especialidad = request.form['especialidad']
        #crea una coneccion y la envia a una variable cur (cursos)
        cur = mysql.connection.cursor()
        #escribe lña consulta sql
        cur.execute('INSERT INTO doctor (id_persona, especialidad) VALUES (%s, %s)',(rut, especialidad))
        #INSERT INTO `doctor`(`id`, `id-persona`, `especialidad`, `estado`, `id-hospítal`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]')
        #ejecuta la coinsulta sql
        mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        flash('El Doctor fue agregado con exito')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))


@app.route('/add_consulta_db', methods=['POST'])
def add_consulta_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        cantidadPaciente = request.form['cantidadPaciente']
        rutDoctor = request.form['rutDoctor']
        tipoConsulta = request.form['tipoConsulta']
        fechaConsulta = request.form['fechaConsulta']
        nombreHospital = request.form['nombreHospital']
        #crea una coneccion y la envia a una variable cur (cursos)
        cur = mysql.connection.cursor()
        #escribe lña consulta sql
        cur.execute('INSERT INTO consulta (cant_pacientes, id_doctor, tipo_consulta, fecha_consulta, id_hospital) VALUES (%s, %s, %s, %s, %s)',(cantidadPaciente, rutDoctor, tipoConsulta, fechaConsulta, nombreHospital))
        #INSERT INTO `consulta`(`id`, `cant-pacientes`, `id-doctor`, `tipo-consulta`, `estado`, `fecha-consulta`, `id-hospital`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]')
        #ejecuta la coinsulta sql
        mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        flash('La consulta fue agregada fue agregada con exito')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))

@app.route('/add_paciente_db', methods=['POST'])
def add_paciente_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        idPersona = request.form['idPersona']
        idHospital = request.form['idHospital']
        #prueba llamando funciones
        prioridad = (suma(10, 5))
        print(prioridad)
        #crea una coneccion y la envia a una variable cur (cursor)
        cur = mysql.connection.cursor()
        #escribe lña consulta sql
        cur.execute('INSERT INTO paciente (id_persona, id_hospital) VALUES (%s, %s)',(idPersona, idHospital))
        #INSERT INTO `paciente`(`id`, `id_persona`, `tiene_dieta`, `rel_peso_altura`, `fumador`, `estado`, `id_hospital`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]')
        #ejecuta la coinsulta sql
        mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        flash('El paciente fue agregada fue agregada con exito')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))



@app.route('/add_atencion_db', methods=['POST'])
def add_atencion_db():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        idPaciente = request.form['idPaciente']
        idConsulta = request.form['idConsulta']
        observacion = request.form['observacion']
        estatura = request.form['estatura']
        peso = request.form['peso']
        tieneDieta = request.form['tieneDieta']
        fumador = request.form['fumador']
        aniosFumador = request.form['aniosfumador']
        dataPaciente = consultaPaciente(int(idPaciente), idConsulta,estatura, peso, fumador, aniosFumador, tieneDieta, observacion, mysql)
        print('en app :', dataPaciente)
        listaAtencion = salaEspera(dataPaciente, mysql)
        #print('lista :', listaAtencion)

        #prueba llamando funciones
        #prioridad = (suma(peso,altura))
        
        #crea una coneccion y la envia a una variable cur (cursor)
        ##cur = mysql.connection.cursor()
        #escribe lña consulta sql
        ##cur.execute('INSERT INTO paciente (id_paciente, id_consulta, observacion, estatura, peso, tiene_dieta, fumador,) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        ##(idPaciente, idConsulta, observacion, estatura, peso, tieneDieta, fumador))
        #INSERT INTO `paciente`(`id`, `id_persona`, `tiene_dieta`, `rel_peso_altura`, `fumador`, `estado`, `id_hospital`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]')
        #ejecuta la coinsulta sql
        ##mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        ##flash('El paciente fue agregada fue agregada con exito')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        return redirect(url_for('Index'))

@app.route('/req_dos_update', methods=['POST'])
def req_dos_update():
    if request.method == 'POST':
        #Asigna valores a variables extraido de los input del form html
        diagnostico = request.form['diagnostico']
        id_atencion = request.form['id_atencion']

        update_estado_consulta(mysql, diagnostico, id_atencion)

        print('Corresponde al id del diagnostico : ', id_atencion)
        print('Corresponde al diagnostico : ', diagnostico)
        #crea una coneccion y la envia a una variable cur (cursos)
        ##cur = mysql.connection.cursor()
        #escribe lña consulta sql
        ##cur.execute('INSERT INTO personas (rut, nombre, direccion, fechaNacimiento) VALUES (%s, %s, %s, %s)',(rut, nombre, direccion, fechaNacimiento))
        #ejecuta la coinsulta sql
        ##mysql.connection.commit()
        #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
        ##flash('Constact added successfully')
        #despues de ejecutar la coinsulta sql, redirecciona la web a index
        ##return redirect(url_for('Index'))
        return redirect(url_for('Index'))

#si el archjivo que arranca es app.py, arranca el server
if __name__ == '__main__':
    app.run(port = 3000, debug = True )