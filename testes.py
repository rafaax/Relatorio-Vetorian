import pandas as pd
import numpy as np
from flask import Flask, request, Response
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
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

    def velocidade_excedida(row):
        if row is False:
            return 'background-color: red'
        else:
            return '' 
    

    styled_df = df_raw.style.applymap(lambda x: f'color: {"red" if isinstance(x,str) else "black"}''')\
                                        .applymap(velocidade_excedida, subset='velocidade_excedida')
                                
    styled_df.index = pd.RangeIndex(len(styled_df.index))

    # styled_df = df_raw.style.applymap(velocidade_excedida, subset='velocidade_excedida')
    # styled_df = df_raw.style.applymap(pos_id, subset='pos_id')

    styled_df.to_excel('relatorio_estilizado.xlsx', index=False)

    return 'ok'



@app.route('/vetorian/natal', methods=['POST'])
def natal():

    file = request.files['file']
    df_raw = pd.read_csv(file, sep=';')

    def is_christmas(df1, df2):
        if (df1.month == 12 and df1.day == 25) and (df2.month == 12 and df2.day == 25) :
            return True
        else:
            return False

    def ultrapassado(velocidade, pos_id):
        velocidade = int(velocidade)
        pos_id = int(pos_id)
        if  velocidade > pos_id :
            if velocidade <= 100:
                tol = 1.1
                velocidadextol = velocidade*tol
                if velocidadextol > pos_id:
                    velocidadeExcedida =  (((velocidadextol / pos_id)  * 100) - 100)

                    return velocidadeExcedida
            else:
                tol = 1.07
                velocidadextol = velocidade*tol
                if velocidadextol > pos_id:
                    velocidadeExcedida =  (((velocidadextol / pos_id)  * 100) - 100)
                    return velocidadeExcedida

        else:
            return False


    df = pd.DataFrame({'velocidade': ['30', '50', '35', '19'],
                        'pos_id': ['50', '40', '30', '20'] })

    # df['Data'] = pd.to_datetime(df['Data'])
    # df['Data2'] = pd.to_datetime(df['Data2'])

    # df['Natal'] = df.apply(lambda row: is_christmas(row['Data'], row['Data2']), axis=1)
    df['ultrapassada'] = df.apply(lambda row: ultrapassado(row['velocidade'], row['pos_id']), axis=1)
    
    print(df)

    return df.to_dict(orient='records')


    

if __name__ == '__main__':
    # app.run('127.0.0.1')
    app.run()