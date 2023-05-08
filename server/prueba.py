import json

def read_json(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data

DBEXECUTIVE = read_json('server/executive_database.json')

connected_executive = [key for key, user in DBEXECUTIVE.items() if user['connection'] and user['available']]
print(connected_executive)