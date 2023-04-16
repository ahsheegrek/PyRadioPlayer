import json

#ラジオ局の情報をjsonから取得
def load_stations(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)