from tools.sender import send_message
from tools.reader import read_message
from tools.managment_json import read_json, write_json
import threading
DBCLIENT = read_json('server/client_database.json')

def status(conn):
    send_message('STATUS', conn)
    return read_message(conn)

def details(conn):
    send_message('DETAILS', conn)
    return read_message(conn)

def connect(conn):
    send_message('CONNECT', conn)
    return read_message(conn)






def command_executive(conn, request, name):
    if request == 'status':
        print(f'\n{status(conn)} clientes conectados.\n')

    elif request == 'details':
        response = details(conn)
        for key, value in response.items():
            print(f'usuario {key}  - {value}')

    elif request == 'history':
        pass
    elif request == 'info':
        pass
    elif request == 'restart internet':
        pass
    elif request == 'restart wifi':
        pass
    

def connect_w(conn, name):
    send_message('CONNECT', conn)
    while True:
        client_msg = read_message(conn)
        print(f'[CLIENTE]: {client_msg}')

        message_executive = input(f'[EJECUTIVO {name.upper()}]:')
        if message_executive[0] == ':':
            message_executive = message_executive.split(' ')[0]
            command_executive(conn, message_executive[1:], name)
            message_executive = input(f'[EJECUTIVO {name.upper()}]:')
        send_message(message_executive, conn)
