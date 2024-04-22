import pandas as pd
from datetime import date
import pyodbc


# valor de mesApi anio
def get_value_api(date_value):
    date = pd.to_datetime(date_value)
    if date.month == 12 and date.year == 2023:
        return 177
    elif date.month == 11 and date.year == 2023:
        return 176
    elif date.month == 10 and date.year == 2023:
        return 174
    elif date.month == 9 and date.year == 2023:
        return 172
    elif date.month == 8 and date.year == 2023:
        return 171
    elif date.month == 7 and date.year == 2023:
        return 169
    elif date.month == 6 and date.year == 2023:
        return 168
    elif date.month == 5 and date.year == 2023:
        return 166
    elif date.month == 4 and date.year == 2023:
        return 165
    elif date.month == 3 and date.year == 2023:
        return 163
    elif date.month == 2 and date.year == 2023:
        return 162
    elif date.month == 1 and date.year == 2023:
        return 159

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
    if cursor.rowcount == 0:
        return 'No se encontraron resultados'
    for row in cursor:
        # gurdar todos los datos en una variable separada por comas
        texto = texto + str(row[0]) + ','
    else:
        # quitar coma final
        texto = texto[:-1]

    conn.close()
    return texto


def main():
    archivo = 'data.xlsx'
    df = pd.read_excel(archivo)
    # desde el primero valor hasta el 10 
    # df = df.iloc[0:10]

    for index, row in df.iterrows():
        valor = get_consulta(row.iloc[6], row.iloc[8], row.iloc[9])
        print('Valor obtenido de la query', valor)
        df.at[index,"Versiones"] = valor
        print('Valor de fecha de venta', row.iloc[3])
        value_api= get_value_api(row.iloc[3])
        df.at[index,"anioValue"] = value_api
    
    df.to_excel('data_resultados.xlsx', index=False, header=True)



main()