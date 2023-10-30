from Gen3.robot.gen3.move_adapter import MoveAdapter
from Gen3.robot.gen3.move_to_key import MoveToKey
from Gen3.robot.movement import Movement

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient


class MoveGen3(Movement):
    def move_robot(self, route, move_type, argument=None):
        # TODO: Instanciar a classe de movimentação, seja por juntas ou por movimentos cartesianos
        # TODO: Criar o objeto base passando a rota como parâmetro, esse objeto base pode ser BaseCyclic (cartesian)
        base = BaseClient(route)

        # TODO: Passar o objeto base como parâmetro para a função que chama o move_joints (ou outra função de movimento)
        if move_type == 'key':
            MoveToKey().move_to_key(base, argument)

        elif move_type == 'zero':
            MoveAdapter().move_zero(base)

        elif move_type == 'close':
            MoveAdapter().close_gripper(base)

        elif move_type == 'open':
            MoveAdapter().open_gripper(base)

        # TODO: Criado para o arquivo dance_test
        elif move_type == 'calibration':
            MoveAdapter().move_joints(base, argument)


