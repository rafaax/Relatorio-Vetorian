import pandas as pd
import numpy as np
from flask import Flask, request, Response
from openpyxl.utils.dataframe import dataframe_to_rows

from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill

app = Flask(__name__)


@app.route('/vetorian/relatorio', methods=['POST'])
def get_pdf():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400
    else:
        file = request.files['file']
        # pipeline = Vetorian()
        csv = pd.read_csv(file, encoding='latin-1')
        
        return csv.to_dict(orient='records')

    
@app.route('/vetorian/highlight', methods=['POST'])
def testes():
    file = request.files['file']
    df_raw = pd.read_csv(file)
    df_raw = df_raw.sample(n=20, random_state=101)

    # df_raw.style.highlight_min().to_excel('highlight.xlsx')
    # print(df_raw)
    df_raw.style.highlight_min()
    # return df_raw.to_dict(orient='records')


    return 'ok'


@app.route('/vetorian/paternfill', methods=['POST'])
def patternFill():
    file = request.files['file']
    df_raw = pd.read_csv(file, sep=';')

    # print(df_raw['velocidade'])
    # df_raw = df_raw[df_raw['velocidade'] > 5] # filtrar por maior que 30 

    #< 100 = 10%
    #> 100 = 7%

    df_raw['velocidade_excedida'] = (df_raw['velocidade'] < 100) & (df_raw['pos_id'] > df_raw['velocidade'])
    print(df_raw)

    def highlight_salario(s):
        if s is False:
            return 'background-color: yellow'
        else:
            return ''

    # Aplique o estilo ao DataFrame usando .style.applymap()
    styled_df = df_raw.style.applymap(highlight_salario, subset='pos_id')

    # Exporte o DataFrame estilizado para um arquivo Excel
    styled_df.to_excel('relatorio_estilizado.xlsx', index=False)


  

    return '0'




if __name__ == '__main__':
    # app.run('127.0.0.1')
    app.run()



   
