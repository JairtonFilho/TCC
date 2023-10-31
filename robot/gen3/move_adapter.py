from robot.gen3.api_gen3.move_robot_api import MoveRobotApi


class MoveAdapter:
    # TODO: Tirar o self caso quebre o programa
    def move_joints(self, base, joints_list):
        MoveRobotApi().angular_movement(base, joints_list)

    # TODO: Levar para o módulo da API o movimento cartesiano
    def move_cartesian(self, base, cartesian_list):
        pass

    def move_home(self, base):
        MoveRobotApi().move_to_home(base)

    def move_zero(self, base):
        joints_list = [0, 0, 0, 0, 0, 0]
        MoveRobotApi().angular_movement(base, joints_list)

    def open_gripper(self, base):
        MoveRobotApi().open_gripper(base)

    def close_gripper(self, base):
        MoveRobotApi().close_gripper(base)