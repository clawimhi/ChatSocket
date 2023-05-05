HEADER = 64
FORMAT = 'utf-8'

def read_message(conn):
    msg = ''
    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
    except ValueError:
        print('No se recibió ningún mensaje')
    return msg