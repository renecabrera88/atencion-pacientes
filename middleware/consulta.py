from flask import Flask, flash, render_template, request, redirect, url_for
from datetime import datetime, timedelta


def consultaPaciente(idPaciente, idConsulta,estatura, peso, fumador,aniosfumador, tieneDieta, mysql):
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




    dataCompleta = dataPaciente + dataPersona[0] 

     



    #print(dataCompleta[9])
    #ahora = datetime.strftime()
    #edad = datetime.now - dataCompleta[9]
    #print(edad) 

    print(dataCompleta)
    return (dataCompleta)
    
    