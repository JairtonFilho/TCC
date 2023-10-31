import threading
import cv2
from robot.gen3.connect_gen3 import ConnectGen3
from robot.gen3.move_gen3 import MoveGen3
import time

# Posições 0, 45, 135, 180, 225, 315 3 360 altura max e med

qtd_posicoes = 6

def move_position(position, route, number):
    #alto
    if number == 1:
        print("Altura - máx")
        if position == 0:
            joints = [7.37, 21.20, 107.36, 268.24, 290.87, 94.33]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P1")

        if position == 1:
            joints = [310.53, 348.25, 72.73, 289.8, 279.29, 36.6]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P2")

        if position == 2:
            joints = [4.44, 357.64, 88.05, 269.6, 294.98, 91.26]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P3")

        if position == 3:
            joints = [54.75, 13.75, 106.82, 250.02, 287.86, 145.11]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P4")

        if position == 4:
            joints = [14.11, 60.88, 118.57, 266, 261.45, 99.54]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P5")

        if position == 5:
            joints = [2.16, 331.96, 54.5, 270.1, 264.18, 88.89]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P6")

    #médio
    if number == 2:
        print("Altura - med")
        if position == 0:
            joints = [3.7, 346.3, 124.56, 269.68, 342.88, 90.66]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P1")

        if position == 1:
            joints = [350.24, 343.33, 117, 284.15, 336.9, 65.05]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P2")

        if position == 2:
            joints = [1.81, 325.91, 91.41, 271.44, 329.87, 87.42]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P3")

        if position == 3:
            joints = [21.81, 346.16, 130.52, 238.37, 345.57, 137.76]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P4")

        if position == 4:
            joints = [4.37, 9.25, 150.2, 268.7, 345.38, 92.35]
            MoveGen3().move_robot(route, 'calibration', joints)
            print("P5")

        if position == 5:
            joints = [1.8, 318.26, 61.99, 270.69, 283, 88.22]
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
    time.sleep(150)

    while True:
        entrada = input("Selecione a altura (1/2/sair ): ").upper()
        if entrada == "1":
            calibration(route, 1)
        if entrada == "2":
            calibration(route, 2)
        if entrada == "SAIR":
            break

    # Desconexão e movimento para o zero
    video_thread.join()
    MoveGen3().move_robot(route, 'zero')
    robot_instance.disconnect_robot()


if __name__ == '__main__':
    main()

