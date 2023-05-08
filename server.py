import socket
import threading
import logging
from tools.reader import read_message
from tools.sender import send_message
from tools.managment_json import read_json, write_json
from tools.transaction_id import transaction_number_generator
from tools.logger import extendable_logger
from tools.managment_json import last_request_client
from functools import partial, partialmethod

PORT = 6969
HOST = '127.0.0.1'
LISTEN_QUEUE = 10
BUFFER_SIZE = 1024
HEADER= 64
FORMAT = 'utf-8'
DISCONNET_MESSAGE = '!DISCONNECT'
CLIENT_DB = 'server/client_database.json'
EXECUTIVE_DB = 'server/executive_database.json'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

logging.TRACE = 9
logging.addLevelName(logging.TRACE, 'TRACE')
logging.Logger.trace = partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = partial(logging.log, logging.TRACE)

DBCLIENT= read_json(CLIENT_DB)
DBEXECUTIVE = read_json(EXECUTIVE_DB)

executive_info = {}
queue_client = []

active_client = 0 
def handle_client(conn, addr):
    print(f'[PETICION DE CONEXION] {addr}.')
    connect = True

    rut = read_message(conn)
    password = read_message(conn)

    if rut in DBCLIENT.keys():
        if DBCLIENT[rut]['connection']:
            send_message('0', conn)
            connect = False

        elif password == DBCLIENT[rut]['password'] and not DBCLIENT[rut]['connection']:
            send_message('1', conn)
            send_message(DBCLIENT[rut]['name'], conn)
            DBCLIENT[rut]['connection'] = True
            write_json(CLIENT_DB, DBCLIENT)

            transaction_number = transaction_number_generator()
            print(f'[CONEXIÓN] Cliente {DBCLIENT[rut]["name"]} {DBCLIENT[rut]["lastname"]} conectado.')
            logger = extendable_logger(str(rut), f'server/logs/{rut}.log', level= logging.TRACE)
               
        else:
            send_message('0', conn)
            connect = False
    else:
        send_message('0', conn)
        connect = False
        conn.close()

    while connect: # Se mantiene la conexión mientras el cliente no se desconecte
        msg = read_message(conn)
        if msg == DISCONNET_MESSAGE:
            print(f'[DESCONEXIÓN] Cliente {DBCLIENT[rut]["name"]} {DBCLIENT[rut]["lastname"]} desconectado.')
            DBCLIENT[rut]['connection'] = False
            write_json(CLIENT_DB, DBCLIENT)
            connect = False  
            logger.handlers = []

        if msg == '1': # Reiniciar servicio de internet
            print(f'[REINICIAR SERVICIO] Cliente {DBCLIENT[rut]["name"]} {DBCLIENT[rut]["lastname"]} reinició su servicio de internet.')
            logger.trace(f'N1 [REINICIAR SERVICIO] - ({transaction_number}) reinicio de servicio exitoso.')

        if msg == '2': # Cambiar contraseña
            new_password = read_message(conn)
            DBCLIENT[rut]['wifi-password'] = new_password
            write_json(CLIENT_DB, DBCLIENT)        
            print(f'[CONTRASEÑA CAMBIADA] Cliente {DBCLIENT[rut]["name"]} {DBCLIENT[rut]["lastname"]} cambió su contraseña.')
            
            logger.trace(f'N2 - [CONTRASENA CAMBIADA] ({transaction_number}) cambio de contrasena exitoso.')
        
        if msg == '3': # Contactarse con un ejecutivo.
            connected_executive = [key for key, user in DBEXECUTIVE.items() if user['connection']]
            queue_client.append((rut, conn))
            send_message(str(len(connected_executive)), conn)
            send_message(str(len(queue_client)), conn)

            rut_exec = read_message(conn)
            con_exec = executive_info[rut_exec]
            while True:
                msg = read_message(conn) # Se lee mensaje del cliente
                send_message(msg, con_exec) # Se envía mensaje al ejecutivo
                
     

    conn.close()

def handle_admin(conn, addr):
    print(f'[NUEVA CONEXIÓN EJECUTIVO] {addr} CONECTADO.')
    connect = True

    # Se autentica al ejecutivo
    rut = read_message(conn)
    password = read_message(conn)

    if rut in DBEXECUTIVE.keys():
        if DBEXECUTIVE[rut]['connection']:
            send_message('0', conn)
            connect = False

        elif password == DBEXECUTIVE[rut]['password'] and not DBEXECUTIVE[rut]['connection']:
            send_message('1', conn)
            send_message(DBEXECUTIVE[rut]['name'], conn)
            DBEXECUTIVE[rut]['connection'] = True
            write_json(EXECUTIVE_DB, DBEXECUTIVE)
            executive_info[rut] = conn
            print(f'[CONEXIÓN] Ejecutivo {DBEXECUTIVE[rut]["name"]} conectado.')

        else:
            send_message('0', conn)
            connect = False

    # se comienza a escuchar al ejecutivo
    while connect:
        msg = read_message(conn)
        if msg == 'STATUS':
            active_client = sum([1 for user in DBCLIENT.values() if user['connection']]) # Se actualiza la cantidad de clientes conectados
            send_message(str(active_client), conn)
    
        if msg == 'DETAILS':
            latest_action = {}
            rut_connected_client = [key for key, user in DBCLIENT.items() if user['connection']]

            send_message(str(len(rut_connected_client)), conn) #Se informa cuantos mensajes se enviarán para preparar al cliente para recibirlos.

            for rut in rut_connected_client:
                latest_action[rut] = last_request_client(rut)

            for rut, action in latest_action.items():
                send_message(rut, conn)
                send_message(action, conn)
                
        if msg == 'CONNECT':
            if len(queue_client):
                rut_client, conn_client = queue_client.pop(0)
            send_message('1', conn_client)
            send_message(str(rut),conn_client)
            send_message('hola', conn_client)
            while True:
                response = read_message(conn) # Se lee mensaje del ejecutivo
                if response == 'STATUS':
                    active_client = sum([1 for user in DBCLIENT.values() if user['connection']]) # Se actualiza la cantidad de clientes conectados
                    send_message(str(active_client), conn)
                else:
                    send_message(response, conn_client) # Se envía al cliente

    conn.close()

def start():
    print(f'[INICIANDO] Servidor iniciado en {HOST}:{PORT}.')
    server.listen(LISTEN_QUEUE)
    print(f'[ESCUCHANDO] Servidor escuchando...')
    while True:
        conn, addr = server.accept() # 'conn' socket para comunicarse con el cliente, 'addr' es la dirección del cliente
        usertype = read_message(conn)
        if usertype:
            if usertype == 'cliente':
                thread = threading.Thread(target=handle_client, args=(conn, addr)).start()
            elif usertype == 'ejecutivo':
                thread = threading.Thread(target=handle_admin, args=(conn, addr)).start()
            else:
                conn.send('Tipo de usuario no válido. Cierre de conexión'.encode(FORMAT))
                conn.close()
        print(f'[CONEXIONES ACTIVAS] {threading.active_count() - 1}')   # Se resta 1 porque el hilo principal es el que cuenta las conexiones