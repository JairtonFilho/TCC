from Gen3.robot.gen3.connect_gen3 import ConnectGen3
from Gen3.robot.gen3.move_gen3 import MoveGen3


class FacadeRobot:
    def __init__(self, robot_type):
        # TODO: Modificar o IP para o 192.168.2.11
        self.ip_address = "172.22.64.105"
        self.robot_type = robot_type
        self.robot_instance = None
        self.route = None

    # TODO: Colocar os condicionais aqui para decidir qual robô conectar
    def connect_robot(self):
        self.robot_instance = ConnectGen3(self.ip_address, ["admin", "admin"])
        self.route = self.robot_instance.connect_robot()

    # TODO: Colocar os condicionais aqui para decidir qual robô desconectar
    def disconnect_robot(self):
        self.robot_instance.disconnect_robot()

    # TODO: Colocar os condicionais aqui para decidir qual robô movimentar
    def move_robot(self, move_type, data_send=None):
        MoveGen3().move_robot(self.route, move_type, data_send)


def main():
    robot_instance = FacadeRobot('gen3')
    robot_instance.connect_robot()

    robot_instance.move_robot('open')
    robot_instance.move_robot('close')

    robot_instance.move_robot('key', 'U1')
    robot_instance.move_robot('key', 'U2')
    robot_instance.move_robot('key', 'U3')

    robot_instance.move_robot('key', 'T1')
    robot_instance.move_robot('key', 'T2')
    robot_instance.move_robot('key', 'T3')

    robot_instance.move_robot('zero')
    robot_instance.disconnect_robot()


if __name__ == "__main__":
    main()
