from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import datetime, timedelta


def consultaPaciente(idPaciente, idConsulta,estatura, peso, fumador,aniosfumador, tieneDieta, observacion, mysql):
    #obtengo datos de paciente
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM paciente WHERE id = (%s)', [idPaciente])
    data = cur.fetchall()
    #extraigo id de la persona
    dataPaciente = (data[0])
    iddata = dataPaciente[1]

    #consulto dato de las personas
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas WHERE id = (%s)', [iddata])
    dataPersona = cur.fetchall()
    #extraigo fecha de la tupla
    dataFecha = dataPersona[0]
    fechaNacimiento = dataFecha[5]
    
    #consulto dato de la consulta
    ##cur = mysql.connection.cursor()
    ##cur.execute('SELECT * FROM consulta WHERE id = (%s)', [idConsulta])
    ##dataTupla = cur.fetchall()
    ##dataConsulta = dataTupla[0]
    ##numero_atencion = (dataConsulta[1]-dataConsulta[7]) + 1
    
    ##print('Datos de la consulta: ', dataConsulta[0] )
    ##print('numero de atencion :', numero_atencion)



    
    #proceso que saca la edad
    today = datetime.now()
    edad = int(today.year - fechaNacimiento.year - ((today.month,today.day) < (fechaNacimiento.month, fechaNacimiento.day)))
    print("La edad es : ", edad)

    #Prioridad
    if (1 <= edad <= 16):
        if (1 <= edad <= 5):
            prioridad = (int(peso) / int(estatura) ) + 3
            print("rango 1")
        elif (6 <= edad <= 12):
            prioridad = (int(peso) / int(estatura) ) + 2
            print("rango 2")
        elif (13 <= edad <= 15):
            prioridad = (int(peso) / int(estatura) ) + 1
            print("rango 3")
    elif (16 <= edad <= 59):
        if (fumador == "si"):
            prioridad = int(aniosfumador)/4 + 2
        else:
            prioridad = 2

        print ("rango joven")
        
    elif (60 <= edad <= 100):
        if tieneDieta == "si":
            prioridad = (int(edad) / 20) + 4
        else:
            prioridad = (int(edad) /30) + 3

    print("rango 3ra edad")
    print ("Paciente con prioridad : ", prioridad)



    if (1 <= edad < 60):
        prioridadGeneral = (prioridad * edad)/ 100
    elif (60 <= edad <= 100):
        prioridadGeneral = ((prioridad * edad)/ 100) + 5.3

    print("prioridad general : ", prioridadGeneral)
    #age = (edad)
    #print (tuple(age))
    dataCompleta = dataPaciente + dataPersona[0]
    lista = list(dataCompleta)
    print('Esta es una lista sin edad :', lista)
    lista.append(edad)
    print('Esta es una lista con edad :', lista)
     
    dataCompletaPaciente = tuple(lista)
    print('data completa paciente :', dataCompletaPaciente )

    
    cur = mysql.connection.cursor()
    #escribe lña consulta sql
    cur.execute('INSERT INTO atencion (id_paciente, id_consulta, observaciones, prioridad, estatura, peso, tiene_dieta, fumador, edad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
    (idPaciente, idConsulta, observacion, prioridadGeneral, estatura, peso, tieneDieta, fumador, edad))
    #ejecuta la coinsulta sql
    mysql.connection.commit()
    #Manda un mensaque flask desde al servidor al frontend, de exito de la transaccion
    flash('El paciente fue agregada fue agregada con exito')

    print ("hello world")
    #print(dataCompleta[9])
    #ahora = datetime.strftime()
    #edad = datetime.now - dataCompleta[9]
    #print(edad) 

    print(dataCompleta)
    return (dataCompletaPaciente)



def salaEspera(dataPaciente, mysql):
    print(dataPaciente)
    return (dataPaciente)

    ##hacer: creaer 2 tablas, una que me guarde una lista con todos los id de paciente listo a ser atendidos
    # de acuerdo a la capacidad de pacientes de la consulta ,y 
    #otra con los pacientes que estan en la sala de espera y proximo a ser pasado a la lista,  
    # aqui construyo las lista de acuerdo a la edad del paciente.