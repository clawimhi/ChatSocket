import logging

FORMATTER = logging.Formatter("[%(asctime)s] %(levelname)s  %(message)s  ",
                              "%Y/%m/%d %H:%M:%S")

def extendable_logger(log_name, file_name,level=logging.INFO):
    """
    Esta función crea un logger con el nombre del cliente y lo guarda en un archivo de log.
    """
    handler = logging.FileHandler(file_name) # Se crea un handler para el archivo de log. Si no existe, se crea uno nuevo.
    handler.setFormatter(FORMATTER) # Se le da formato al handler

    specified_logger = logging.getLogger(log_name) # Se crea un logger con el nombre del cliente. Si no existe, se crea uno nuevo.
    specified_logger.setLevel(level) # Se define el nivel de logging
    
    specified_logger.addHandler(handler) # Se agrega el handler al logger
    return specified_logger

def search_transaction_log(file_log, transaction_id):
    f = open(file_log, 'r')
    return [line for line in f.readlines() if str(transaction_id) in line]

