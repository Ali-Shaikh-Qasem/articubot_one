import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'articubot_one'  # Your package with URDF and rsp.launch.py

    # 1️⃣ Launch robot_state_publisher (same as old)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2️⃣ Launch Gazebo Harmonic (ros_gz_sim style)
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', '--render-engine', 'ogre', '-r', 'empty.sdf'],
        output='screen'
    )

    # 3️⃣ Spawn your robot in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',  # Uses the topic published by robot_state_publisher
            '-name', 'my_bot'
        ],
        output='screen'
    )

    # Return LaunchDescription with all three
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])
