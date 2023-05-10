import socket
import time
from tools.reader import read_message
from tools.sender import send_message

PORT = 6969
HOST = '127.0.0.1'
BUFFER_SIZE = 1024
HEADER= 64

FORMAT = 'utf-8'
DISCONNET_MESSAGE = '!DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def start():
    send_message('cliente', client)
    print('\nAsistente: ¡Bienvenido al asistente virtual!. Por favor ingrese sus credenciales.')

    rut = input('usuario:')
    send_message(str(rut), client)
    password = input('constraseña:')
    send_message(str(password), client)

    response = int(read_message(client)) # Informacion or 0

    if response == 1:
        client_name = read_message(client)
    else:
        print('Asistente: Usuario o contraseña incorrectos. La conexión fue cerrada.')
        return False
    while response:
        print(f'\nAsistente: Hola {client_name}, en qué te podemos ayudar?.')

        print('     (1) Reiniciar servicio internet.')
        print('     (2) Reiniciar Clave wifi.')
        print('     (3) Contactar a un ejecutivo.')
        print('     (4) Salir.')
        request = input('\nCliente: ') # Se ingresa la opción que se desea realizar
        
        if request == '1':
            time.sleep(1)
            send_message(request, client)
            print(f'Asistente: Se ha reiniciado su Servicio de Internet.')
            
        elif request == '2':

            print(f'\nAsistente: Por favor, ingresar una nueva contraseña.')
            new_password = input('Clave: ')
            repeat_password = input('Repetir Clave: ')

            while new_password != repeat_password:
                print('Las contraseñas no coinciden, por favor intente nuevamente.')
                print(f'Ingresar nueva contraseña:')
                new_password = input('Clave: ')
                repeat_password = input('Repetir Clave: ')

            print(f'Asistente: Estamos actualizando su clave Wifi.')

            time.sleep(1)    
            send_message(request, client)
            send_message(new_password, client)
            print(f'Asistente: Clave actualizada.')
            time.sleep(1) 

        elif request == '3':
            send_message(request, client)
            response = read_message(client)
            print(f'Asistente: Estimado cliente, actualmente hay {response} ejecutivos disponibles.')
            time.sleep(1)
            msg_rec = int(read_message(client))
            print( f"Asistente: Su lugar en la fila de espera es {msg_rec}." 
                    f"Tiempo estimado de espera de {msg_rec*3} minutos."
                    "Por favor esperar a que un ejecutivo atienda la solicitud.")
            
            assigned = int(read_message(client)) # Mensaje del ejecutivo asignado.
            rut_exec = read_message(client)
            send_message(rut_exec, client)
            print('\n-----------------------------------------------------------\n\n')
            while assigned:
                msg_executive = read_message(client) # Mensaje de entrada
                if len(msg_executive.split(' ')) > 1:
                    msg_servidor = msg_executive.split(' ')[0] + ' ' + msg_executive.split(' ')[1]
                    if msg_servidor == '[AVISO SERVIDOR]':
                        print(f'{msg_executive}')
                        continue
                if msg_executive == '2': # Se debe introducir una nueva contraseña
                    print(f'Asistente: Estimado cliente, se ha reiniciado su clave Wifi.')
                    print(f'Asistente: Por favor, ingresar una nueva contraseña.')
                    while True:
                        new_password = input('Clave: ')
                        repeat_password = input('Repetir Clave: ')
                        if new_password!=repeat_password:
                            print('Las contraseñas no coinciden, por favor intente nuevamente.')
                            continue
                        break
                    send_message('new_password', client)
                    send_message(new_password, client)
                    continue
                if msg_executive== DISCONNET_MESSAGE:
                    send_message('0', client)
                    print(f'Asistente: Estimado cliente, se ha cerrado la sesión.')
                    print('-------------------------------------------------------')
                    break

                print(f'Ejecutivo: {msg_executive}')

                msg_client = input('Cliente: ')
                send_message(msg_client, client)
               
        elif request == '4':
            send_message(input('Asistente: Presionar una tecla para terminar la conexión.'), client)
            send_message(DISCONNET_MESSAGE, client)
            print(f'Asistente: Estimado cliente, se ha cerrado la sesión.')
            response = 0

start()
print('--------------------------------------------------------------------------------')