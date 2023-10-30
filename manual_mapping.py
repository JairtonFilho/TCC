from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
import device_connection

router = device_connection.DeviceConnection('192.168.2.10', 10000, credentials=('admin', 'admin'))  # 172.22.66.92
router = router.connect()
base = BaseClient(router)
base_cyclic = BaseCyclicClient(router)

while True:
    lista_valor_atual_juntas = []
    feedback = base_cyclic.RefreshFeedback()
    input("Pressione ENTER para apresentar o valor atual das juntas: ")
    for i in range(0, 6):
        lista_valor_atual_juntas.append(round(feedback.actuators[i].position, 3))
    print(lista_valor_atual_juntas)