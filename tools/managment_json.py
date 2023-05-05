import json

def read_json(file):
    with open(file, 'r') as archivo:
        contenido = archivo.read()
    return json.loads(contenido)

def write_json(file, data):
    try:
        with open(file, 'w') as archivo:
            json.dump(data, archivo, indent=4)
        return True
    except:
        return False
    
def last_request_client(file):
    path_file = f'server/logs/{file}.log' # Ruta del historial de acciones del cliente.
    with open(file,'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1] # Se tomas la ultima linea del archivo. (Ultima acción realizada)
    return last_line