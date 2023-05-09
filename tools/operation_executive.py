from tools.sender import send_message
from tools.reader import read_message
from tools.managment_json import read_json, write_json
import threading

DISCONNECT_MESSAGE = '!DISCONNECT'

def status(conn):
    send_message('STATUS', conn)
    return read_message(conn)

def details(conn):
    send_message('DETAILS', conn)
    response = int(read_message(conn))
    dicc = {}
    for k in range(response):
        rut = read_message(conn)
        action = read_message(conn)
        dicc[rut] = action
    return dicc

def connect(conn):
    send_message('CONNECT', conn)
    return read_message(conn)

def history(conn):
    send_message('HISTORY', conn)
    response = int(read_message(conn))
    history = []
    for k in range(response):
        history.append(read_message(conn))
    return history

def info(conn, rut_client):
    send_message('INFO', conn)
    msg = input(':')
    send_message(str(msg), conn) # Se envía de información del cliente
    send_message(str(rut_client), conn) # Se envia el rut del cliente
    

def command_executive(conn, request, name, rut_client = None):
    if request == 'status':
        print(f'\n{status(conn)} clientes conectados.\n')

    elif request == 'details':
        response = details(conn)

        for key, value in response.items():
            print(f'usuario {key}  - {value}')

    elif request == 'history':
        if not rut_client:
            print('No se ha abierto una conexión con un cliente. No es posible ver el historial.')
        else:
            response = history(conn)
            if not response:
                print('No hay historial de transacciones.')
            else:
                for k in response:
                    print(k, end='\n')
    
    elif request == 'info':
        if not rut_client:
            print('No se ha abierto una conexión con un cliente. No es posible ver el historial.')     
        else:
            info(conn, rut_client) 
    elif request == 'restart internet':
        pass
    elif request == 'restart wifi':
        pass
    elif request == 'disconnection':
        if not rut_client:
            print('No se ha abierto una conexión con un cliente. No es posible desconectar.')


def connect_w(conn, name):
    send_message('CONNECT', conn)
    response = int(read_message(conn)) #Rut del cliente
    if not response:
        print('No hay clientes esperando en la cola.')
    n = 0
    while response:
        if n == 0:
            client_msg = read_message(conn)
            print(f'[CLIENTE]: {client_msg}')

        message_executive = input(f'[EJECUTIVO {name.upper()}]:')

    
        if message_executive[0] == ':':
            message_executive = message_executive.split(' ')[0][1:]
            if message_executive == 'close':
                send_message(DISCONNECT_MESSAGE, conn)
                break
            command_executive(conn, message_executive, name, rut_client= response)
            n=1
            continue

        send_message(message_executive, conn)
        n = 0

