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