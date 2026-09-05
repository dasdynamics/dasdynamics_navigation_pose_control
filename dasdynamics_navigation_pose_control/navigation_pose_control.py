import os
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator

class NavigationPoseControlNode (Node):
    def __init__(self):

        # Файлы с точками
        self.waypoints_file = os.path.expanduser('~/waypoints.yaml')
        self.waypoints = self.load_waypoints()

        # Навигатор
        self.navigator = BasicNavigator()

        # Текущая поза
        self.current_pose = None
        self.pose_subscription = self.create_subscription(
            PoseStamped,
            '/amcl_pose'
        )
