from robot.gen3.connect_gen3 import ConnectGen3
from robot.gen3.move_gen3 import MoveGen3
import time


#TODO: teste utilizando variações no threshold no canny e usando uma lista de posições


def move_position(position, route, cap=None):

    if position == 1:
        joints = [351.31, 327.55, 99.99, 351.82, 355.17, 359.85]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P1")

    if position == 2:
        joints = [337.86, 323.87, 93.91, 342.45, 344.94, 0.47]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P2")

    if position == 3:
        joints = [331.37, 320.45, 87.56, 335.90, 339.16, 3.06]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P3")

    if position == 4:
        joints = [330.74, 323.24, 92.82, 341.76, 339.53, 357.6]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P4")

    if position == 5:
        joints = [335.53, 326.34, 98.29, 349.42, 343.79, 353.43]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P5")

    if position == 6:
        joints = [352, 331.70, 105.36, 3.06, 355.65, 350.35]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P6")

    if position == 7:
        joints = [343.12, 325.90, 107.06, 21.37, 347.82, 323.72]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P7")

    if position == 8:
        joints = [332.16, 320.76, 97.74, 355.43, 341.26, 342.85]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P8")

    if position == 9:
        joints = [328.04, 318.40, 93.06, 347.45, 338.06, 347.45]
        MoveGen3().move_robot(route, 'calibration', joints)
        print("P9")


# TODO: FAZER TRATAMENTO DE EXCEÇÃO CASO NAO HAJA NA LISTA
def calibration(route, cap=None):
    i = 1

    while i <= 9:
        move_position(i, route, cap)
        time.sleep(1)
        i += 1


def main():
    # Conexão do robô (ip cabo: 192.168.2.11)
    robot_instance = ConnectGen3("192.168.2.10", ["admin", "admin"])
    route = robot_instance.connect_robot()
    MoveGen3().move_robot(route, 'close')

    calibration(route)

    # Desconexão e movimento para o zero
    MoveGen3().move_robot(route, 'zero')
    robot_instance.disconnect_robot()


if __name__ == '__main__':
    main()
# TODO: testar mais tratamentos de imagem--
# TODO: testar o rastreamento com a função e depois treinar o yolo pra testar com ele.
# TODO: Verificar a possibilidade de fazer a ánelise cega com a repartição das unidades da tela
# img = cv2.imread('C:/Users/jsff/Desktop/TCC/Gen3/frames/frame_recortado_manualmente/iluminacao_natural9.jpg')
# a = move_position(img)
# print(a)