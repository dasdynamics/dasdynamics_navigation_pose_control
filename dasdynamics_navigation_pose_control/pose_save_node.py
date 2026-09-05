import os
import yaml
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped


class PoseSaveNode (Node):
    def __init__(self):
        super().__init__("pose_save_node")

        # Параметры окружения
        self.command_topic_name = 'command'


        # Файлы с точками
        self.waypoints_file = os.path.expanduser('~/ros2_smart_box_ws/waypoints.yaml')
        self.waypoints = self.load_waypoints()



        # Текущая поза
        self.current_pose = None


        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/pose',
            self.pose_callback,
            10, 
        )

        self.pose_subscription = self.create_subscription(
            String,
            'command',
            self.command_callback,
            10, 
        )

        self.get_logger().info(f'Pose saver node started. Listing on {self.command_topic_name}')


    # Вызываемые функции
    def pose_callback(self, msg:PoseWithCovarianceStamped):
        self.current_pose = msg.pose

    def command_callback(self, msg:String):
        cmd = msg.data.strip()
        self.get_logger().info(f'Received command: {cmd}')

        if cmd.startswith('save'):
            self.handle_save(cmd[5:])
        else:
            self.get_logger().info(f'Unknown command: {cmd}. Use "save:<name>"')


    # Логика
    def load_waypoints(self):
        if os.path.exists(self.waypoints_file):
            with open(self.waypoints_file, 'r') as file:
                data = yaml.safe_load(file) or {}
            return data
        return {}


    def save_waypoints(self):
        with open(self.waypoints_file, 'w') as file:
            yaml.dump(self.waypoints, file, default_flow_style=False)

    def handle_save(self, name:str):
        name = name.strip()
        if not name:
            self.get_logger().info('Save command without name. Use "save:<name>"')
            return 

        if self.current_pose is None:
            self.get_logger().info('No current pose')
            return

        pose = self.current_pose.pose
        self.waypoints[name] = {
            'x': pose.position.x,
            'y': pose.position.y,
            'z': pose.position.z,
            'ox': pose.orientation.x,
            'oy': pose.orientation.y,
            'oz': pose.orientation.z,
            'ow': pose.orientation.w,
        }
        self.save_waypoints()
        self.get_logger().info(f'Save point {name}')


    def handle_go(self, name:str):
        name = name.strip()
        if not name:
            self.get_logger().warn('Go command without name. Use "go:<name>"')
            return

        if name not in self.waypoints:
            self.get_logger().warn(f'Waypoint "{name}" not found')
            return

        wp = self.waypoints[name]

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = wp['x']
        goal.pose.position.y = wp['y']
        goal.pose.position.z = wp['z']
        goal.pose.orientation.x = wp['qx']
        goal.pose.orientation.y = wp['qy']
        goal.pose.orientation.z = wp['qz']
        goal.pose.orientation.w = wp['qw']

        self.get_logger().info(f'Navigating to "{name}"')
        self.navigator.goToPose(goal)

        # Ждём завершения задачи
        while rclpy.ok() and not self.navigator.isTaskComplete():
            pass

        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info(f'Navigated to "{name}" successfully')
        else:
            self.get_logger().error(f'Navigation to "{name}" failed (result={result})')


def main():
    rclpy.init()
    node = PoseSaveNode()
    rclpy.spin(node)
    node.destroy_node()


if __name__ == '__main__':
    main()
