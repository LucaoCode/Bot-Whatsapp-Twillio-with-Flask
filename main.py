from flask import Flask, request
from twilio.rest import Client

sid = 'your_account_sid'
aToken = 'your_auth_token'
FROM_NUMBER = "your_twilio_phone_number"

client = Client(sid,aToken)

app = Flask(__name__)

# transform a string of dados_recebidos in a dictionary
# where each parameter is separated by the "&" character and each key-value is separated by the "=" character
def transformar_dados_recebidos_em_dicionario(dados_recebidos):
    dados_enviados = str(dados_recebidos).split('&')
    dicionario_dados_recebidos = {}
    for dado in dados_enviados:
        lista_dado = dado.split("=")
        dicionario_dados_recebidos[lista_dado[0]] = lista_dado[1]
    return dicionario_dados_recebidos


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'Meu site!'
    elif request.method == 'POST':
        print('--- Original Data ---')
        print(request.get_data())
        dados_enviados = transformar_dados_recebidos_em_dicionario(request.get_data())
        print('--- Formated Data ---')
        print(dados_enviados)
        number_from = dados_enviados['WaId']
        if number_from == 'your-number-here':
            client.messages.create(
                from_=FROM_NUMBER,
                body='Hi Name of number!! This is your message',
                to=f'whatsapp:{number_from}'
            )
        else:
            client.messages.create(
                from_=FROM_NUMBER,
                body='Dont know you!',
                to=f'whatsapp:{number_from}'
            )
        return 'Data Processed!', 201
    else:
        return "We have a problem!", 404

if __name__ == "__main__":  
    app.run(debug=True,host='0.0.0.0', port=5000)