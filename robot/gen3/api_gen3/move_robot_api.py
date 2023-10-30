import threading
import time

from kortex_api.autogen.messages import Base_pb2

# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 10


# TODO: Classe de movimentação adaptada dos exemplos disponibilizados pela API.
# TODO: Essa classe é a única (até agora) que tem contato direto com a base (CPU) do Gen3
class MoveRobotApi:
    # Create closure to set an event after an END or an ABORT
    @staticmethod
    def check_for_end_or_abort(error):
        def check(notification, e=error):
            if notification.action_event == Base_pb2.ACTION_END or notification.action_event == Base_pb2.ACTION_ABORT:
                e.set()

        return check

    @staticmethod
    def move_to_home(base):
        # Make sure the arm is in Single Level Servoing mode
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        base.SetServoingMode(base_servo_mode)

        # Move arm to ready position
        action_type = Base_pb2.RequestedActionType()
        action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
        action_list = base.ReadAllActions(action_type)
        action_handle = None
        for action in action_list.action_list:
            if action.name == "Home":
                action_handle = action.handle

        if action_handle is None:
            print("Can't reach safe position. Exiting")
            return False

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            base.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        base.ExecuteActionFromReference(action_handle)
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            print("Safe position reached")
        else:
            print("Timeout on action notification wait")
        return finished

    @staticmethod
    def populateAngularPose(jointPose, durationFactor):
        waypoint = Base_pb2.AngularWaypoint()
        waypoint.angles.extend(jointPose)
        waypoint.duration = durationFactor * 5.0

        return waypoint

    # TODO: Método utilizado para mover o robô para waypoints definidos.
    def move_trajectory(self, base, joints_list):
        base_servo_mode = Base_pb2.ServoingModeInformation()
        base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
        base.SetServoingMode(base_servo_mode)

        joint_poses = joints_list

        waypoints = Base_pb2.WaypointList()
        waypoints.duration = 0.0
        waypoints.use_optimal_blending = False

        index = 0
        for joint_pose in joint_poses:
            waypoint = waypoints.waypoints.add()
            waypoint.name = "waypoint_" + str(index)
            durationFactor = 1
            # Joints/motors 5 and 7 are slower and need more time
            if index == 4 or index == 6:
                durationFactor = 6  # Min 30 seconds

            waypoint.angular_waypoint.CopyFrom(self.populateAngularPose(joint_pose, durationFactor))
            index = index + 1

            # Verify validity of waypoints
        result = base.ValidateWaypointList(waypoints)
        if len(result.trajectory_error_report.trajectory_error_elements) == 0:

            e = threading.Event()
            notification_handle = base.OnNotificationActionTopic(
                self.check_for_end_or_abort(e),
                Base_pb2.NotificationOptions()
            )

            print("Reaching angular pose trajectory...")

            base.ExecuteWaypointTrajectory(waypoints)

            print("Waiting for trajectory to finish ...")
            finished = e.wait(TIMEOUT_DURATION)
            base.Unsubscribe(notification_handle)

            if finished:
                print("Angular movement completed")
            else:
                print("Timeout on action notification wait")
            return finished
        else:
            print("Error found in trajectory")
            print(result.trajectory_error_report)
            return finished

    # TODO: O método move_joints chama esse método para mover as juntas.
    def angular_movement(self, base, joints_list):
        # Starting angular action movement
        action = Base_pb2.Action()
        action.name = "Angular action movement"
        action.application_data = ""

        # Place arm straight up
        joint_id = 1
        for joint_value in joints_list:
            joint_angle = action.reach_joint_angles.joint_angles.joint_angles.add()
            joint_angle.joint_identifier = joint_id
            joint_angle.value = joint_value
            joint_id += 1

        e = threading.Event()
        notification_handle = base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        # Executing action
        base.ExecuteAction(action)

        # Waiting for movement to finish
        finished = e.wait(TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            pass
        else:
            print("Timeout on action notification wait")
        return finished

    # TODO: Função para fechar a garra. Ver outra opção ao time sleep.
    def close_gripper(self, base):

        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = 1
        base.SendGripperCommand(gripper_command)

        time.sleep(2)

    # TODO: Função para abrir a garra. Ver outra opção ao time sleep.
    def open_gripper(self, base):

        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = 0
        base.SendGripperCommand(gripper_command)

        time.sleep(2)

    @staticmethod
    def send_joint_speeds(base, speeds_list):
        joint_speeds = Base_pb2.JointSpeeds()

        joint_id = 0
        for speed in speeds_list:
            joint_speed = joint_speeds.joint_speeds.add()
            joint_speed.joint_identifier = joint_id
            joint_speed.value = speed
            joint_speed.duration = 0
            joint_id += 1

        base.SendJointSpeedsCommand(joint_speeds)