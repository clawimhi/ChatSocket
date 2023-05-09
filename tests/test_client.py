import unittest
import subprocess


def test_interaction():
    # Definimos las entradas que queremos proporcionar
    inputs = "4\n1\n3\n"

    # Ejecutamos el script del servidor y redirigimos su entrada estándar desde un pipe
    p1 = subprocess.Popen(["python", "server.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Ejecutamos el script del cliente y redirigimos su salida estándar a la entrada del servidor
    p2 = subprocess.Popen(["python", "client.py"], stdin=subprocess.PIPE, stdout=p1.stdin)


    # Enviamos las entradas al servidor
    for i in range(3):
        print((inputs[i] + '\n'))
        p2.stdin.write((inputs[i] + '\n').encode())
        output = p1.stdout.readline().decode().strip()
        print(output)

if __name__ == '__main__':
    test_interaction()