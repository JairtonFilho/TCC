import threading
import cv2
from robot.gen3.connect_gen3 import ConnectGen3
from robot.gen3.move_gen3 import MoveGen3
import time

# altura min

qtd_posicoes = 6

def move_position(position, route, number):

    if number == 1:
        print("Altura - min")
        if position == 0:
            joints = [4.18, 349.25, 133.18, 265.08, 350.3, 95.62]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P1")

        if position == 1:
            joints = [313.83, 323.4, 83.37, 298.05, 314.55, 23.31]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P2")

        if position == 2:
            joints = [5, 335.95, 112.88, 265.92, 343.21, 95.41]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P3")

        if position == 3:
            joints = [25.74, 354.09, 138.38, 230.34, 345.38, 148.99]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P4")

        if position == 4:
            joints = [359.46, 355.45, 150.19, 233.75, 1.56, 122.94]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P5")

        if position == 5:
            joints = [2.16, 321.67, 86.64, 270.16, 306.39, 88.82]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P6")


def calibration(route, number):
    i = 0
    while i < qtd_posicoes:
        move_position(i, route, number)
        time.sleep(1)
        i += 1

def video():

    cap = cv2.VideoCapture(1)
    cap.set(3, 3840)
    cap.set(4, 2160)

    if (cap.isOpened() == False):
        print("Erro ao abrir a câmera")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    result = cv2.VideoWriter('video.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             30, size)

    while (True):
        ret, frame = cap.read()

        if ret == True:
            result.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    result.release()

    cv2.destroyAllWindows()

    print("Video salvo")

def main():
    # Conexão do robô (ip cabo: 192.168.2.11)
    robot_instance = ConnectGen3("192.168.2.10", ["admin", "admin"])
    route = robot_instance.connect_robot()
    MoveGen3().move_robot(route, 'close')

    video_thread = threading.Thread(target=video)
    video_thread.start()
    print("Abrindo câmera")
    time.sleep(170)

    while True:
        entrada = input("Selecione a altura (1/sair ): ").upper()
        if entrada == "1":
            calibration(route, 1)
        if entrada == "SAIR":
            break

    # Desconexão e movimento para o zero
    video_thread.join()
    MoveGen3().move_robot(route, 'zero')
    robot_instance.disconnect_robot()


if __name__ == '__main__':
    main()
