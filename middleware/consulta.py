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
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM consulta WHERE id = (%s)', [idConsulta])
    dataTupla = cur.fetchall()
    dataConsulta = dataTupla[0]
    ticket = dataConsulta[1]
    ##numero_atencion = (dataConsulta[1]-dataConsulta[7]) + 1
    
    #Reseteo de ticket, llevando al nunmero de cupo
    cur = mysql.connection.cursor()
    cur.execute("""
       UPDATE consulta
       SET ticket = %s
       WHERE id = %s
       """ ,(ticket, idConsulta))
    mysql.connection.commit()
    


    print('Esto son los Datos de la Tupla de la consulta :', ticket )
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


def llenarConsulta(enEspera, mysql):
    #extraigo cupo de atenciones y cuanto disponibles
    idatencion = enEspera[0]
    idPaciente = enEspera[1]
    idConsulta = enEspera[2]
    prioridad = enEspera[5]
    #consulta por la cantidad de numeros de atencion entregado basado en los tickes
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM consulta WHERE id = (%s)', [idConsulta])
    atencionConsulta  = cur.fetchall()
    tuplaConsulta = atencionConsulta[0]
    pacientes = tuplaConsulta[1]
    ticket = tuplaConsulta[7]
    numerosAtencion = (pacientes - ticket) + 1
    ticket = ticket - 1
    print('Datas', idatencion, idPaciente, idConsulta, prioridad, pacientes, ticket, numerosAtencion)
    if ticket >= 0:
        #Limpio las tablas sala_atencion y sala_espera

        #actualiza nuevo valor ticket
        cur = mysql.connection.cursor()
        cur.execute("""
           UPDATE consulta
           SET ticket = %s
           WHERE id = %s
           """ ,(ticket, idConsulta))
        mysql.connection.commit()
        #estos corresponde a las primeras prioridades y se van a lista para esperar atencion
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO sala_atencion (id_atencion, id_consulta, id_paciente, prioridad) VALUES (%s, %s, %s, %s)',(idatencion, idConsulta, idPaciente, prioridad))
        mysql.connection.commit()
    else:
        #esta tabla llena a los que no son prioridad
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO sala_espera (id_atencion, prioridad, id_consulta, id_paciente) VALUES (%s, %s, %s, %s)',(idatencion, prioridad, idConsulta, idPaciente, ))
        mysql.connection.commit()

    return

#def resetTicket(mysql):

 #   cur = mysql.connection.cursor()
 #   cur.execute('SELECT * FROM atencion WHERE estado = (%s) ORDER BY prioridad DESC', ['activo'])
 #   dataAtencionActivos  = cur.fetchall()

def salaEspera(dataPaciente, mysql):
    #reinicio las tablas borrandolas
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM sala_atencion;')
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM sala_espera;')
    mysql.connection.commit()
    #la idea es consulta por y resetear los ticket
    #resetTicket(mysql)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM atencion WHERE estado = (%s) ORDER BY prioridad DESC', ['activo'])
    dataAtencionActivos  = cur.fetchall()
    #Extraigo info sobre de los pacientes activos para crear sala de espera
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM atencion WHERE estado = (%s) ORDER BY prioridad DESC', ['activo'])
    dataAtencionActivos  = cur.fetchall()
    #extraigo id de la persona
    #dataPaciente = (data[0])
    for enEspera in dataAtencionActivos:
        llenarConsulta(enEspera, mysql)
        
        
        
    #print('Sala de espera: ',dataAtencionActivos)
    return (dataAtencionActivos)

    ##hacer: creaer 2 tablas, una que me guarde una lista con todos los id de paciente listo a ser atendidos
    # de acuerdo a la capacidad de pacientes de la consulta ,y 
    #otra con los pacientes que estan en la sala de espera y proximo a ser pasado a la lista,  
    # aqui construyo las lista de acuerdo a la edad del paciente.