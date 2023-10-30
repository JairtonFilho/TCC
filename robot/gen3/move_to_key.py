# TODO: Essa classe recebe um número para votar e busca os valores de juntas em um dicionário que é recuperado
# TODO: através de um JSON gerado por uma tabela com os ângulos de juntas mapeados. Recebe um número, busca esse número
# TODO: em um dicionário e recupera os ângulos associados ao número (que é uma key).
import json
import os

from robot.gen3.move_adapter import MoveAdapter

cwd = os.getcwd()


class MoveToKey:
    def move_to_key(self, base, number_key):
        # TODO: Recuperar os números através do JSON para realizar a votação
        with open(cwd + '/gen3/keys_repository/keys_joints_angles.json', 'r') as js:
            data = json.load(js)
            approach_key = data[str(number_key)][0]
            press_key = data[str(number_key)][1]

        # TODO: Passar os ângulos recuperados através do dicionário/JSON como parâmetro usando o move_joints do adapter
        MoveAdapter().move_joints(base, approach_key)
        MoveAdapter().move_joints(base, press_key)
        MoveAdapter().move_joints(base, approach_key)
