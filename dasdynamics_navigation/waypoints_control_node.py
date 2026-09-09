import os
import yaml
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped


class WaypointsControlNode (Node):
    def __init__(self):
        super().__init__("waypoints_control_node")

        self.pose_topic_name = '/pose'
        self.user_command_topic_name = '/user_commands'
        self.goal_pose_topic_name = '/goal_pose'

        self.save_waypoints_command = 'save_waypoint'
        self.go_to_waypoint_command = 'go_to_waypoint:'

        self.waypoints_file_path = os.path.expanduser('~/SmartBox/waypoints.yaml')
        self.waypoints = self.load_waypoints()

        self.current_pose = None

        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            self.pose_topic_name,
            self.pose_callback,
            10, 
        )

        self.pose_subscription = self.create_subscription(
            String,
            self.user_command_topic_name,
            self.user_command_callback,
            10, 
        )

        self.goal_pub = self.create_publisher(
            PoseStamped,
            self.goal_pose_topic_name,
            10,
        )

        self.get_logger().info(f'WaypointsControlNode started. Listing on {self.user_command_topic_name}')


    def pose_callback(self, msg:PoseWithCovarianceStamped):
        self.current_pose = msg.pose


    def user_command_callback(self, msg:String):
        cmd = msg.data.strip()
        self.get_logger().info(f'Received command: {cmd}')

        if cmd.startswith(self.save_waypoints_command):
            self.save_waypoints(cmd[14:])
        elif cmd.startswith(self.go_to_waypoint_command):
            self.go_to_waypoint(cmd[15:])
        else:
            self.get_logger().warning(f'Unknown command: {cmd}. Use "save_waypoint:<name>"')


    def load_waypoints(self):
        if os.path.exists(self.waypoints_file_path):
            with open(self.waypoints_file_path, 'r') as file:
                data = yaml.safe_load(file) or {}
            return data
        return {}


    def update_waypoints_file(self):
        with open(self.waypoints_file_path, 'w') as file:
            yaml.dump(self.waypoints, file, default_flow_style=False)

    def save_waypoints(self, name:str):
        name = name.strip()
        if not name:
            self.get_logger().warning('Save command without name. Use "save_waypoint:<name>"')
            return 

        if self.current_pose is None:
            self.get_logger().warning('No current pose')
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
        self.update_waypoints_file()
        self.get_logger().info(f'Save point {name}')


    def go_to_waypoint(self, name:str):
        name = name.strip()
        if not name:
            self.get_logger().warning('Go command without name. Use "go_to_waypoint:<name>"')
            return

        if name not in self.waypoints:
            self.get_logger().warning(f'Waypoint "{name}" not found')
            return

        wp = self.waypoints[name]

        goal = PoseStamped()
        goal.header.frame_id = 'map'
        goal.pose.position.x = wp['x']
        goal.pose.position.y = wp['y']
        goal.pose.position.z = wp['z']
        goal.pose.orientation.x = wp['ox']
        goal.pose.orientation.y = wp['oy']
        goal.pose.orientation.z = wp['oz']
        goal.pose.orientation.w = wp['ow']

        self.get_logger().info(f'Navigating to "{name}"')
        self.goal_pub.publish(goal)


def main():
    rclpy.init()
    node = WaypointsControlNode()
    rclpy.spin(node)
    node.destroy_node()


if __name__ == '__main__':
    main()
