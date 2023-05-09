import random

# Lista para almacenar los números de transacción generados
TRANSACTION_NUMBER =[]

def transaction_number_generator():
    while True:
        transaction_number = ''.join(random.choices('0123456789', k=10))
        if transaction_number not in TRANSACTION_NUMBER:
            TRANSACTION_NUMBER.append(transaction_number)
            break
    return transaction_number

# Se busca información en el archivo .log por el id de transacción
def search_transaction(path_log, transaction_number):
    result = []
    with open(path_log, 'r') as file:
        for line in file:
            if transaction_number in line:
                result.append(line)
    return result