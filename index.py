import pandas as pd
import numpy as np
import pymysql
import conexao
import csv
import chardet
from flask import Flask, request, Response
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill

app = Flask(__name__)

conn = pymysql.connect(host=conexao.host, user=conexao.user, password=conexao.passw, database=conexao.db, charset='utf8')
cursor = conn.cursor()

def ultrapassado(velocidade, pos_id):
    velocidade = int(velocidade)
    pos_id = int(pos_id)
    if  velocidade > pos_id :
        if velocidade <= 100:
            tol = 1.1
            velocidadextol = pos_id*tol
            # print(velocidadextol)
            if velocidade > velocidadextol :
                velocidadeExcedida =  ((velocidade / pos_id) - 1) * 100

                return velocidadeExcedida
            else:
                return 'Não ultrapassou'
        else:
            tol = 1.07
            velocidadextol = pos_id*tol
            if velocidade > velocidadextol:
                velocidadeExcedida =  ((velocidade / pos_id) - 1) * 100
                return velocidadeExcedida
            else:
                return 'Não ultrapassou'
    else:
        return 'Não ultrapassou'


@app.route('/vetorian/relatorio', methods=['POST'])
def relatorio_teste1():
    
    file = request.files['file']
    placa = request.form['placa']
    data = request.form['data']

    cursor.execute('SELECT placa, data_atualizacao, observacao, velocidade, pos_id, latitude, longitude FROM sau_posicionamento where placa = "' + placa + '" and date(data_atualizacao) =  "'+ data +' "')
    results = cursor.fetchall()

    data_to_write = [result for result in results]

    
    with open('resultado_query.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Escrever o cabeçalho do CSV
        csvwriter.writerow(['placa', 'data_atualizacao', 'observacao', 'velocidade', 'pos_id', 'latitude', 'longitude', 'ultrapassada'])
        
        # Escrever os dados no CSV
        for row in data_to_write:
            velocidade, pos_id = row[3], row[4]
            row = list(row)  # Converter a tupla em uma lista
            row.append(ultrapassado(velocidade, pos_id))  # Adicionar a coluna 'ultrapassada'
            csvwriter.writerow(row)


    with open('resultado_query.csv', 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    # df = pd.read_csv(file, sep=';')

    df = pd.read_csv('resultado_query.csv', encoding=encoding)

    df = df[df['velocidade'] > 5] 
    df['ultrapassada'] = df.apply(lambda row: ultrapassado(row['velocidade'], row['pos_id']), axis=1)
    
    # print(df)

    return 'ok'



if __name__ == '__main__':
    # app.run('127.0.0.1')
    app.run()
