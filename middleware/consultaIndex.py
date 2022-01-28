def get_pacientes(mysql):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM atencion')
    data = cur.fetchall()
    #La siguiente linea retorna una variable contact que tiene valor de data
    return data