from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('livox_ros')

    rviz = LaunchConfiguration('rviz')
    publish_freq = LaunchConfiguration('publish_freq')
    frame_id = LaunchConfiguration('frame_id')
    lvx_config_file = LaunchConfiguration('lvx_config_file')
    lvx_lidar_topic = LaunchConfiguration('lvx_lidar_topic')
    lvx_imu_topic = LaunchConfiguration('lvx_imu_topic')

    declare_rviz_arg = DeclareLaunchArgument(
        'rviz',
        default_value='false',
        description='Whether to launch RViz',
        choices=['true', 'false']
    )

    declare_publish_freq_arg = DeclareLaunchArgument(
        'publish_freq',
        default_value='100.0',
        description='LiDAR publish frequency (e.g. 10.0, 50.0, 100.0)'
    )

    declare_frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='livox_frame',
        description='Frame ID for the LiDAR data'
    )

    declare_lvx_config_file_arg = DeclareLaunchArgument(
        'lvx_config_file',
        default_value=PathJoinSubstitution([pkg_share, 'config', 'MID360_config.json']),
        description='Path to Livox .json configuration file'
    )

    declare_lvx_lidar_topic = DeclareLaunchArgument(
        'lvx_lidar_topic',
        default_value='/livox/lidar',
        description='Livox topic where raw points are published'
    )

    declare_lvx_imu_topic = DeclareLaunchArgument(
        'lvx_imu_topic',
        default_value='/livox/imu',
        description='Livox topic where IMU data is published'
    )

    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        output='screen',
        remappings=[
            ('/livox/lidar', lvx_lidar_topic),
            ('/livox/imu', lvx_imu_topic)
        ],
        parameters=[{
            'xfer_format': 1,  # 0-Pointcloud2(PointXYZRTL), 1-customized pointcloud format
            'multi_topic': 0,  # 0-All LiDARs share the same topic, 1-One LiDAR one topic
            'data_src': 0,     # 0-lidar, others-Invalid data src
            'publish_freq': publish_freq,
            'output_data_type': 0,
            'frame_id': frame_id,
            'user_config_path': lvx_config_file,
        }]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', PathJoinSubstitution([pkg_share, 'config', 'livox_pointcloud.rviz'])],
        condition=IfCondition(rviz),
        output='screen'
    )

    return LaunchDescription([
        declare_rviz_arg,
        declare_publish_freq_arg,
        declare_frame_id_arg,
        declare_lvx_config_file_arg,
        declare_lvx_lidar_topic,
        declare_lvx_imu_topic,
        livox_driver,
        rviz_node,
    ])
