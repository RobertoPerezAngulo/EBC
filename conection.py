import pyodbc

def get_connection():
    server = '192.168.11.4\developer'
    database = 'mx_sis_bd'  
    username = 'jrperez'  
    password = 'Pumas2012JAZ' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn

def get_consulta(marca, modelo, anio):
    texto = ''
    param_marca = f'%{marca}%'
    param_modelo = f'%{modelo}%'
    query= """
                   SELECT CAST(CVANIO AS VARCHAR)  +  CAST(VERSI.CVMARG AS VARCHAR) + CAST(VERSI.CVMODG AS VARCHAR)  + CAST(CVVEVG AS VARCHAR) [Version]
                    FROM EBCCVEVG VERSI
                    INNER JOIN EBCCMARG MARCA
                    ON VERSI.CVMARG = MARCA.CVMARG
                    INNER JOIN EBCCMODG MODELO
                    ON VERSI.CVMODG = MODELO.CVMODG
                    WHERE EXMARG LIKE ?
                    AND MODELO.EXMODG LIKE ?
                    AND VERSI.CVANIO = ? """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, param_marca, param_modelo, anio)
    for row in cursor:
        # gurdar todos los datos en una variable separada por comas
        texto = texto + str(row[0]) + ','
    else:
        # quitar coma final
        texto = texto[:-1]

    conn.close()
    return texto

get_consulta('MAZDA', '2', '2019')