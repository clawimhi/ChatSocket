from tools.managment_json import read_json, write_json
import server
import time

def main():
    client_dababase = read_json('server/client_database.json')
    executive_database = read_json('server/executive_database.json')

    for key, value in client_dababase.items():
        client_dababase[key]['connection'] = False
    for key, value in executive_database.items():
        executive_database[key]['connection'] = False

    write_json('server/client_database.json', client_dababase)
    write_json('server/executive_database.json', executive_database)
    time.sleep(1)
    server.start()
    
if __name__ == '__main__':
    main()