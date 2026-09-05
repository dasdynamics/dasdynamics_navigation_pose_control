import os
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator

class NavigationPoseControlNode (Node):
    def __init__(self):

        # Параметры окружения
        self.command_topic_name = 'command'


        # Файлы с точками
        self.waypoints_file = os.path.expanduser('~/waypoints.yaml')
        self.waypoints = self.load_waypoints()



        # Текущая поза
        self.current_pose = None


        self.pose_subscription = self.create_subscription(
            PoseStamped,
            '/amcl_pose',
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
        def pose_callback(self, msg:PoseStamped):
            self.current_pose = msg

        def command_callback(self, msg:String):
            cmd = msg.data.strip()
            self.get_logger().info(f'Received command: {cmd}')

            if cmd.startswith('save'):
                self.handle_save(cmd[5:])
            else:
                self.get_logger().info(f'Unknown command: {cmd}. Use "save:<name>"')


        # Логика
        def save_waypoints(self):
            with open(self.waypoints_file, 'w') as file:
                yaml.dump(self.waypoints, f, default_flow_style=False)

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
            self.save_waypoints