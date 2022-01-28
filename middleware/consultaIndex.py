
def get_data_filtrada(mysql, prioridad):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT atencion.id, atencion.prioridad, personas.rut, personas.nombre, personas.direccion
                FROM atencion  
                JOIN paciente
                ON atencion.id_paciente = paciente.id
                JOIN personas
                ON paciente.id_persona = personas.id
                WHERE atencion.estado = "activo" AND atencion.prioridad > (%s)
                ORDER BY atencion.prioridad DESC''', [prioridad])
        
    data = cur.fetchall()
    return data


def get_pacientes(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT atencion.id, atencion.prioridad, personas.rut, personas.nombre, personas.direccion
                FROM atencion  
                JOIN paciente
                ON atencion.id_paciente = paciente.id
                JOIN personas
                ON paciente.id_persona = personas.id
                WHERE atencion.estado = "activo"
                ORDER BY atencion.prioridad DESC''')
        
    #cur.execute('SELECT * FROM atencion')
    data = cur.fetchall()
    #print('esta es la data de index :', data)
    #La siguiente linea retorna una variable contact que tiene valor de data
    return data

def get_sala(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT sala_atencion.id, atencion.prioridad, atencion.observaciones, personas.rut, personas.nombre, personas.direccion
                FROM sala_atencion
                JOIN atencion
                ON sala_atencion.id_atencion = atencion.id  
                JOIN paciente
                ON atencion.id_paciente = paciente.id
                JOIN personas
                ON paciente.id_persona = personas.id
                WHERE atencion.estado = "activo" ''')
        
    #cur.execute('SELECT * FROM atencion')
    data = cur.fetchall()
    #print('esta es la data de index :', data)
    #La siguiente linea retorna una variable contact que tiene valor de data
    return data


def get_sala_atencion(mysql, id_sala):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT sala_atencion.id, atencion.id, atencion.prioridad, atencion.observaciones, personas.rut, personas.nombre, personas.direccion
                FROM sala_atencion
                JOIN atencion
                ON sala_atencion.id_atencion = atencion.id  
                JOIN paciente
                ON atencion.id_paciente = paciente.id
                JOIN personas
                ON paciente.id_persona = personas.id
                WHERE atencion.estado = "activo" AND atencion.id = sala_atencion.id_atencion  AND sala_atencion.id = (%s)''', [ id_sala] )
        
    #cur.execute('SELECT * FROM atencion')
    data = cur.fetchall()
    #print('esta es la data de index :', data)
    #La siguiente linea retorna una variable contact que tiene valor de data
    return data



def update_estado_consulta(mysql, diagnostico, id_atencion):
    cur = mysql.connection.cursor()
    cur.execute("""
       UPDATE atencion
       SET observaciones = %s, estado = 'atendido'  
       WHERE id = %s
       """ ,(diagnostico, id_atencion))
    mysql.connection.commit()
    return




#SELECT OrderID, C.CustomerID, CompanyName, OrderDate
#FROM Customers C JOIN Orders O ON C.CustomerID = O.CustomerID JOIN Employees E ON O.EmployeeID = E.EmployeeID
#WHERE C.Country = 'Spain' OR E.EmployeeID = 5


#SELECT atencion.id, atencion.prioridad, personas.rut, personas.nombre, personas.direccion
#FROM atencion  
#JOIN paciente
#ON atencion.id_paciente = paciente.id
#JOIN personas
#ON paciente.id_persona = personas.id
#WHERE atencion.estado = 'activo'
#ORDER BY atencion.prioridad DESC

#SELECT atencion.id, atencion.prioridad, atencion.observacion, personas.rut, personas.nombre, personas.direccion
#FROM atencion  
#JOIN paciente
#ON atencion.id_paciente = paciente.id
#JOIN personas
#ON paciente.id_persona = personas.id
#WHERE atencion.estado = 'activo' AND atencionid = id
#ORDER BY atencion.prioridad DESC
