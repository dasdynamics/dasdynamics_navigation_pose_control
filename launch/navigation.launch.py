import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    # Аргументы запуска
    # # rviz2_launch_argument_declare = DeclareLaunchArgument(
    # #     'rviz2_run',
    # #     default_value = 'true',
    # #     description = 'Start Rviz2 when starting descriptions.'
    # # )

    use_sim_time_arg_declare = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time at launch.'
    )


    # Параметры окружения
    # robot_name = 'SmartBox'

    navigation_pkg_name = 'dasdynamics_navigation_pose_control'
    config_file_name = 'config'

    slam_pkg_name = 'slam_toolbox'

    # description_pkg_name = 'smartbox_description'
    # description_file_name = 'main.urdf.xacro'

    # gazebo_pkg_name = 'ros_gz_sim'
    # gazebo_config_file_name = 'gz_bridge_config.yaml'
    # gazebo_world_file_name = 'dasdynamic_test_world1.sdf'

    rviz2_config_file_name = 'rviz2_navigation_config.rviz'


    # Пути к пакетам
    # description_pkg_path = get_package_share_directory(description_pkg_name)
    # gazebo_pkg_path = get_package_share_directory(gazebo_pkg_name)
    
    navigation_pkg_path = get_package_share_directory(navigation_pkg_name)
    slam_pkg_path = get_package_share_directory(slam_pkg_name)



    # Пути к файлам
    slam_params_path = os.path.join(navigation_pkg_path, 'config', 'mapper_params_online_async.yaml')
    slam_launch_file_path = os.path.join(slam_pkg_path, 'launch', 'online_async_launch.py')
    twist_mux_params_path = os.path.join(navigation_pkg_path, 'config', 'twist_mux_params.yaml')
    nav2_params_path = os.path.join(navigation_pkg_path, 'config', 'nav2_params.yaml')

    # description_launch_file_path = os.path.join(description_pkg_path, 'launch', 'description.launch.py')
    # gazebo_launch_file_path = os.path.join(gazebo_pkg_path, 'launch', 'gz_sim.launch.py')
    # gz_bridge_config_file_path = os.path.join(simulation_pkg_path, 'configs', gazebo_config_file_name)
    rviz2_config_file_path = os.path.join(navigation_pkg_path, 'rviz', rviz2_config_file_name)
    # gazebo_world_file_path = os.path.join(simulation_pkg_path, 'worlds', gazebo_world_file_name)


    # Обращение к файлам запуска
    slam_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch_file_path),
        launch_arguments = {
            'params_file': slam_params_path
        }.items()
    )

    # gazebo_launch_include = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(gazebo_launch_file_path),
    #     launch_arguments = {
    #         'gz_args': f'-r {gazebo_world_file_path}'
    #     }.items()
    # )


    # Ноды
    twist_mux_node = Node(
        package = 'twist_mux',
        executable = 'twist_mux', 
        output = 'screen',
        parameters = [
            twist_mux_params_path,
            #{'use_stamped': LaunchConfiguration('use_sim_time')},
        ],
        remappings=[('/cmd_vel_out', '/cmd_vel')] # !!!!! Заменить
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    controller_server_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params_path],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
            # ('cmd_vel', '/cmd_vel_nav')
        ]
    )

    planner_server_node = Node(
        package='nav2_planner', 
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    behavior_server_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_params_path]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params_path]
    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'autostart': True,
            'node_names': [
                'map_server',
                'controller_server', 
                'planner_server',
                "behavior_server",
                'bt_navigator'
            ]
        }]
    )

    rviz2_launch_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        name = 'rviz2',
        output = 'screen',
        arguments = ['-d', rviz2_config_file_path],
    )


    # Запуск
    ld = LaunchDescription()



    ld.add_action(use_sim_time_arg_declare)
    ld.add_action(slam_launch_include)
    ld.add_action(rviz2_launch_node)

    # ld.add_action(twist_mux_node)
    ld.add_action(map_server_node)
    ld.add_action(controller_server_node)
    ld.add_action(planner_server_node)
    ld.add_action(behavior_server_node)
    ld.add_action(bt_navigator_node)
    ld.add_action(lifecycle_manager_node)
    

    return ld