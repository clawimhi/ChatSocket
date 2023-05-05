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