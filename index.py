import pandas as pd
from flask import Flask, request, Response

# csv = pd.read_csv('equipamentos.csv', encoding='latin-1') #forma de ler a csv 
# print(csv) #printar a csv

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


if __name__ == '__main__':
    # app.run('127.0.0.1')
    app.run()
