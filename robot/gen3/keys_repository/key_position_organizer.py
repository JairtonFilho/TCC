import pandas
import json
import os


class KeyPositionsOrganizer:
    @staticmethod
    def create_json_file(csv_file_path):
        key_positions = {}
        df = pandas.read_csv(csv_file_path)
        for i in range(len(df['Tecla'])):
            pos_app = df['Posição de aproximação'][i].split(',')
            pos_press = df['Posição de pressionamento'][i].split(',')
            pos_app = [float(x.replace(" ", '')) for x in pos_app if len(x) > 2]
            pos_press = [float(y.replace(" ", '')) for y in pos_press if len(y) > 2]
            key_positions[df['Tecla'][i]] = [pos_app, pos_press]
        half_path = os.getcwd()
        with open(half_path + '/keys_joints_angles.json', 'w') as js:
            json.dump(key_positions, js)


# TODO: Executar isso em algum lugar para gerar o JSON com as teclas
cwd = os.getcwd()
KeyPositionsOrganizer.create_json_file(cwd + '/teclas.csv')
