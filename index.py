import pandas as pd
import numpy as np
import pymysql
import conexao
import csv
import json
import time
import chardet
import pytz
import os
import matplotlib.pyplot as plt
from io import BytesIO
from xhtml2pdf import pisa
from functions import Functions
from flask import Flask, request, Response
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill

app = Flask(__name__)

conn = pymysql.connect(host=conexao.host, user=conexao.user, password=conexao.passw, database=conexao.db,
                       charset='utf8')

cursor = conn.cursor()


@app.route('/relatorio', methods=['POST'])
def relatorio_query():
    placa = request.form['placa']
    data = request.form['data']

    func = Functions() ## instancia classe funcoes

    query = 'SELECT placa, data_atualizacao, observacao, velocidade, pos_id, latitude, longitude FROM sau_posicionamento WHERE placa = "' + placa + '" AND date(data_atualizacao) = "' + data + '" ORDER BY data_atualizacao DESC'
    cursor.execute(query)

    results = cursor.fetchall()

    # cursor.close() #nao descomentar
    # conn.close() #nao descomentar

    if not results:
        return ' query não obteve resultados'
    else:

        data_to_write = [result for result in results]
        with open('files/csv/'+placa + data + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow(
                ['PLACA', 'DATA', 'LOCAL', 'VELOCIDADE', 'VELOCIDADE VIA', 'LATITUDE', 'LONGITUDE', 'ULTRAPASSADO'])
            
            for row in data_to_write:
                velocidade, pos_id = row[3], row[4]
                row = list(row)
                row.append(func.ultrapassado(velocidade, pos_id))
                csvwriter.writerow(row)
        
        time.sleep(3)
        
        with open('files/csv/'+placa + data + '.csv', 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        df = pd.read_csv('files/csv/'+placa + data + '.csv', encoding=encoding)

        df = df[df['VELOCIDADE'] > 5]

        if df.empty:
            return 'nao houve movimentacoes esse dia'
            abort(400)
            sys.exit()
        else:

            df['DATA'] = pd.to_datetime(df['DATA'])
            df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y %H:%M:%S')

            df['ULTRAPASSADO'] = df.apply(lambda row: func.ultrapassado(row['VELOCIDADE'], row['VELOCIDADE VIA']), axis=1)
            df[["VELOCIDADE", "VELOCIDADE VIA"]] = df[["VELOCIDADE", "VELOCIDADE VIA"]].applymap(func.add_km)

            styled_df = df.style.set_properties(**{
                'font-family': 'Gotham Book',
                'font-size': '18px',
            }).applymap(lambda x: f'color: {"black" if isinstance(x, str) else "purple"}''') \
                .applymap(func.velocidade_excedida, subset='ULTRAPASSADO')

            styled_df.to_excel('files/'+placa+data+'.xlsx', index=False)
            
            diretorio_nome = placa+data

            response = {
                "erro": False,
                "msg": diretorio_nome
            }
            
            return response
            abort(400)
            sys.exit()


@app.route('/relatorio-file', methods=['POST'])
def relatorio_file():
    if request.files:
        
        file = request.files['file']
        df = pd.read_csv(file, sep=';')
        df = df[df['velocidade'] > 5]
        filename = file.filename
        name, extension = os.path.splitext(filename)
        
        func = Functions() ## instancia classe funcoes
        
        df['data_atualizacao'] = pd.to_datetime(df['data_atualizacao'], dayfirst=True)
        df['data_atualizacao'] = df['data_atualizacao'].dt.strftime('%d/%m/%Y %H:%M:%S')

        df['ultrapassado'] = df.apply(lambda row: func.ultrapassado(row['velocidade'], row['pos_id']), axis=1)
        df[["velocidade", "pos_id"]] = df[["velocidade", "pos_id"]].applymap(func.add_km)

        styled_df = df.style.set_properties(**{
            'font-family': 'Gotham Book',
            'font-size': '18px',
        }).applymap(lambda x: f'color: {"black" if isinstance(x, str) else "purple"}''') \
            .applymap(func.velocidade_excedida, subset='ultrapassado')
        
        arquivo = name + '.xlsx'
        styled_df.to_excel(arquivo, index=False)

        # print(df)

        return df.to_dict(orient='records')

        abort(400)  
        sys.exit()

    else:
        return 'precisa conter arquivo'

        abort(400)  
        sys.exit()


if __name__ == '__main__':
    app.run('127.0.0.1')
    app.run()
