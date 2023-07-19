import pandas as pd
import numpy as np
from flask import Flask, request, Response
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import PatternFill

app = Flask(__name__)

def ultrapassado(velocidade, pos_id):
    velocidade = int(velocidade)
    pos_id = int(pos_id)
    if  velocidade > pos_id :
        if velocidade <= 100:
            tol = 1.1
            velocidadextol = pos_id*tol
            print(velocidadextol)
            if velocidade > velocidadextol :
                velocidadeExcedida =  ((velocidade / pos_id) - 1) * 100

                return velocidadeExcedida
            else:
                return False
        else:
            tol = 1.07
            velocidadextol = pos_id*tol
            if velocidade > velocidadextol:
                velocidadeExcedida =  ((velocidade / pos_id) - 1) * 100
                return velocidadeExcedida
            else:
                return False
    else:
        return False


@app.route('/vetorian/relatorio', methods=['POST'])
def relatorio_teste1():
    file = request.files['file']
    df = pd.read_csv(file, sep=';')

    df = df[df['velocidade'] > 5] 
    df['ultrapassada'] = df.apply(lambda row: ultrapassado(row['velocidade'], row['pos_id']), axis=1)
    
    print(df)

    return 'ok'



if __name__ == '__main__':
    # app.run('127.0.0.1')
    app.run()
