import socket 
from tools.sender import send_message
from tools.reader import read_message
from tools.operation_executive import status, details, command_executive, connect_w
import threading
PORT = 6969
BUFFER_SIZE = 1024
HEADER= 64
HOST = '127.0.0.1'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

executive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
executive.connect((HOST, PORT))

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
        name = read_message(executive) # Nombre del ejecutivo
        print(f'Hola {name}, en estos momentos hay:')
        num_connection = status(executive)
        print(f'{num_connection} clientes conectados.')
        print('comandos permitidos :\n\n [:status, :details, :history, :info, :restart internet, :restart wifi, :connect, :close]\n')

    while response: # se mantiene la conexión solo si la información es correcta.
        request = input(f'[EJECUTIVO {name.upper()}]: ')
        if len(request):
            if request[0] == ':':
                request = request.split(' ')[0]
                command_executive(executive, request[1:], name)
                if request[1:] == 'connect':  
                    connect_w(executive, name)

            elif request == DISCONNECT_MESSAGE:
                input('Asistente: Presionar espacio para terminar la conexión')
                send_message(DISCONNECT_MESSAGE, executive)
                break
    
start()
    