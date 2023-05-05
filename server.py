import socket
import threading
import logging
from tools.reader import read_message
from tools.sender import send_message
from tools.managment_json import read_json, write_json
from tools.transaction_id import transaction_number_generator
from tools.logger import extendable_logger
from functools import partial, partialmethod

HOST = '127.0.0.1'
PORT = 6969
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
            DBCLIENT[rut]['connection'] = False #Cambiar a True
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
        
    conn.close()

#Cambio en el codigo

def handle_admin(conn, addr):
    print(f'[NUEVA CONEXIÓN EJECUTIVO] {addr} CONECTADO.')

    while True:
        msg = read_message(conn)
        if msg == DISCONNET_MESSAGE:
            print(f'[DESCONEXIÓN] {addr} DESCONECTADO.')
            break   
        print(f'[{addr}] {msg}')
        conn.send("Msg received".encode(FORMAT))
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
            elif usertype == 'admin':
                thread = threading.Thread(target=handle_admin, args=(conn, addr)).start()
            else:
                conn.send('Tipo de usuario no válido. Cierre de conexión'.encode(FORMAT))
                conn.close()

        print(f'[CONEXIONES ACTIVAS] {threading.active_count() - 1}') # Se resta 1 porque el hilo principal es el que cuenta las conexiones

start()