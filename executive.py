import socket 
from tools.sender import send_message
from tools.reader import read_message

PORT = 6969
BUFFER_SIZE = 1024
HEADER= 64
HOST = '127.0.0.1'
FORMAT = 'utf-8'
DISCONNET_MESSAGE = '!DISCONNECT'

executive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
executive.connect((HOST, PORT))

def status():
    send_message('STATUS', executive)
    response = read_message(executive)
    return response

def details():
    send_message('DETAILS', executive)

    activated_client = int(read_message(executive))
    response = {}
    for i in range(activated_client):
        rut_response = read_message(executive)
        last_request_response = read_message(executive)
        response[rut_response] = last_request_response

    return response

def history():
    pass

def start():
    send_message('ejecutivo', executive)
    print('Asistente: Hola! Bienvenido, Ingrese su RUT y Clave para continuar.')
    rut = input('RUT: ')
    send_message(rut, executive)
    password = input('Clave: ')
    send_message(password, executive)

    response = int(read_message(executive)) # Se recibe un 1 si la información es correcta o un 0 si no lo es.
    if response == 1:
        # name = read_message(executive) #entrego el nombre del ejecutivo
        name = 'Ignacio' # Temporal
        print(f'Hola {name}, en estos momentos hay:')
        print(f'{status()} clientes conectados.')
        print('comandos permitidos :\n\n [:status, :details, :history, :info, :restart internet, :restart wifi, :connect, :close]\n')


    while response: #Se mantiene la conexión solo si la información es correcta.
        request = input(f'{name}: ')
        if request == ':status':
            print(f'\n{status()} clientes conectados.\n')
            print('------------------------------------------------------------------------------------')
        elif request == ':details':
            dicc_response = details()
            for key, value in dicc_response.items():
                print(f'usuario {key}  - {value}')
        elif request == ':history':
            pass
        else:
            print('comando invalido. Intente nuevamente.')
start()
    