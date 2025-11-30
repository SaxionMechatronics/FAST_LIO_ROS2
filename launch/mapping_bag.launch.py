import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    package_path = get_package_share_directory('fast_lio')

    default_config_path = os.path.join(package_path, 'config')
    default_rviz_config_path = os.path.join(package_path, 'rviz', 'fastlio.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time')
    config_path = LaunchConfiguration('config_path')
    config_file = LaunchConfiguration('config_file')
    rviz_use = LaunchConfiguration('rviz')
    rviz_cfg = LaunchConfiguration('rviz_cfg')
    bag_folder = LaunchConfiguration('bag_folder')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    declare_config_path_cmd = DeclareLaunchArgument(
        'config_path',
        default_value=default_config_path,
        description='Yaml config file path'
    )
    declare_config_file_cmd = DeclareLaunchArgument(
        'config_file',
        default_value='ouster128.yaml',
        description='Config file'
    )
    declare_rviz_cmd = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Use RViz to monitor results'
    )
    declare_rviz_config_path_cmd = DeclareLaunchArgument(
        'rviz_cfg',
        default_value=default_rviz_config_path,
        description='RViz config file path'
    )
    declare_bag_folder_cmd = DeclareLaunchArgument(
        'bag_folder',
        description='Path to the ros2 bag folder to play'
    )

    fast_lio_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                package_path,
                'launch',
                'mapping_rviz.launch.py'   
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'config_path': config_path,
            'config_file': config_file,
            'rviz': rviz_use,
            'rviz_cfg': rviz_cfg,
        }.items()
    )

    bag_play_proc = ExecuteProcess(
        cmd=['ros2', 'bag', 'play', bag_folder],
        output='screen'
    )

    bag_play_delayed = TimerAction(
        period=3.0,        
        actions=[bag_play_proc]
    )

    ld = LaunchDescription()

    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_config_path_cmd)
    ld.add_action(declare_config_file_cmd)
    ld.add_action(declare_rviz_cmd)
    ld.add_action(declare_rviz_config_path_cmd)
    ld.add_action(declare_bag_folder_cmd)
    ld.add_action(fast_lio_launch)
    ld.add_action(bag_play_delayed)

    return ld
