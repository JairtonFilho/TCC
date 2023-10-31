from robot.connection import Connection
from robot.gen3.api_gen3.device_connection import DeviceConnection


class ConnectGen3(Connection):
    route = None

    def __init__(self, ip_address, credentials):
        self.ip_address = ip_address
        self.credentials = credentials

        self.connect_instance = DeviceConnection(ip_address=self.ip_address,
                                                 credentials=(credentials[0], credentials[1]))

    def connect_robot(self):
        # TODO: Aqui pode-se instanciar as classes e métodos de conexão do Gen3
        # TODO: Ver o repo sistema-votacao-backend-legacy
        # TODO: Passar como parâmetro o necessário para a conexão: IP, user e password

        self.route = self.connect_instance.connect()

        return self.route

    def disconnect_robot(self):
        # TODO: Lembrar de estruturar a classe de conexão para que o método de desconexão não depender da instancia
        # TODO: Atualmente, é dependente da mesma instancia

        self.connect_instance = self.connect_instance.disconnect()
